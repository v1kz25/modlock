"""Human summaries preserve the complete machine-readable evidence."""

import json
from pathlib import Path

from typer.testing import CliRunner

from modlock.cli import app
from modlock.reports import render_markdown

ROOT = Path(__file__).resolve().parents[1]


def test_review_markdown_snapshot_and_complete_json_compatibility() -> None:
    fixture = (
        ROOT / "docs/research/issue-2/fixtures/anomalous/02-partial-installed.json"
    )
    runner = CliRunner()
    args = [
        "compare",
        str(fixture),
        str(fixture),
        "--context",
        "synthetic:review",
        "--audit",
    ]
    json_result = runner.invoke(app, args)
    markdown_result = runner.invoke(app, args + ["--format", "markdown"])
    assert json_result.exit_code == markdown_result.exit_code == 0
    markdown = markdown_result.stdout
    expected = (ROOT / "tests/fixtures/review-report.md").read_text(encoding="utf-8")
    assert markdown == expected
    payload = markdown.split("```json\n", 1)[1].rsplit("\n```", 1)[0]
    data = json.loads(json_result.stdout)
    assert json.loads(payload) == data
    assert data["summary"] == {"ambiguous": 2}
    assert data["warnings"]["base"] and data["warnings"]["head"]
    assert "| ambiguous | 2 |" in markdown
    assert r"| base | file\_references | 1 |" in markdown


def test_warning_and_summary_text_cannot_escape_markdown() -> None:
    data = json.loads(
        (ROOT / "tests/fixtures/empty-report.json").read_text(encoding="utf-8")
    )
    hostile = "<script>|[click](https://example.com)\n日本語" + (chr(96) * 9)
    data["warnings"]["base"].append(
        {"code": hostile, "location": "$[0]", "message": hostile}
    )
    data["summary"][hostile] = 1
    markdown = render_markdown(data)
    human = markdown.split("## Complete evidence")[0]
    assert "<script>" not in human
    assert "&lt;script&gt;" in human and r"\|" in human and r"\[click\]" in human
    assert "日本語" in human
    fence = chr(96) * 10
    assert fence + "json\n" in markdown
    assert (
        json.loads(markdown.split(fence + "json\n", 1)[1].rsplit("\n" + fence, 1)[0])
        == data
    )


def test_empty_report_explicitly_has_no_warnings_or_records() -> None:
    data = json.loads(
        (ROOT / "tests/fixtures/empty-report.json").read_text(encoding="utf-8")
    )
    markdown = render_markdown(data)
    assert "No comparison records." in markdown
    assert "## Reader warnings\n\nNone." in markdown
    assert "## Reproducibility signals" not in markdown
