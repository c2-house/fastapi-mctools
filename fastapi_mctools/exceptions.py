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
        super().__init__(status_code, detail, headers)
        for key, value in kwargs.items():
            setattr(self, key, value)        

    @property
    def attributes(self) -> dict:
        self.__dict__.pop("status_code")
        self.__dict__.pop("headers")
        return self.__dict__


async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """
    HTTPException을 JSONResponse로 변환하여 반환합니다.
    """
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
