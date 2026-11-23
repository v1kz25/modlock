"""Native filesystem cases; real symlinks are mandatory in Windows CI."""

import json
import os
import stat
from pathlib import Path

import pytest
from typer.testing import CliRunner

from modlock.cli import app

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/base.json"


def saved(tmp_path: Path) -> Path:
    path = tmp_path / "Café entrada [x].json"
    path.write_bytes(EXAMPLE.read_bytes())
    return path


def link_to(target: Path, link: Path) -> None:
    try:
        link.symlink_to(target)
    except OSError as exc:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            pytest.fail(
                f"CI must exercise real symlinks, not skip them (errno={exc.errno})"
            )
        pytest.skip(
            f"Native symlink unavailable; winerror={getattr(exc, 'winerror', None)}"
        )


def compare(base: Path, head: Path, *args: str):
    return CliRunner().invoke(
        app,
        [
            "compare",
            str(base),
            str(head),
            "--context",
            "synthetic:safety",
            "--audit",
            *args,
        ],
    )


def test_input_symlink_reads_regular_target_without_mutation(tmp_path: Path) -> None:
    target = saved(tmp_path)
    link = tmp_path / "input-link.json"
    link_to(target, link)
    before = target.read_bytes()
    result = compare(link, target)
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout)["summary"] == {"separator": 2, "unchanged": 1}
    assert link.is_symlink() and target.read_bytes() == before


@pytest.mark.parametrize("dangling", [False, True])
def test_output_symlink_never_changes_or_creates_target(
    tmp_path: Path, dangling: bool
) -> None:
    source = saved(tmp_path)
    target = tmp_path / "must-not-change.txt"
    if not dangling:
        target.write_bytes(b"synthetic sentinel")
    link = tmp_path / "output-link.json"
    link_to(target, link)
    result = compare(source, source, "--output", str(link))
    assert result.exit_code == 1, result.output
    assert link.is_symlink()
    assert (
        target.read_bytes() == b"synthetic sentinel"
        if not dangling
        else not target.exists()
    )


def test_dangling_input_is_error_without_creating_target(tmp_path: Path) -> None:
    source = saved(tmp_path)
    target = tmp_path / "absent.json"
    link = tmp_path / "dangling-input.json"
    link_to(target, link)
    result = compare(link, source)
    assert result.exit_code == 1 and "Error" in result.stderr
    assert not target.exists() and link.is_symlink()


def test_native_hardlink_input_and_output_preserve_original(tmp_path: Path) -> None:
    source = saved(tmp_path)
    linked = tmp_path / "hardlink.json"
    linked.hardlink_to(source)
    before = source.read_bytes()
    assert compare(linked, source).exit_code == 0
    assert compare(source, source, "--output", str(linked)).exit_code == 1
    assert source.read_bytes() == linked.read_bytes() == before


def test_readonly_file_attribute_requires_no_write_access(tmp_path: Path) -> None:
    source = saved(tmp_path)
    mode = source.stat().st_mode
    source.chmod(stat.S_IREAD)
    try:
        before = source.read_bytes()
        assert compare(source, source).exit_code == 0
        assert source.read_bytes() == before
    finally:
        source.chmod(mode)


def test_audited_cli_opens_only_explicit_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = saved(tmp_path)
    untouched = tmp_path / "private-synthetic-placeholder.zip"
    untouched.write_bytes(b"not mod content")
    rows = json.loads(source.read_bytes())
    rows[1]["general"]["installationFile"] = str(untouched)
    source.write_text(json.dumps(rows), encoding="utf-8")
    opened = []
    original = Path.open

    def tracked(path, mode="r", *args, **kwargs):
        opened.append((path, mode))
        assert path == source and mode == "rb"
        return original(path, mode, *args, **kwargs)

    with monkeypatch.context() as context:
        context.setattr(Path, "open", tracked)
        result = compare(source, source)
    assert result.exit_code == 0, result.output
    assert opened == [(source, "rb"), (source, "rb")]
    assert untouched.read_bytes() == b"not mod content"


@pytest.mark.parametrize(
    "content", [b"+Local mod\r\n-Disabled mod\r\n", b"PK\x03\x04not an export", b"{}"]
)
def test_other_shapes_fail_without_creating_output(
    tmp_path: Path, content: bytes
) -> None:
    source = saved(tmp_path)
    foreign = tmp_path / "unsupported.data"
    foreign.write_bytes(content)
    output = tmp_path / "report.json"
    result = compare(foreign, source, "--output", str(output))
    assert result.exit_code == 1 and "Traceback" not in result.output
    assert not output.exists() and foreign.read_bytes() == content
    assert source.read_bytes() == EXAMPLE.read_bytes()


def test_directory_input_is_not_a_regular_export(tmp_path: Path) -> None:
    source = saved(tmp_path)
    result = compare(tmp_path, source)
    assert result.exit_code == 1 and "file_type" in result.stderr
