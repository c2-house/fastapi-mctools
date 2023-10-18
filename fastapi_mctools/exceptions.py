from fastapi import HTTPException as FastAPIHTTPException, status


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


async def exception_handler(error: Exception) -> HTTPException:
    """
    Exception을 HTTPException으로 변환하여 HTTP 상태 코드와 에러 메시지를 반환합니다.
    """
    if not isinstance(error, HTTPException):
        error = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
            code="INTERNAL_SERVER_ERROR",
        )
    return error
