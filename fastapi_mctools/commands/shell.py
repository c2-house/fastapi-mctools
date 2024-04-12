import click
import importlib
import asyncio


@click.group("shell", help="터미널 실행")
def main():
    pass


class InteractiveShellLauncher:
    def __init__(self, session_var_name, session_type, module_path):
        self.session_var_name = session_var_name
        self.session_type = session_type
        self.module_path = module_path

    async def launch_async_shell(self):
        module = importlib.import_module(self.module_path)
        get_session = getattr(module, self.session_var_name)
        async with get_session() as session:
            self.start_ipython({"session": session})

    def launch_sync_shell(self):
        module = importlib.import_module(self.module_path)
        get_session = getattr(module, self.session_var_name)
        session = get_session()
        try:
            self.start_ipython({"session": session})
        finally:
            session.close()

    def start_ipython(self, user_ns):
        try:
            from IPython import start_ipython
            from traitlets.config import Config
        except ImportError:
            raise ImportError("IPython is not installed. Please install it to use this feature.")

        c = Config()
        if self.session_type == "async":
            c.InteractiveShell.banner1 = "Welcome to your interactive shell with async database session!"
        else:
            c.InteractiveShell.banner1 = "Welcome to your interactive shell with sync database session!"

        start_ipython(argv=[], user_ns=user_ns, config=c)


@main.command()
@click.option("--session-var-name", default="get_db", help="The variable name of the session.")
@click.option(
    "--session-type",
    type=click.Choice(["async", "sync"], case_sensitive=False),
    default="async",
    help="Type of the SQLAlchemy session (async or sync).",
)
@click.option(
    "--module-path",
    required=True,
    help="Path to the module where the session is defined.",
)
def shell(session_var_name, session_type, module_path):
    """Launches an interactive shell with database session."""
    launcher = InteractiveShellLauncher(session_var_name, session_type, module_path)
    if session_type == "async":
        asyncio.run(launcher.launch_async_shell())
    else:
        launcher.launch_sync_shell()
