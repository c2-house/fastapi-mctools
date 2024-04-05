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
            "./app/",
            "./app/config/",
            "./app/routes/",
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
        "config/settings.py",
        "main.py",
        "routes/routers.py",
        "db/async_session.py",
        "db/session.py",
        "models/base.py",
        ".gitignore",
        ".pre-commit-config.yaml",
    ]

    for template, file in zip(TEMPLATES, FILES):
        with resources.path(TEMPLATE_PATH, template) as template_path:
            if file in [".gitignore", ".pre-commit-config.yaml"]:
                shutil.copy(str(template_path), "./" + file)
            else:
                shutil.copy(str(template_path), "./app/" + file)
