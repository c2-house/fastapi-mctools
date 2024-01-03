from typing import ParamSpecKwargs
from fastapi import HTTPException as FastAPIHTTPException, Request, status
from fastapi.responses import JSONResponse


class HTTPException(FastAPIHTTPException):
    """
    Custom HTTPException class
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
        headers: dict = None,
        **kwargs: ParamSpecKwargs,
    ):
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def attributes(self) -> dict:
        attributes = self.__dict__.copy()
        attributes.pop("status_code")
        attributes.pop("headers")
        return attributes


async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """
    HTTPException을 JSONResponse로 변환하여 반환합니다.
    """
    print(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.attributes,
        headers=exc.headers,
    )


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
