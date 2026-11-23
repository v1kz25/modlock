"""End-to-end reports, source path privacy and exclusive output creation."""

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from modlock.cli import app

runner = CliRunner()
FIXTURE = Path(__file__).parent / "fixtures/identity/export.json"


def inputs(tmp_path: Path, *, hostile: bool = False):
    row = json.loads(FIXTURE.read_text(encoding="utf-8"))[1]
    row.update(order=0, separatorName="Unsectioned")
    old, new = tmp_path / "base.json", tmp_path / "head.json"
    old.write_text(json.dumps([row]), encoding="utf-8")
    row["general"]["version"] = "2"
    if hostile:
        row["modName"] = row["displayName"] = (
            "<script>alert(1)</script>|[link](https://example.com)\n"
            + (chr(96) * 7)
            + "\n\ud800"
        )
    new.write_text(json.dumps([row]), encoding="utf-8")
    return old, new


@pytest.mark.parametrize("format", ["json", "markdown"])
def test_reports_are_deterministic_and_inputs_intact(
    tmp_path: Path, format: str
) -> None:
    old, new = inputs(tmp_path)
    before = old.read_bytes(), new.read_bytes()
    args = [
        "compare",
        str(old),
        str(new),
        "--context",
        "synthetic:lineage",
        "--format",
        format,
    ]
    first, second = runner.invoke(app, args), runner.invoke(app, args)
    assert first.exit_code == 0, first.output
    assert first.stdout_bytes == second.stdout_bytes
    assert (old.read_bytes(), new.read_bytes()) == before
    assert str(tmp_path) not in first.stdout
    if format == "json":
        data = json.loads(first.stdout)
        assert data["summary"] == {"modified": 1}
        assert data["changes"][0]["fields"] == ["version"]
    else:
        assert "Complete evidence" in first.stdout
        assert '"version"' in first.stdout


def test_missing_context_is_explicitly_unresolved(tmp_path: Path) -> None:
    old, new = inputs(tmp_path)
    result = runner.invoke(app, ["compare", str(old), str(new)])
    assert result.exit_code == 0, result.output
    data = json.loads(result.stdout)
    assert data["context"] is None
    assert data["summary"] == {"ambiguous": 2}


def test_output_is_created_once_and_never_overwrites_input(tmp_path: Path) -> None:
    old, new = inputs(tmp_path)
    before = old.read_bytes(), new.read_bytes()
    output = tmp_path / "report.json"
    args = ["compare", str(old), str(new), "--output", str(output)]
    assert runner.invoke(app, args).exit_code == 0
    saved = output.read_bytes()
    assert runner.invoke(app, args).exit_code == 1
    assert output.read_bytes() == saved
    for source in (old, new):
        attempt = runner.invoke(
            app, ["compare", str(old), str(new), "--output", str(source)]
        )
        assert attempt.exit_code == 1
    assert (old.read_bytes(), new.read_bytes()) == before


def test_markdown_escapes_hostile_table_and_fence_input(tmp_path: Path) -> None:
    old, new = inputs(tmp_path, hostile=True)
    result = runner.invoke(
        app,
        [
            "compare",
            str(old),
            str(new),
            "--context",
            "synthetic",
            "--format",
            "markdown",
        ],
    )
    assert result.exit_code == 0, result.output
    table = result.stdout.split("## Limitations")[0]
    assert "<script>" not in table
    assert "&lt;script&gt;" in table
    assert r"\|" in table
    assert r"\[link\]" in table
    assert (chr(96) * 8) + "json" in result.stdout


@pytest.mark.parametrize("bad", ["missing", "invalid", "format"])
def test_useful_error_codes_without_tracebacks_or_writes(
    tmp_path: Path, bad: str
) -> None:
    old, new = inputs(tmp_path)
    args = ["compare", str(old), str(new)]
    expected = 1
    if bad == "missing":
        old.unlink()
    elif bad == "invalid":
        old.write_bytes(b"[truncated")
    else:
        args += ["--format", "html"]
        expected = 2
    before = new.read_bytes()
    result = runner.invoke(app, args)
    assert result.exit_code == expected, result.output
    assert "Error" in result.output
    assert "Traceback" not in result.output
    assert new.read_bytes() == before


def test_empty_report_golden_and_warning_conservation(tmp_path: Path) -> None:
    old, new = tmp_path / "a.json", tmp_path / "b.json"
    old.write_text("[]", encoding="utf-8")
    new.write_text("[]", encoding="utf-8")
    result = runner.invoke(app, ["compare", str(old), str(new)])
    expected = Path(__file__).parent / "fixtures/empty-report.json"
    assert json.loads(result.stdout) == json.loads(expected.read_text(encoding="utf-8"))
    row = json.loads(FIXTURE.read_text(encoding="utf-8"))[6]
    row.update(order=0, separatorName="Unsectioned")
    old.write_text(json.dumps([row]), encoding="utf-8")
    data = json.loads(runner.invoke(app, ["compare", str(old), str(new)]).stdout)
    assert data["warnings"]["base"]
    assert data["changes"][0]["base"]["data"] == row
