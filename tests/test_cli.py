"""Exercise the installed CLI contract without modlists or network access."""

import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

from modlock import __version__
from modlock.cli import app

runner = CliRunner()


@pytest.mark.parametrize("arguments", [[], ["--help"]])
def test_help_exits_successfully(arguments: list[str]) -> None:
    result = runner.invoke(app, arguments, env={"NO_COLOR": "1", "TERM": "dumb"})

    assert result.exit_code == 0, result.output
    assert "--help" in result.output
    assert "--version" in result.output
    assert "not available yet" in " ".join(result.output.split())
    assert "--install-completion" not in result.output


def test_version_matches_package_metadata() -> None:
    from importlib.metadata import version

    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0, result.output
    assert result.output.strip() == f"modlock {version('modlock')}"
    assert version("modlock") == __version__
    assert "dev" in __version__


@pytest.mark.parametrize(
    "arguments",
    [
        ["--unknown-option"],
        ["unexpected-argument"],
        ["compare", "old.json", "new.json"],
        ["--version=invalid"],
    ],
)
def test_invalid_arguments_exit_with_usage_error(arguments: list[str]) -> None:
    result = runner.invoke(app, arguments, env={"NO_COLOR": "1", "TERM": "dumb"})

    assert result.exit_code == 2, result.output
    assert "Error" in result.output
    assert "Traceback" not in result.output


def test_module_entry_point_works_outside_the_repository(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "modlock", "--version"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == f"modlock {__version__}"
    assert result.stderr == ""
