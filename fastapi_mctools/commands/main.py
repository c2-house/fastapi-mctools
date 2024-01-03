import click
from fastapi_mctools.commands.startproject import main as startproject_main
from fastapi_mctools.commands.gunicorn import main as gunicorn_main
from fastapi_mctools.commands.uvicorn import main as uvicorn_main
from fastapi_mctools.commands.types import main as types_main


@click.group()
@click.version_option()
def cli():
    pass


def run_main():
    cli.add_command(startproject_main)
    cli.add_command(gunicorn_main)
    cli.add_command(uvicorn_main)
    cli.add_command(types_main)
    cli(prog_name="fastapi-mctools")


if __name__ == "__main__":
    run_main()
