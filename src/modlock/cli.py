"""Help and development version for the initial CLI setup."""

from typing import Annotated

import typer

from modlock import __version__

app = typer.Typer(add_completion=False)


@app.command(
    help="modlock: initial CLI setup. Export reading and auditing are not available yet.",
)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool, typer.Option("--version", help="Show the development version and exit.")
    ] = False,
) -> None:
    """Display setup help when no option is supplied."""
    if version:
        typer.echo(f"modlock {__version__}")
    else:
        typer.echo(ctx.get_help())
