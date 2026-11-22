"""Exercise the original ten synthetic pairs through the installed CLI pipeline."""

import hashlib
import json
import socket
from pathlib import Path

import pytest
from typer.testing import CliRunner

from modlock.cli import app

CORPUS = Path(__file__).resolve().parents[1] / "docs/research/issue-1/fixtures"


@pytest.mark.parametrize("case", sorted(CORPUS.iterdir()), ids=lambda p: p.name)
def test_ten_pairs_preserve_every_record_and_input(case: Path) -> None:
    old, new = case / "old.json", case / "new.json"
    before = [p.read_bytes() for p in (old, new)]
    result = CliRunner().invoke(
        app, ["compare", str(old), str(new), "--context", "synthetic:corpus"]
    )
    assert result.exit_code == 0, result.output
    report = json.loads(result.stdout)
    for side, raw in zip(("base", "head"), before, strict=True):
        expected = json.loads(raw)
        records = [
            change[side] for change in report["changes"] if change[side] is not None
        ]
        assert sorted(r["index"] for r in records) == list(range(len(expected)))
        assert all(r["data"] == expected[r["index"]] for r in records)
    assert [hashlib.sha256(p.read_bytes()).digest() for p in (old, new)] == [
        hashlib.sha256(raw).digest() for raw in before
    ]


def test_comparison_and_reports_need_no_network(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def blocked(*args, **kwargs):
        raise AssertionError("Comparison attempted network access")

    fixture = CORPUS / "01-identical/old.json"
    with monkeypatch.context() as context:
        context.setattr(socket, "socket", blocked)
        context.setattr(socket, "create_connection", blocked)
        result = CliRunner().invoke(
            app, ["compare", str(fixture), str(fixture), "--context", "synthetic"]
        )
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["summary"]["unchanged"] == 1
