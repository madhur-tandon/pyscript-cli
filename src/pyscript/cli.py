"""The main CLI entrypoint and commands."""
from pathlib import Path
from typing import Optional

from pyscript._generator import file_to_html, string_to_html

try:
    import rich_click.typer as typer
except ImportError:
    import typer  # type: ignore
from rich.console import Console

from pyscript import __version__

console = Console()
app = typer.Typer(add_completion=False)


def _print_version():
    console.print(f"PyScript CLI version: {__version__}", style="bold green")


@app.callback(invoke_without_command=True, no_args_is_help=True)
def main(
    version: Optional[bool] = typer.Option(
        None, "--version", help="Show project version and exit."
    )
):
    """Command Line Interface for PyScript."""
    if version:
        _print_version()
        raise typer.Exit()


@app.command()
def version() -> None:
    """Show project version and exit."""
    _print_version()


@app.command()
def wrap(
    input_file: Optional[Path] = typer.Argument(None),
    command: Optional[str] = typer.Option(None, "-c", "--command"),
    output: Optional[Path] = typer.Option(None, "-o"),
) -> None:
    """Wrap a Python script inside an HTML file."""
    if input_file is not None:
        assert command is None
        file_to_html(input_file, output)
        raise typer.Exit()

    if command:
        assert output is not None
        string_to_html(command, output)
