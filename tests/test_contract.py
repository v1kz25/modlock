"""Compatibility against evidence captured from the published v0.1 wheel."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from modlock.cli import app

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("audit", [False, True])
def test_v01_machine_report_is_preserved(audit: bool) -> None:
    args = [
        "compare",
        str(ROOT / "examples/base.json"),
        str(ROOT / "examples/head.json"),
        "--context",
        "synthetic:contract",
    ]
    if audit:
        args.append("--audit")
    result = CliRunner().invoke(app, args)
    assert result.exit_code == 0, result.output
    data = json.loads(result.stdout)
    expected = json.loads(
        (ROOT / "tests/fixtures/contract-v0.1.json").read_text(encoding="utf-8")
    )
    if audit:
        assert data.pop("audit")["schema"] == "modlock-audit-0.2-experimental"
    assert data == expected


def test_legacy_output_alias_keeps_exit_and_exclusive_creation(tmp_path: Path) -> None:
    output = tmp_path / "legacy.json"
    args = [
        "compare",
        str(ROOT / "examples/base.json"),
        str(ROOT / "examples/head.json"),
        "-o",
        str(output),
    ]
    runner = CliRunner()
    assert runner.invoke(app, args).exit_code == 0
    saved = output.read_bytes()
    assert json.loads(saved)["context"] is None
    assert runner.invoke(app, args).exit_code == 1
    assert output.read_bytes() == saved


def test_unknown_metadata_is_preserved_without_certifying_new_format(
    tmp_path: Path,
) -> None:
    rows = json.loads((ROOT / "examples/base.json").read_text(encoding="utf-8"))
    rows[1]["future_field"] = {"unrecognized": [None, 7, "日本語"]}
    path = tmp_path / "future.json"
    path.write_text(json.dumps(rows), encoding="utf-8")
    result = CliRunner().invoke(app, ["compare", str(path), str(path)])
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    raw = next(
        c["base"]["data"]
        for c in data["changes"]
        if c["base"] and c["base"]["index"] == 1
    )
    assert raw["future_field"] == rows[1]["future_field"]
    assert any(w["code"] == "unknown_field" for w in data["warnings"]["base"])
    rows[1]["type"] = "future_record_type"
    path.write_text(json.dumps(rows), encoding="utf-8")
    unsupported = CliRunner().invoke(app, ["compare", str(path), str(path)])
    assert unsupported.exit_code == 1 and "unsupported" in unsupported.stderr
