import click
import shutil
from importlib import resources


@click.command("gunicorn", help="gunicorn config 생성")
def main():
    """
    배포할 때 사용할 gunicorn config 파일 매번 만들기 귀찮아서 만든 명령어
    """
    TEMPLATE_PATH = "fastapi_mctools.commands._templates"
    TEMPLATE = "gunicorn.config.py-tpl"
    FILE = "gunicorn.config.py"

    with resources.path(TEMPLATE_PATH, TEMPLATE) as template_path:
        shutil.copy(str(template_path), "./app/" + FILE)
