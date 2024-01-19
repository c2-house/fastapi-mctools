import click
import subprocess
from pathlib import Path


@click.group("run", help="실행 명령어 모음")
def main():
    pass


@main.command(help="uvicorn 실행 command 출력")
def show():
    """
    일일히 터미널에 입력하기 귀찮아서 만든 명령어
    출력되면 복사해서 터미널에 입력하면 됨
    """
    click.echo("uvicorn app.main:app --reload --host 127.0.0.1")


@main.command("dev", help="uvicorn 서버 실행")
def dev():
    main_py = find_main_py()

    if main_py:
        module_path = str(main_py).replace("/", ".").rstrip(".py")
        if module_path.startswith("."):
            module_path = module_path[1:]
        uvicorn_command = [
            "uvicorn",
            f"{module_path}:app",
            "--reload",
            "--host",
            "127.0.0.1",
        ]
        subprocess.run(uvicorn_command)
    else:
        click.echo("main.py 파일을 찾을 수 없습니다.")


def find_main_py():
    """
    현재 디렉토리부터 시작하여 main.py 파일을 찾습니다.
    """
    for path in Path(".").rglob("main.py"):
        return path
    return None
