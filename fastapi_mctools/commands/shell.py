import click


class InteractiveShellLauncher:
    """
    This is for launching an interactive shell.
    Inspired by Django's `shell` command.
    when needed to run orm queries separately. use this command.
    """

    def start_ipython(self):
        try:
            from IPython import start_ipython
            from traitlets.config import Config
        except ImportError:
            raise ImportError("IPython is not installed. Please install it to use this feature.")
        c = Config()
        c.InteractiveShell.banner1 = "Welcome to your interactive shell"
        start_ipython(argv=[], config=c)


@click.command("shell", help="Launches an interactive shell")
def main():
    """Launches an interactive shell"""
    launcher = InteractiveShellLauncher()
    launcher.start_ipython()
