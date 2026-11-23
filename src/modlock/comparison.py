"""Conservative, deterministic comparison of two normalized in-memory exports."""

from dataclasses import dataclass
from typing import Literal

from modlock.identity import (
    FileReference,
    NormalizedExport,
    NormalizedRecord,
    checked_export,
)

type Category = Literal[
    "added", "removed", "modified", "reordered", "unchanged", "ambiguous", "separator"
]


@dataclass(frozen=True)
class Change:
    category: Category
    base: NormalizedRecord | None
    head: NormalizedRecord | None
    fields: tuple[str, ...] = ()
    reason: str | None = None


@dataclass(frozen=True)
class Comparison:
    context: str | None
    changes: tuple[Change, ...]


def _key(record: NormalizedRecord) -> tuple[FileReference, ...]:
    return record.identity.references


def _fields(
    base: NormalizedRecord, head: NormalizedRecord, moved: bool
) -> tuple[str, ...]:
    old, new = base.original, head.original
    fields = []
    for name, left, right in (
        ("name", (old.mod_name, old.display_name), (new.mod_name, new.display_name)),
        ("section", old.separator_name, new.separator_name),
        ("active", old.active, new.active),
        ("plugins", old.plugins, new.plugins),
        ("tags", old.tags, new.tags),
    ):
        if left != right:
            fields.append(name)
    a, b = old.general.get("version"), new.general.get("version")
    if a != b:
        fields.append("version" if a and b else "version_metadata")
    excluded = {
        "order",
        "separatorName",
        "modName",
        "displayName",
        "active",
        "plugins",
        "tags",
        "general",
    }
    other_old = {k: v for k, v in old.raw.items() if k not in excluded}
    other_new = {k: v for k, v in new.raw.items() if k not in excluded}
    general_old = {k: v for k, v in old.raw["general"].items() if k != "version"}
    general_new = {k: v for k, v in new.raw["general"].items() if k != "version"}
    if other_old != other_new or general_old != general_new:
        fields.append("metadata")
    if moved:
        fields.append("order")
    return tuple(sorted(fields))


def compare_exports(
    base: NormalizedExport, head: NormalizedExport, *, context: str | None = None
) -> Comparison:
    """Pair only unique complete identical reference sets in a caller-asserted context.

    Context asserts the same game AND export lineage. It is not inferred from the
    JSON, filenames or names, nor verified externally. Without it all mods remain
    unresolved. A changed file ID never becomes a version match by page/name alone.
    """
    if context is not None and (not isinstance(context, str) or not context.strip()):
        raise ValueError(
            "Context must be a non-empty same-game/export-lineage assertion."
        )
    old, new = checked_export(base), checked_export(head)
    old_mods = [r for r in old.records if r.original.kind == "mod"]
    new_mods = [r for r in new.records if r.original.kind == "mod"]
    left = {_key(r): r for r in old_mods if r.identity.state == "referenced"}
    right = {_key(r): r for r in new_mods if r.identity.state == "referenced"}
    common = left.keys() & right.keys() if context is not None else set()
    old_rank = {key: i for i, key in enumerate(k for k in left if k in common)}
    new_rank = {key: i for i, key in enumerate(k for k in right if k in common)}
    changes = []
    paired_head = set()
    for record in old.records:
        if record.original.kind == "separator":
            changes.append(Change("separator", record, None))
        elif _key(record) in common and record.identity.state == "referenced":
            other = right[_key(record)]
            fields = _fields(
                record, other, old_rank[_key(record)] != new_rank[_key(record)]
            )
            category: Category = "unchanged"
            if fields:
                category = "reordered" if fields == ("order",) else "modified"
            changes.append(Change(category, record, other, fields))
            paired_head.add(other.original.index)
        else:
            changes.append(_unpaired(record, new_mods, context, "base"))
    for record in new.records:
        if record.original.kind == "separator":
            changes.append(Change("separator", None, record))
        elif record.original.index not in paired_head:
            changes.append(_unpaired(record, old_mods, context, "head"))
    return Comparison(context, tuple(changes))


def _unpaired(
    record: NormalizedRecord,
    others: list[NormalizedRecord],
    context: str | None,
    side: str,
) -> Change:
    reason = None
    if context is None:
        reason = "unconfirmed_context"
    elif record.identity.state != "referenced":
        reason = "uncertain_identity"
    elif any(r.identity.state != "referenced" for r in others):
        reason = "unresolved_identity_in_other_export"
    elif any(
        record.original.source_id == r.original.source_id
        or set(_key(record)) & set(_key(r))
        for r in others
    ):
        reason = "unresolved_page_or_reference_overlap"
    if reason:
        return Change(
            "ambiguous",
            record if side == "base" else None,
            record if side == "head" else None,
            reason=reason,
        )
    return Change(
        "removed" if side == "base" else "added",
        record if side == "base" else None,
        record if side == "head" else None,
    )
