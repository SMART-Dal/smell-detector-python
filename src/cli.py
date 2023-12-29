import os
from types import SimpleNamespace

import typer

from src.main import main

app = typer.Typer()

__version__ = "1.0.0"


def validate_input_path(input_path):
    if not os.path.exists(input_path):
        typer.echo(f"Error: The specified input path does not exist: {input_path}", err=True)
        raise typer.Exit(code=1)


def confirm_and_update_args(args):
    typer.echo("Current Configuration:")
    typer.echo(f"  Input Path: {args.input}")
    typer.echo(f"  Output Directory: {args.output_dir}")
    typer.echo(f"  Output Format: {args.format}")
    typer.echo(f"  Configuration File: {args.config}")
    typer.echo(f"  Log Directory: {args.log_dir}")

    if typer.confirm("Do you want to update any of these options?"):
        if typer.confirm("Update input path?"):
            args.input = typer.prompt("Enter new input path")
        if typer.confirm("Update output directory?"):
            args.output_dir = typer.prompt("Enter new output directory")
        if typer.confirm("Update output format?"):
            args.format = typer.prompt("Enter new output format")
        if typer.confirm("Update configuration file path?"):
            args.config = typer.prompt("Enter new configuration file path")
        if typer.confirm("Update log directory?"):
            args.log_dir = typer.prompt("Enter new log directory")

    return args


@app.command()
def analyze(
        input_dir: str = typer.Option(..., "--input", "-i",
                                      help="The path to the input Python file or directory for analysis."),
        output_dir: str = typer.Option(..., "--output_dir", "-o",
                                       help="The path to the directory where results will be saved."),
        out_format: str = typer.Option("json", "--format", "-f",
                                       help="The output format for results, e.g., 'json' or 'csv'.",
                                       case_sensitive=False),
        config: str = typer.Option(None, "--config", "-c",
                                   help="The path to a custom configuration file. If not provided, defaults to 'default_config.json' in the script directory."),
        log_dir: str = typer.Option(None, "--log_dir", "-l",
                                    help="The directory to store log files. Defaults to the output directory if not specified.")
):
    """ Analyzes the specified Python project directory for code smells and calculate software metrics. """

    args = SimpleNamespace(
        input=input_dir,
        output_dir=output_dir,
        format=out_format,
        config=config or os.path.join(os.path.dirname(__file__), "default_config.json"),
        log_dir=log_dir or output_dir
    )

    args = confirm_and_update_args(args)

    validate_input_path(args.input)

    try:
        main(args)
    except Exception as e:
        typer.echo(f"An error occurred: {e}", err=True)
        raise typer.Exit(code=1)


@app.command(help="Displays the version of the Python Smell Detector.")
def version():
    typer.echo(f"Python Smell Detector Version {__version__}")


if __name__ == "__main__":
    app()
