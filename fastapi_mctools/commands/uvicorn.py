import click


@click.command("uvicorn", help="uvicorn 실행 command 출력")
def main():
    """
    일일히 터미널에 입력하기 귀찮아서 만든 명령어
    출력되면 복사해서 터미널에 입력하면 됨
    """
    click.echo("uvicorn app.main:app --reload --host 127.0.0.1")
