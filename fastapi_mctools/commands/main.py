import click
from fastapi_mctools.commands.startproject import main as startproject_main
from fastapi_mctools.commands.gunicorn import main as gunicorn_main
from fastapi_mctools.commands.run import main as run_main
from fastapi_mctools.commands.types import main as types_main
from fastapi_mctools.commands.shell import main as shell_main


@click.group()
@click.version_option()
def cli():
    pass


def command_main():
    cli.add_command(startproject_main)
    cli.add_command(gunicorn_main)
    cli.add_command(run_main)
    cli.add_command(types_main)
    cli.add_command(shell_main)
    cli(prog_name="fastapi-mctools")


if __name__ == "__main__":
    command_main()
