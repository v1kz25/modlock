"""Run the optional audit/report pipeline over the entire pinned format corpus."""

import hashlib
import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from modlock.cli import app

CORPUS = Path(__file__).resolve().parents[1] / "docs/research/issue-2"
CASES = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))["fixtures"]


@pytest.mark.parametrize("case", CASES, ids=lambda c: c["path"])
@pytest.mark.parametrize("format", ["json", "markdown"])
def test_full_format_corpus_with_audit(case: dict, format: str) -> None:
    path = CORPUS / "fixtures" / case["path"]
    before = path.read_bytes()
    assert hashlib.sha256(before).hexdigest() == case["sha256"]
    args = [
        "compare",
        str(path),
        str(path),
        "--audit",
        "--format",
        format,
        "--context",
        "synthetic:corpus",
    ]
    runner = CliRunner()
    first, second = runner.invoke(app, args), runner.invoke(app, args)
    assert first.stdout_bytes == second.stdout_bytes
    assert first.stderr_bytes == second.stderr_bytes
    assert (
        first.exit_code == second.exit_code == (1 if case["kind"] == "invalid" else 0)
    )
    assert path.read_bytes() == before
    if case["kind"] == "invalid":
        assert "Traceback" not in first.output and "Error" in first.output
        return
    payload = first.stdout
    if format == "markdown":
        payload = payload.split("```json\n", 1)[1].rsplit("\n```", 1)[0]
    report = json.loads(payload)
    expected = json.loads(before.decode("utf-8-sig"))
    mods = sum(row["type"] == "mod" for row in expected)
    for side in ("base", "head"):
        evidence = [c[side] for c in report["changes"] if c[side] is not None]
        assert sorted(r["index"] for r in evidence) == list(range(len(expected)))
        assert all(r["data"] == expected[r["index"]] for r in evidence)
        assert report["audit"][side]["summary"]["mods"] == mods
        for entry in report["audit"][side]["records"]:
            for name in ("content_hash", "game", "provenance"):
                assert entry["signals"][name]["state"] == "unknown"
