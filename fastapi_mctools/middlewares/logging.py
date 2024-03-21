import os
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
from fastapi_mctools.exceptions import handle_500_exception


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
        Creates a dictionary containing log information.

        - request: HTTP request object
        - response: HTTP response object
        - status_code: HTTP status code
        - tz_location: Time zone
        - error: Occurred error, if any

        Return:
        A dictionary containing log information
        """
        log_dict = {
            "URL": self.get_url(request),
            "Method": request.method,
            "Status-Code": status_code,
            "IP": self.get_ip(request),
            "PID": os.getpid(),
            "Error-Message": await self.get_err_msg(response, error),
            "User-Agent": request.headers.get("user-agent", None),
            "Process-Time": str(round((time.time() - request.state.start_time) * 1000, 5)) + "ms",
            "Request-Time": datetime.now(ZoneInfo(tz_location)).strftime("%Y-%m-%d %H:%M:%S"),
        }
        return log_dict

    def get_url(self, request: Request) -> str:
        """
        Get the URL of the request.
        """
        scheme = request.url.scheme
        if request.query_params:
            params = request.query_params._dict
            params_str = "&".join(f"{key}={value}" for key, value in params.items())
            url = f"{scheme}://{request.url.hostname}{request.url.path}?{params_str}"
        else:
            url = f"{scheme}://{request.url.hostname}{request.url.path}"
        return url

    def get_ip(self, request: Request) -> str:
        ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
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
        """
        get status code from response or error.
        """
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
        check if the request is pre-flight request.
        """
        method = str(request.method)
        if method == "OPTIONS":
            return True
        return False

    def add_addtional_log(self, additional_log: dict, log_dict: dict) -> dict:
        """
        Add additional logs to the log dictionary.

        additional_log: log dictionary to add
        log_dict: existing log dictionary

        Return:
        Added Log Dictionary
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
    Request Logging Middleware
    - Add to FastAPI app to use.
    - Logs requests and responses.
    - You can skip health check requests by setting health_check_path.
    - If you set allowed_hosts, only requests from allowed_hosts will be logged.
    """

    def __init__(
        self,
        app: FastAPI,
        logger: Logger,
        health_check_path: str | None = None,
        tz_location: str = "Asia/Seoul",
        allowed_hosts: list[str] | None = None,
    ) -> None:
        self.logger = logger
        self.health_check_path = health_check_path
        self.tz_location = tz_location
        self.allowed_hosts = allowed_hosts
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        is_pre_flight = self.is_pre_flight(request)
        is_allowed_hosts = self.check_allowed_hosts(request, self.allowed_hosts) if self.allowed_hosts else None
        is_health_check_pass = self.health_check_path == request.url.path
        pass_case = (is_pre_flight, is_health_check_pass)

        if any(pass_case):
            return await call_next(request)

        if is_allowed_hosts is False:
            return await call_next(request)

        return await self.process_log(request, call_next)

    async def process_log(self, request: Request, call_next):
        try:
            request.state.start_time = time.time()
            response = await call_next(request)
            status_code = self.get_status_code(response)
            log_dict = await self.get_log_dict(request, response, status_code)
        except Exception as e:
            # 500이상 에러 발생시
            e = await handle_500_exception(e)
            status_code = self.get_status_code(None, e)
            log_dict = await self.get_log_dict(request, None, status_code, e)
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
    ):
        log_dict = await self.make_log_dict(request, response, status_code, self.tz_location, error)
        return log_dict
