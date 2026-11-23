"""Local experimental JSON/Markdown views; never expose source filesystem paths."""

import html
import json
import re
from collections import Counter
from dataclasses import asdict

from modlock.comparison import Comparison
from modlock.meteoric import ReadWarning

LIMITATIONS = [
    "Experimental Meteoric JSON 1.0 structure; producer/version not authenticated.",
    "Context is a caller assertion of same game and export lineage, not verification.",
    "Reference correspondence is not content integrity, FOMOD equivalence or compatibility.",
    "Changed file IDs, incomplete identities and collisions can remain unresolved.",
]


def report_data(
    result: Comparison,
    base_warnings: tuple[ReadWarning, ...] = (),
    head_warnings: tuple[ReadWarning, ...] = (),
) -> dict:
    def record(value):
        if value is None:
            return None
        return dict(
            index=value.original.index,
            identity=asdict(value.identity),
            data=value.original.raw,
        )

    return dict(
        schema="modlock-0.1-experimental",
        context=result.context,
        limitations=LIMITATIONS.copy(),
        summary=dict(sorted(Counter(c.category for c in result.changes).items())),
        warnings=dict(
            base=[asdict(w) for w in base_warnings],
            head=[asdict(w) for w in head_warnings],
        ),
        changes=[
            dict(
                category=c.category,
                fields=list(c.fields),
                reason=c.reason,
                base=record(c.base),
                head=record(c.head),
            )
            for c in result.changes
        ],
    )


def render_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=True, sort_keys=True, indent=2) + "\n"


def _cell(value: str) -> str:
    text = html.escape(value).replace("\r", " ").replace("\n", " ")
    text = text.encode("utf-8", "backslashreplace").decode("utf-8")
    return re.sub(r"([\\`*_{}\[\]()#+.!|>\-])", r"\\\1", text)


def render_markdown(data: dict) -> str:
    lines = [
        "# modlock comparison",
        "",
        f"Context: {_cell(data['context'] or 'unconfirmed')}",
        "",
        "| Category | Base index/name | Head index/name | Fields / reason |",
        "|---|---|---|---|",
    ]
    for change in data["changes"]:

        def label(record):
            return (
                ""
                if record is None
                else f"{record['index']}: {record['data']['displayName']}"
            )

        lines.append(
            "| "
            + " | ".join(
                _cell(v)
                for v in (
                    change["category"],
                    label(change["base"]),
                    label(change["head"]),
                    ", ".join(change["fields"]) or change["reason"] or "",
                )
            )
            + " |"
        )
    lines.extend(["", "## Summary", "", "| Category | Count |", "|---|---:|"])
    for category, count in sorted(data["summary"].items()):
        lines.append(f"| {_cell(category)} | {_cell(str(count))} |")
    if not data["summary"]:
        lines.extend(["", "No comparison records."])
    lines.extend(["", "## Reader warnings", ""])
    warnings = [
        (side, warning)
        for side in ("base", "head")
        for warning in data["warnings"][side]
    ]
    if warnings:
        lines.extend(["| Side | Location | Code | Message |", "|---|---|---|---|"])
        for side, warning in warnings:
            lines.append(
                "| "
                + " | ".join(
                    _cell(value)
                    for value in (
                        side,
                        warning["location"],
                        warning["code"],
                        warning["message"],
                    )
                )
                + " |"
            )
    else:
        lines.append("None.")
    if "audit" in data:
        lines.extend(
            [
                "",
                "## Reproducibility signals",
                "",
                "Unknown means insufficient evidence; presence is declared metadata.",
                "",
                "| Side | Unknown signal | Count |",
                "|---|---|---:|",
            ]
        )
        for side in ("base", "head"):
            for signal, count in sorted(
                data["audit"][side]["summary"]["unknown_signals"].items()
            ):
                lines.append(f"| {side} | {_cell(signal)} | {_cell(str(count))} |")
    lines.extend(
        ["", "## Limitations", ""] + ["- " + _cell(v) for v in data["limitations"]]
    )
    # Full JSON preserves all findings, unknown metadata and reader warnings. A dynamic
    # fence prevents hostile names/metadata from terminating this code block.
    payload = render_json(data)
    fence = "`" * max(
        3, 1 + max((len(m.group()) for m in re.finditer(r"`+", payload)), default=0)
    )
    lines.extend(
        [
            "",
            "## Complete evidence (JSON)",
            "",
            fence + "json",
            payload.rstrip("\n"),
            fence,
            "",
        ]
    )
    return "\n".join(lines)
