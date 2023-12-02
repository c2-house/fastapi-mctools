import os
import shutil
import click
import subprocess
from importlib import resources


@click.command("startproject", help="프로젝트 생성")
def main():
    def check_path(paths: list[str]):
        for path in paths:
            dir_path = os.path.dirname(path)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                subprocess.run(["touch", dir_path + "/__init__.py"])

    check_path(
        [
            "./app/config/",
            "./app/routers/",
            "./app/db/",
            "./app/models/",
            "./app/schemas/",
            "./app/orms/",
        ]
    )
    TEMPLATE_PATH = "fastapi_mctools.commands._templates"
    TEMPLATES = [
        "settings.py-tpl",
        "main.py-tpl",
        "routers.py-tpl",
        "async_session.py-tpl",
        "session.py-tpl",
        "sqlalchemy_base.py-tpl",
        "gitignore-tpl",
        "pre-commit-tpl",
    ]
    FILES = [
        "settings.py",
        "main.py",
        "routers.py",
        "async_session.py",
        "session.py",
        "base.py",
        ".gitignore",
        ".pre-commit-config.yaml",
    ]

    for template, file in zip(TEMPLATES, FILES):
        with resources.path(TEMPLATE_PATH, template) as template_path:
            shutil.copy(str(template_path), "./app/" + file)
