"""Compare two explicit local exports, without overwriting inputs or outputs."""

import sys
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer

from modlock import __version__
from modlock.audit import audit_pair
from modlock.comparison import compare_exports
from modlock.identity import normalize_export
from modlock.meteoric import ReaderError, read_meteoric
from modlock.reports import render_json, render_markdown, report_data

app = typer.Typer(add_completion=False, pretty_exceptions_enable=False)


@app.callback(
    invoke_without_command=True,
    help="Read-only comparison of local Meteoric exports.",
)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool, typer.Option("--version", help="Show the package version and exit.")
    ] = False,
) -> None:
    """Display help when no option is supplied."""
    if version:
        typer.echo(f"modlock {__version__}")
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


class ReportFormat(StrEnum):
    json = "json"
    markdown = "markdown"


@app.command("compare")
def compare(
    base: Path,
    head: Path,
    audit: Annotated[
        bool,
        typer.Option("--audit", help="Include experimental reproducibility signals."),
    ] = False,
    context: Annotated[
        str | None,
        typer.Option(
            help="Assert same game AND export lineage; otherwise all mods stay unresolved."
        ),
    ] = None,
    format: Annotated[
        ReportFormat, typer.Option("--format", help="Report format.")
    ] = ReportFormat.json,
    output: Annotated[
        Path | None,
        typer.Option("--output", "-o", help="New output file only; never overwrite."),
    ] = None,
) -> None:
    """Compare BASE and HEAD read-only; emit JSON or Markdown reports."""
    try:
        old, new = (
            normalize_export(read_meteoric(base)),
            normalize_export(read_meteoric(head)),
        )
        result = compare_exports(old, new, context=context)
        data = report_data(result, old.read_warnings, new.read_warnings)
        if audit:
            data["audit"] = audit_pair(old, new)
        text = (
            render_json(data) if format == ReportFormat.json else render_markdown(data)
        )
        if output is None:
            sys.stdout.buffer.write(text.encode("utf-8"))
            sys.stdout.flush()
        else:
            # Windows exclusive open can follow an existing dangling symlink and
            # create its target. Inspect the directory entry without following it.
            try:
                output.lstat()
            except FileNotFoundError:
                pass
            else:
                raise FileExistsError
            with output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(text)
    except FileExistsError:
        typer.echo("Error: output already exists; choose a new file.", err=True)
        raise typer.Exit(1) from None
    except ReaderError as exc:
        typer.echo(f"Error [{exc.code}]: {exc}", err=True)
        raise typer.Exit(1) from None
    except (OSError, ValueError) as exc:
        message = str(exc) if isinstance(exc, ValueError) else "Unable to write output."
        typer.echo(f"Error: {message}", err=True)
        raise typer.Exit(1) from None
