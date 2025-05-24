import httpx
import warnings
from typing import (
    Callable,
    Any,
    Coroutine,
    TypeVar,
    Union,
    ParamSpecArgs,
    ParamSpecKwargs,
)
from functools import wraps

T = TypeVar("T", bound="APIClient")
P = Union[ParamSpecArgs, ParamSpecKwargs]


def ensure_session(
    func: Callable[..., Coroutine[Any, Any, httpx.Response]],
) -> Callable[..., Coroutine[Any, Any, httpx.Response]]:
    @wraps(func)
    async def wrapper(self: T, *args: P, **kwargs: P) -> httpx.Response:
        if self.session is None:
            raise RuntimeError("세션이 시작되지 않았습니다. start() 메소드를 호출하세요.")
        return await func(self, *args, **kwargs)

    return wrapper


class APIClient:
    """
    APIClient is a class that wraps httpx.AsyncClient.
    It uses a single session, created through the start() method.
    The session is closed using the close() method.

    Usage:
        api_client = APIClient()
        await api_client.start()
        async def get_example_1(api_client: APIClient):
            response = await api_client.get("https://example.com")
            return response

        async def get_example_2(api_client: APIClient):
            response = await api_client.get("https://example.com")
            return response

        response_1, response_2 = await asyncio.gather(
            get_example_1(api_client),
            get_example_2(api_client)
        )
        await api_client.close()
    """

    def __init__(self) -> None:
        self.session = None

    async def start(self) -> None:
        if not self.session:
            self.session = httpx.AsyncClient()

    async def close(self) -> None:
        if self.session:
            await self.session.aclose()
            self.session = None

    @ensure_session
    async def get(self, url: str, params: dict[str, Any] | None = None, **kwargs: P) -> httpx.Response:
        response = await self.session.get(url, params=params, **kwargs)
        return response

    @ensure_session
    async def post(self, url: str, json: dict[str, Any] | None = None, **kwargs: P) -> httpx.Response:
        response = await self.session.post(url, json=json, **kwargs)
        return response

    @ensure_session
    async def put(self, url: str, json: dict[str, Any] | None = None, **kwargs: P) -> httpx.Response:
        response = await self.session.put(url, json=json, **kwargs)
        return response

    @ensure_session
    async def patch(self, url: str, json: dict[str, Any] | None = None, **kwargs: P) -> httpx.Response:
        response = await self.session.patch(url, json=json, **kwargs)
        return response

    def __del__(self) -> None:
        if self.session and not self.session.closed:
            warnings.warn("APIClient 객체가 close되지 않았습니다.")
