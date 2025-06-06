import click
import subprocess
from pathlib import Path


@click.group("run", help="실행 명령어 모음")
def main():
    pass


@main.command("dev", help="uvicorn 서버 실행")
@click.option("--host", default="127.0.0.1", help="서버 호스트 주소")
@click.option("--port", default=8000, help="서버 포트 번호")
def dev(port: int, host: str):
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
            host,
            "--port",
            str(port),
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


@main.command("prod", help="gunicorn 서버 실행")
def prod():
    def run_gunicorn():
        gunicorn_config = find_gunicorn_config()

        if gunicorn_config:
            gunicorn_command = ["gunicorn", "-c", str(gunicorn_config)]
            subprocess.run(gunicorn_command)
        else:
            # when gunicorn_config not found, make it by mct gunicorn
            subprocess.run(["mct", "gunicorn"])
            run_gunicorn()

    run_gunicorn()


def find_gunicorn_config():
    """
    현재 디렉토리부터 시작하여 gunicorn.config.py 파일을 찾습니다.
    """
    for path in Path(".").rglob("gunicorn.config.py"):
        return path
    return None
