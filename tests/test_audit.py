"""Evidence never upgrades unknowns into proof of a reproducible installation."""

import json
import socket
from copy import deepcopy
from pathlib import Path

import pytest
from typer.testing import CliRunner

from modlock.audit import audit_export
from modlock.cli import app
from modlock.identity import normalize_export
from modlock.meteoric import read_meteoric

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/base.json"


def source(tmp_path: Path, change=None):
    rows = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    if change:
        change(rows[1])
    path = tmp_path / "export.json"
    path.write_text(json.dumps(rows), encoding="utf-8")
    return path, normalize_export(read_meteoric(path))


def test_known_metadata_has_unknown_content_game_and_provenance(tmp_path: Path) -> None:
    path, export = source(tmp_path)
    before = deepcopy(export)
    result = audit_export(export)
    assert result["summary"] == {
        "mods": 1,
        "unknown_signals": {"content_hash": 1, "game": 1, "provenance": 1},
    }
    assert [r["index"] for r in result["records"]] == [1]
    signals = result["records"][0]["signals"]
    assert signals["version"] == {
        "state": "present",
        "location": "$[1].general.version",
        "reason": "declared_version",
    }
    assert signals["order"]["reason"] == "export_position_only"
    assert signals["file_references"]["state"] == "present"
    assert export == before
    assert str(path) not in json.dumps(result)


@pytest.mark.parametrize(
    ("version", "reason"),
    [(None, "missing_version"), ("", "empty_version"), (" \t", "empty_version")],
)
def test_missing_empty_and_whitespace_versions_are_unknown(
    tmp_path: Path, version: str | None, reason: str
) -> None:
    def change(row):
        if version is None:
            row["general"].pop("version")
        else:
            row["general"]["version"] = version

    _, export = source(tmp_path, change)
    assert audit_export(export)["records"][0]["signals"]["version"] == {
        "state": "unknown",
        "location": "$[1].general.version",
        "reason": reason,
    }


@pytest.mark.parametrize("case", ["local", "conflicting", "partial", "duplicate"])
def test_uncertain_references_are_not_promoted(tmp_path: Path, case: str) -> None:
    def change(row):
        if case == "local":
            row["id"] = "Synthetic Alpha"
        elif case == "conflicting":
            row["general"]["modid"] = "999"
        elif case == "partial":
            row["installed"]["size"] = 2
        else:
            row["installed"]["files"] *= 2
            row["installed"]["size"] = 2

    _, export = source(tmp_path, change)
    signals = audit_export(export)["records"][0]["signals"]
    assert signals["file_references"]["state"] == "unknown"
    if case in {"local", "conflicting"}:
        assert signals["page_identifier"]["state"] == "unknown"


def test_disabled_mod_and_untrusted_extension_are_preserved(tmp_path: Path) -> None:
    def change(row):
        row["active"] = False
        row["sha256"] = "fake hash"
        row["provenance"] = "trusted by nobody"
        row["game"] = "claimed game"

    _, export = source(tmp_path, change)
    result = audit_export(export)
    assert result["summary"]["mods"] == 1
    for name in ("content_hash", "provenance", "game"):
        assert result["records"][0]["signals"][name]["state"] == "unknown"


def test_mutated_normalized_model_is_rejected(tmp_path: Path) -> None:
    _, export = source(tmp_path)
    export.records[1].original.raw["general"]["version"] = "changed"
    with pytest.raises(ValueError, match="inconsistent"):
        audit_export(export)


@pytest.mark.parametrize("format", ["json", "markdown"])
def test_audit_cli_is_opt_in_deterministic_offline_and_read_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, format: str
) -> None:
    path, _ = source(tmp_path)
    before = path.read_bytes()

    def blocked(*args, **kwargs):
        raise AssertionError("Unexpected network")

    monkeypatch.setattr(socket, "socket", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)
    args = ["compare", str(path), str(path), "--format", format]
    runner = CliRunner()
    default = runner.invoke(app, args)
    audited = runner.invoke(app, args + ["--audit"])
    repeat = runner.invoke(app, args + ["--audit"])
    assert default.exit_code == audited.exit_code == repeat.exit_code == 0
    assert audited.stdout_bytes == repeat.stdout_bytes
    assert path.read_bytes() == before
    if format == "json":
        data = json.loads(audited.stdout)
        assert data.pop("audit")["schema"] == "modlock-audit-0.2-experimental"
        assert data == json.loads(default.stdout)
        assert data["summary"] == {"ambiguous": 2, "separator": 2}
    else:
        assert '"audit"' in audited.stdout and '"audit"' not in default.stdout


def test_empty_and_separator_only_exports_have_no_mod_findings(tmp_path: Path) -> None:
    for rows in ([], json.loads(EXAMPLE.read_text(encoding="utf-8"))[:1]):
        path = tmp_path / "empty.json"
        path.write_text(json.dumps(rows), encoding="utf-8")
        result = audit_export(normalize_export(read_meteoric(path)))
        assert result == {"records": [], "summary": {"mods": 0, "unknown_signals": {}}}
