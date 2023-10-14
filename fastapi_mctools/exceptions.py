from fastapi import HTTPException as FastAPIHTTPException


class HTTPException(FastAPIHTTPException):
    """
    Custom HTTPException class to add a code field to the response.
    ...
    raise HTTPException(
        status_code=404,
        detail="Item not found",
        code="NOT_FOOUND",
    )
    """

    def __init__(
        self,
        status_code: int,
        detail: str = None,
        code: str = None,
        headers: dict = None,
    ):
        super().__init__(status_code, detail, headers)
        self.code = code
