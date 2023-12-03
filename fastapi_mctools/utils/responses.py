import json
from typing import Union

ResultType = Union[dict, list[dict], list, str]


class ResponseInterFace:
    """
    Response 통일을 위한 인터페이스입니다.
    """

    def __init__(self, result: ResultType, **kwargs) -> None:
        self.result = result
        self.kwargs = kwargs

    def to_dict(self) -> dict:
        return {**self.kwargs, "result": self.result}

    def to_str(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)
