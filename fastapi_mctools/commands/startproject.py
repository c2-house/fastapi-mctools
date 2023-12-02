import os
import shutil
import subprocess

TEMPLATE_PATH = "fastapi_mctools/commands/_templates/"


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

    shutil.copy(TEMPLATE_PATH + "settings.py-tpl", "./app/config/settings.py")
    shutil.copy(TEMPLATE_PATH + "main.py-tpl", "./app/main.py")
    shutil.copy(TEMPLATE_PATH + "routers.py-tpl", "./app/routers/routers.py")
    shutil.copy(TEMPLATE_PATH + "async_session.py-tpl", "./app/db/async_session.py")
    shutil.copy(TEMPLATE_PATH + "session.py-tpl", "./app/db/session.py")
    shutil.copy(TEMPLATE_PATH + "sqlalchemy_base.py-tpl", "./app/models/base.py")
    shutil.copy(TEMPLATE_PATH + "gitignore-tpl", "./.gitignore")
    shutil.copy(TEMPLATE_PATH + "pre-commit-tpl", "./.pre-commit-config.yaml")


if __name__ == "__main__":
    main()
