"""Offline package-content, runtime-closure and repeatable-build checks."""

import configparser
import hashlib
import importlib.metadata
import zipfile
from email.parser import BytesParser
from pathlib import Path

import pytest
from flit_core import buildapi
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

from modlock import __version__

ROOT = Path(__file__).resolve().parents[1]


def build(target: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    target.mkdir()
    monkeypatch.chdir(ROOT)
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "315532800")
    return target / buildapi.build_wheel(str(target))


def test_wheel_contains_complete_package_and_own_license_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    wheel = build(tmp_path / "wheel", monkeypatch)
    prefix = f"modlock-{__version__}.dist-info/"
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        assert all(name.startswith(("modlock/", prefix)) for name in names)
        source = {
            p.relative_to(ROOT / "src").as_posix()
            for p in (ROOT / "src/modlock").rglob("*.py")
        }
        assert {name for name in names if name.endswith(".py")} == source
        for name in source:
            assert archive.read(name) == (ROOT / "src" / name).read_bytes()
        for license_name in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
            assert (
                archive.read(prefix + "licenses/" + license_name)
                == (ROOT / license_name).read_bytes()
            )
        metadata = BytesParser().parsebytes(archive.read(prefix + "METADATA"))
        assert metadata["Version"] == __version__
        assert metadata["License-Expression"] == "MIT"
        assert metadata["Requires-Python"] == ">=3.12,<3.13"
        runtime = [
            Requirement(value) for value in metadata.get_all("Requires-Dist", [])
        ]
        active = [
            req
            for req in runtime
            if req.marker is None or req.marker.evaluate({"extra": ""})
        ]
        assert [str(req) for req in active] == ["typer==0.29.2"]
        entry = configparser.ConfigParser()
        entry.read_string(archive.read(prefix + "entry_points.txt").decode())
        assert entry["console_scripts"]["modlock"] == "modlock.cli:app"


def test_runtime_lock_is_complete_and_does_not_require_development_tools() -> None:
    locked = {}
    for line in (ROOT / "requirements-runtime.txt").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        requirement, checksum = line.split(" --hash=sha256:")
        name, version = requirement.split("==")
        assert len(checksum) == 64 and int(checksum, 16) >= 0
        locked[canonicalize_name(name)] = version
    visited, pending = set(), [Requirement("typer==0.29.2")]
    while pending:
        requirement = pending.pop()
        name = canonicalize_name(requirement.name)
        assert name in locked and locked[name] in requirement.specifier
        assert importlib.metadata.version(name) == locked[name]
        if name in visited:
            continue
        visited.add(name)
        for value in importlib.metadata.requires(name) or []:
            child = Requirement(value)
            if child.marker is None or child.marker.evaluate({"extra": ""}):
                pending.append(child)
    assert visited == set(locked)
    assert not visited.intersection({"pytest", "ruff", "mypy", "flit-core"})


def test_offline_wheel_build_is_byte_repeatable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first = build(tmp_path / "first", monkeypatch)
    second = build(tmp_path / "second", monkeypatch)
    assert (
        hashlib.sha256(first.read_bytes()).digest()
        == hashlib.sha256(second.read_bytes()).digest()
    )
