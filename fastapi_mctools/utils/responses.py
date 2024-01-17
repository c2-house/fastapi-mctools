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
