import json
import time
from logging import Logger
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse
from starlette.concurrency import iterate_in_threadpool
from fastapi_mctools.exceptions import exception_handler


class RequestLoggingMixin:
    async def make_log_dict(
        self,
        request: Request,
        response: StreamingResponse | None,
        status_code: int,
        tz_location: str = "Asia/Seoul",
        error=None,
    ) -> dict:
        """
        로그 정보를 포함하는 딕셔너리를 생성합니다.

        - request: HTTP 요청 객체
        - response: HTTP 응답 객체
        - status_code: HTTP 상태 코드
        - tz_location: 시간대
        - error: 발생한 에러, 있을 경우

        반환값:
        로그 정보를 포함하는 딕셔너리
        """
        log_dict = {
            "URL": request.url.hostname + request.url.path,
            "Method": request.method,
            "Status-Code": status_code,
            "IP": self.get_ip(request),
            "Error-Message": await self.get_err_msg(response, error),
            "User-Agent": request.headers.get("user-agent", None),
            "Process-Time": str(
                round((time.time() - request.state.start_time) * 1000, 5)
            )
            + "ms",
            "Request-Time": datetime.now(ZoneInfo(tz_location)).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
        return log_dict

    def get_ip(self, request: Request) -> str:
        ip = (
            request.headers["x-forwarded-for"]
            if "x-forwarded-for" in request.headers.keys()
            else request.client.host
        )
        return ip.split(",")[0] if "," in ip else ip

    async def get_err_msg(self, response: StreamingResponse | None, error=None) -> str:
        if error:
            err_msg = error.detail
        else:
            if response.status_code >= 400:
                response_body = [section async for section in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))
                err_msg = response_body[0].decode("utf-8")
                err_msg = json.loads(err_msg)["detail"]
            else:
                return None
        return err_msg

    def get_status_code(self, response, error=None) -> int:
        try:
            if error:
                status_code = error.status_code
            else:
                status_code = response.status_code
        except AttributeError:
            error.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_code = error.status_code
        finally:
            return status_code

    def is_pre_flight(self, request: Request):
        """
        pre-flight 요청인지 확인합니다.
        """
        method = str(request.method)
        if method == "OPTIONS":
            return True
        return False

    def add_addtional_log(self, additional_log: dict, log_dict: dict) -> dict:
        """
        로그 딕셔너리에 추가적인 로그를 추가합니다.

        additional_log: 추가할 로그 딕셔너리
        log_dict: 기존 로그 딕셔너리

        반환값:
        추가된 로그 딕셔너리
        """
        log_dict.update(additional_log)
        return log_dict

    def check_request_header(self, request: Request):
        check = request.headers.get("Authorization", None)
        return check

    def check_allowed_hosts(self, request: Request, allowed_hosts: list[str]) -> bool:
        if request.url.hostname in allowed_hosts:
            return True
        return False


class RequestLoggingMiddleware(BaseHTTPMiddleware, RequestLoggingMixin):
    """
    Request 로깅 미들웨어
    - FastAPI 앱에 추가하여 사용합니다.
    - 요청과 응답에 대한 로그를 기록합니다.
    """

    def __init__(
        self,
        app: FastAPI,
        logger: Logger,
        health_check_path: str | None = None,
        tz_location: str = "Asia/Seoul",
        allowed_hosts: list[str] = None,
        additional_log: dict = None,
    ) -> None:
        self.logger = logger
        self.health_check_path = health_check_path
        self.tz_location = tz_location
        self.allowed_hosts = allowed_hosts
        self.additional_log = additional_log
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        is_pre_flight = self.is_pre_flight(request)
        is_allowed_hosts = (
            self.check_allowed_hosts(request, self.allowed_hosts)
            if self.allowed_hosts
            else None
        )
        is_health_check_pass = False if not self.health_check_path else True
        pass_case = (is_pre_flight, is_allowed_hosts, is_health_check_pass)

        match pass_case:
            case (True, False, False):
                response = await call_next(request)
                return response

        return await self.process_log(request, call_next)

    async def process_log(self, request: Request, call_next):
        try:
            request.state.start_time = time.time()
            response = await call_next(request)
            status_code = self.get_status_code(response)
            log_dict = await self.get_log_dict(
                request, response, status_code, additional_log=self.additional_log
            )
        except Exception as e:
            # 500이상 에러 발생시
            e = await exception_handler(e)
            status_code = self.get_status_code(None, e)
            log_dict = await self.get_log_dict(
                request, None, status_code, e, additional_log=self.additional_log
            )
            log_str = ", ".join(f"{key}: {value}" for key, value in log_dict.items())
            self.logger.error(log_str)
            return JSONResponse(content={"detail": e.detail}, status_code=e.status_code)
        else:
            log_str = ", ".join(f"{key}: {value}" for key, value in log_dict.items())
            self.logger.info(log_str)
            return response

    async def get_log_dict(
        self,
        request: Request,
        response: StreamingResponse | None,
        status_code: int,
        error=None,
        additional_log: dict = None,
    ):
        log_dict = await self.make_log_dict(
            request, response, status_code, self.tz_location, error
        )
        if additional_log:
            log_dict = self.add_addtional_log(additional_log, log_dict)
        return log_dict
