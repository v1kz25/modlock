"""Saved exports are sufficient snapshots: exercise real installed CLI processes."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from modlock.meteoric import DEFAULT_MAX_BYTES

ROOT = Path(__file__).resolve().parents[1]


def invoke(cwd: Path, *arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "modlock", "compare", *arguments],
        cwd=cwd,
        capture_output=True,
        check=False,
    )


def save_pair(tmp_path: Path) -> tuple[Path, Path]:
    directory = tmp_path / "Café snapshots con espacios"
    directory.mkdir()
    paths = directory / "antes.json", directory / "después.json"
    for name, path in zip(("base", "head"), paths, strict=True):
        data = json.loads((ROOT / f"examples/{name}.json").read_text(encoding="utf-8"))
        data[1]["modName"] = data[1]["displayName"] = "Café 日本語"
        data[1]["general"]["installationFile"] = "NO-ABRIR/archivo-privado.zip"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8-sig")
    return paths


@pytest.mark.parametrize("format", ["json", "markdown"])
@pytest.mark.parametrize("audit", [False, True])
def test_saved_snapshots_are_repeatable_from_another_directory(
    tmp_path: Path, format: str, audit: bool
) -> None:
    paths = save_pair(tmp_path)
    hashes = [hashlib.sha256(p.read_bytes()).digest() for p in paths]
    args = [
        *(str(p) for p in paths),
        "--context",
        "synthetic:saved",
        "--format",
        format,
    ]
    if audit:
        args.append("--audit")
    first, second = invoke(tmp_path, *args), invoke(tmp_path, *args)
    assert first.returncode == second.returncode == 0, first.stderr
    assert first.stdout == second.stdout
    assert not first.stderr and not second.stderr
    assert str(tmp_path).encode() not in first.stdout
    assert [hashlib.sha256(p.read_bytes()).digest() for p in paths] == hashes
    if format == "json":
        report = json.loads(first.stdout)
        assert report["summary"] == {"modified": 1, "separator": 2}
        change = next(c for c in report["changes"] if c["category"] == "modified")
        assert (
            change["base"]["data"]
            == json.loads(paths[0].read_bytes().decode("utf-8-sig"))[1]
        )
        assert (
            change["head"]["data"]
            == json.loads(paths[1].read_bytes().decode("utf-8-sig"))[1]
        )
        assert ("audit" in report) == audit


def test_reversing_snapshots_exchanges_payloads_and_add_remove(tmp_path: Path) -> None:
    old, new = save_pair(tmp_path)
    row = json.loads(new.read_bytes().decode("utf-8-sig"))[1]
    row.update(id=999, modName="Different", displayName="Different", order=2)
    row["general"]["modid"] = "999"
    row["installed"]["files"] = [{"modid": "999", "fileid": "9991"}]
    data = json.loads(new.read_bytes().decode("utf-8-sig")) + [row]
    new.write_text(json.dumps(data), encoding="utf-8")
    forward = invoke(tmp_path, str(old), str(new), "--context", "synthetic:saved")
    reverse = invoke(tmp_path, str(new), str(old), "--context", "synthetic:saved")
    assert forward.returncode == reverse.returncode == 0
    a, b = json.loads(forward.stdout), json.loads(reverse.stdout)
    assert a["summary"] == {"added": 1, "modified": 1, "separator": 2}
    assert b["summary"] == {"removed": 1, "modified": 1, "separator": 2}
    left = next(c for c in a["changes"] if c["category"] == "modified")
    right = next(c for c in b["changes"] if c["category"] == "modified")
    assert left["base"] == right["head"] and left["head"] == right["base"]
    assert left["fields"] == right["fields"] == ["active", "version"]


@pytest.mark.parametrize("error", ["missing", "malformed", "too_large"])
def test_snapshot_errors_preserve_other_input_and_do_not_create_report(
    tmp_path: Path, error: str
) -> None:
    old, new = save_pair(tmp_path)
    if error == "missing":
        old.unlink()
    elif error == "malformed":
        old.write_bytes(b"{invalid")
    else:
        old.write_bytes(b" " * (DEFAULT_MAX_BYTES + 1))
    before = new.read_bytes()
    output = tmp_path / "report.json"
    result = invoke(tmp_path, str(old), str(new), "--audit", "--output", str(output))
    assert result.returncode == 1
    assert b"Error" in result.stderr and b"Traceback" not in result.stderr
    assert new.read_bytes() == before
    assert not output.exists()
