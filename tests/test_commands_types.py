import os
import ast
from click.testing import CliRunner
from fastapi_mctools.commands.types import TypeHintChecker, main

DUMMY_CODE = """
def function_with_hints(a: int, b: str) -> bool:
    return True

def function_without_hints(a, b):
    return True


class class_without_hints:
    def method_with_hints(self, a: int, b: str) -> bool:
        return True

    def method_without_hints(self, a, b):
        return True
"""


def test_type_hint_checker():
    tree = ast.parse(DUMMY_CODE)
    checker = TypeHintChecker()
    checker.visit(tree)

    assert len(checker.missing_type_hints) == 6
    assert ("function_without_hints", "return") in checker.missing_type_hints
    assert ("function_without_hints", "a") in checker.missing_type_hints
    assert ("function_without_hints", "b") in checker.missing_type_hints
    assert ("method_without_hints", "return") in checker.missing_type_hints
    assert ("method_without_hints", "a") in checker.missing_type_hints
    assert ("method_without_hints", "b") in checker.missing_type_hints


def test_cli_with_directory():
    runner = CliRunner()
    with runner.isolated_filesystem():
        os.mkdir("test_dir")

        # test_dir 내에 Python 파일 생성
        with open("test_dir/test_file1.py", "w") as f:
            f.write(
                """
def function_with_hints(a: int, b: str) -> bool:
    return True

def function_without_hints(a, b):
    return True
"""
            )

        with open("test_dir/test_file2.py", "w") as f:
            f.write(
                """
def another_function(x: int) -> None:
    pass
"""
            )

        result = runner.invoke(main, ["test_dir"])
        assert result.exit_code == 0
        assert "타입힌트를 빼먹지 않았습니다." in result.output or "Type Hint 빼먹음 :" in result.output
