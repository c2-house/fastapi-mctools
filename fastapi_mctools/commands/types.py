import ast
import os
import click

Hint = tuple[str, str]
HintDict = dict[str, list[Hint]]

SELF = {"self", "cls"}


class TypeHintChecker(ast.NodeVisitor):
    def __init__(self):
        self.missing_type_hints = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for arg in node.args.args:
            if arg.annotation is None and arg.arg not in SELF:
                self.missing_type_hints.append((node.name, arg.arg))

        if node.returns is None:
            self.missing_type_hints.append((node.name, "return"))

        self.generic_visit(node)


def check_file_for_type_hints(filename: str) -> list[Hint]:
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
        checker = TypeHintChecker()
        checker.visit(tree)
        return checker.missing_type_hints


def check_directory_for_type_hints(directory: str) -> HintDict:
    missing_type_hints = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                file_hints = check_file_for_type_hints(full_path)
                if file_hints:
                    missing_type_hints[full_path] = file_hints
    return missing_type_hints


@click.command("types", help="타입 힌트 안빠트렸는지 검사")
@click.argument("path", type=click.Path(exists=True))
def main(path):
    if os.path.isdir(path):
        missing_hints = check_directory_for_type_hints(path)
        if missing_hints:
            click.echo("Type Hint 빼먹음 :")
            for file, hints in missing_hints.items():
                click.echo(f"In {file}:")
                for func, arg in hints:
                    click.echo(f"  Function '{func}' 타입힌트가 없습니다. -> '{arg}'")
        else:
            click.echo("타입힌트를 빼먹지 않았습니다.")
    else:
        missing_hints = check_file_for_type_hints(path)
        if missing_hints:
            click.echo("Type Hint 빼먹음 :")
            click.echo(f"In {path}:")
            for func, arg in missing_hints:
                click.echo(f"  Function '{func}' 타입힌트가 없습니다. -> '{arg}'")
        else:
            click.echo("타입힌트를 빼먹지 않았습니다.")
