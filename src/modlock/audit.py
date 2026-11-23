"""Observe export evidence only; never certify reproducibility or installed data."""

from collections import Counter
from dataclasses import asdict, dataclass
from typing import Literal

from modlock.identity import NormalizedExport, checked_export
from modlock.meteoric import JsonObject


@dataclass(frozen=True)
class Signal:
    state: Literal["present", "unknown"]
    location: str | None
    reason: str


def audit_export(export: NormalizedExport) -> JsonObject:
    """Return independent per-mod observations, including disabled entries.

    Unknown means insufficient supported evidence, not absence in the installed
    game. JSON locations point into the original export; no source paths leak.
    """
    source = checked_export(export)
    records = []
    unknown: Counter[str] = Counter()
    for entry in source.records:
        row = entry.original
        if row.kind != "mod":
            continue
        location = f"$[{row.index}]"
        page_known = (
            type(row.source_id) is int
            and "conflicting_page_id" not in entry.identity.reasons
        )
        version = row.general.get("version")
        signals = {
            "page_identifier": Signal(
                "present" if page_known else "unknown",
                location + ".id",
                "declared_page_id" if page_known else "missing_or_conflicting_page_id",
            ),
            "version": Signal(
                "present" if version and version.strip() else "unknown",
                location + ".general.version",
                "declared_version"
                if version and version.strip()
                else "missing_version"
                if version is None
                else "empty_version",
            ),
            "file_references": Signal(
                "present" if entry.identity.state == "referenced" else "unknown",
                location + ".installed",
                "locally_unique_references"
                if entry.identity.state == "referenced"
                else "incomplete_or_ambiguous_references",
            ),
            "order": Signal("present", location + ".order", "export_position_only"),
            "content_hash": Signal("unknown", None, "unsupported_content_evidence"),
            "provenance": Signal("unknown", None, "unauthenticated_producer"),
            "game": Signal("unknown", None, "unverified_game_context"),
        }
        unknown.update(k for k, signal in signals.items() if signal.state == "unknown")
        records.append(
            {
                "index": row.index,
                "signals": {key: asdict(value) for key, value in signals.items()},
            }
        )
    return {
        "records": records,
        "summary": {
            "mods": len(records),
            "unknown_signals": dict(sorted(unknown.items())),
        },
    }


def audit_pair(base: NormalizedExport, head: NormalizedExport) -> JsonObject:
    """Independent observations, not additional matching or a security score."""
    return {
        "schema": "modlock-audit-0.2-experimental",
        "base": audit_export(base),
        "head": audit_export(head),
        "limitations": [
            "Presence is declared export metadata, not verified installed content.",
            "Unknown does not prove absence, incompatibility or malicious content.",
            "Order is export position, not plugin load order or conflict detection.",
            "Unknown extension fields are preserved but not trusted as evidence.",
        ],
    }
