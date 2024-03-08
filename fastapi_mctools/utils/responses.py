import json
from typing import Union

ResultType = Union[dict, list[dict], list, str]


class ResponseInterFace:
    """
    Represents a response interface.

    Attributes:
        result (ResultType): The result of the response.
        kwargs (dict): Additional keyword arguments for the response.

    Methods:
        to_dict(): Converts the response to a dictionary.
        to_str(): Converts the response to a string.
    """

    def __init__(self, result: ResultType, **kwargs) -> None:
        self.result = result
        self.kwargs = kwargs

    def to_dict(self) -> dict:
        """
        Converts the response to a dictionary.

        Returns:
            dict: The response as a dictionary.
        """
        return {**self.kwargs, "result": self.result}

    def to_str(self) -> str:
        """
        Converts the response to a string.

        Returns:
            str: The response as a string.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False)

    def __getitem__(self, key: str) -> Union[ResultType, str]:
        return self.to_dict()[key]

    def __iter__(self):
        return iter(self.to_dict())

    def keys(self):
        return self.to_dict().keys()

    def items(self):
        return self.to_dict().items()
