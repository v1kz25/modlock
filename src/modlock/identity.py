"""Conservative identity evidence within one Meteoric export, without matching."""

from collections import Counter, defaultdict
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from modlock.meteoric import MeteoricExport, MeteoricRecord, ReadWarning

type IdentityState = Literal["referenced", "incomplete", "ambiguous", "not_applicable"]
type IdentityReason = Literal[
    "missing_page_id",
    "missing_file_reference",
    "incomplete_file_list",
    "conflicting_page_id",
    "duplicate_reference",
    "name_collision",
]


@dataclass(frozen=True, order=True)
class FileReference:
    """Numeric page/file reference, scoped to the source's unspecified game context."""

    page_id: int
    file_id: int


@dataclass(frozen=True)
class IdentityEvidence:
    state: IdentityState
    references: tuple[FileReference, ...]
    reasons: tuple[IdentityReason, ...]
    conflicting_indices: tuple[int, ...]


@dataclass(frozen=True)
class NormalizedRecord:
    original: MeteoricRecord
    identity: IdentityEvidence


@dataclass(frozen=True)
class NormalizedExport:
    source: Path
    records: tuple[NormalizedRecord, ...]
    read_warnings: tuple[ReadWarning, ...]


def _positive_id(value: str | None) -> int | None:
    # No whitespace, Unicode-digit conversion, sign guessing or name parsing.
    if not value or not value.isascii() or not value.isdecimal():
        return None
    try:
        number = int(value)
    except ValueError:
        return None  # Preserve oversized/unrepresentable source text as unknown.
    return number if number > 0 else None


def _references(
    record: MeteoricRecord,
) -> tuple[tuple[FileReference, ...], set[IdentityReason]]:
    reasons: set[IdentityReason] = set()
    page = record.source_id if type(record.source_id) is int else None
    if page is None:
        reasons.add("missing_page_id")
    declared = record.general.get("modid")
    if declared and page is not None and _positive_id(declared) != page:
        reasons.add("conflicting_page_id")

    installed = record.installed
    if (
        installed.size is None
        or installed.files is None
        or installed.size != len(installed.files)
    ):
        reasons.add("incomplete_file_list")
    references = []
    for file in installed.files or ():
        file_page = _positive_id(file.get("modid"))
        file_id = _positive_id(file.get("fileid"))
        if file_page is None or file_id is None:
            reasons.add("missing_file_reference")
            continue
        references.append(FileReference(file_page, file_id))
        if page is not None and file_page != page:
            reasons.add("conflicting_page_id")
    if not references:
        reasons.add("missing_file_reference")
    # Sort only reference evidence. Keep every occurrence, original file order and text.
    return tuple(sorted(references)), reasons


def normalize_export(export: MeteoricExport) -> NormalizedExport:
    """Retain all reader records and annotate uncertainty within this export only.

    Referenced means complete, locally unique page/file evidence, not verified
    Nexus existence, content, variant, game, or identity across exports. The
    returned originals are detached copies; this function never reads/writes files.
    """
    source = deepcopy(export)
    evidence: dict[int, tuple[tuple[FileReference, ...], set[IdentityReason]]] = {}
    by_reference: dict[FileReference, set[int]] = defaultdict(set)
    reference_counts: Counter[FileReference] = Counter()
    by_name: dict[str, set[int]] = defaultdict(set)

    for record in source.records:
        if record.kind != "mod":
            continue
        references, reasons = _references(record)
        evidence[record.index] = references, reasons
        for reference in references:
            by_reference[reference].add(record.index)
            reference_counts[reference] += 1
        if record.mod_name:
            # A conservative collision warning, never an identity or rewritten name.
            by_name[record.mod_name.casefold()].add(record.index)

    records = []
    for record in source.records:
        if record.kind == "separator":
            identity = IdentityEvidence("not_applicable", (), (), ())
        else:
            references, reasons = evidence[record.index]
            conflicts: set[int] = set()
            for reference in references:
                if reference_counts[reference] > 1:
                    reasons.add("duplicate_reference")
                    conflicts.update(by_reference[reference] - {record.index})
            names = by_name.get(record.mod_name.casefold(), set())
            if len(names) > 1:
                reasons.add("name_collision")
                conflicts.update(names - {record.index})
            state: IdentityState = "referenced"
            if reasons:
                state = "incomplete"
            if reasons & {
                "conflicting_page_id",
                "duplicate_reference",
                "name_collision",
            }:
                state = "ambiguous"
            identity = IdentityEvidence(
                state, references, tuple(sorted(reasons)), tuple(sorted(conflicts))
            )
        records.append(NormalizedRecord(record, identity))
    return NormalizedExport(source.source, tuple(records), source.warnings)
