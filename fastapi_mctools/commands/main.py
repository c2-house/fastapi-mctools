import click
from fastapi_mctools.commands.startproject import main as startproject_main


@click.group()
@click.version_option()
def cli():
    pass


def run_main():
    cli.add_command(startproject_main)
    cli(prog_name="fastapi-mctools")


if __name__ == "__main__":
    run_main()
