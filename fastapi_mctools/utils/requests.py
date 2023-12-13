import httpx
import warnings
from typing import Callable, Any, Coroutine, TypeVar
from functools import wraps

T = TypeVar("T", bound="APIClient")


def ensure_session(
    func: Callable[..., Coroutine[Any, Any, httpx.Response]]
) -> Callable[..., Coroutine[Any, Any, httpx.Response]]:
    @wraps(func)
    async def wrapper(self: T, *args: Any, **kwargs: Any) -> httpx.Response:
        if self.session is None:
            raise RuntimeError("세션이 시작되지 않았습니다. start() 메소드를 호출하세요.")
        return await func(self, *args, **kwargs)

    return wrapper


class APIClient:
    def __init__(self) -> None:
        self.session = None

    async def start(self) -> None:
        if not self.session:
            self.session = httpx.AsyncClient()

    async def close(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None

    @ensure_session
    async def get(
        self, url: str, params: dict[str, Any] | None = None, **kwargs: Any
    ) -> httpx.Response:
        response = await self.session.get(url, params=params, **kwargs)
        return response

    @ensure_session
    async def post(
        self, url: str, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> httpx.Response:
        response = await self.session.post(url, json=data, **kwargs)
        return response

    @ensure_session
    async def put(
        self, url: str, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> httpx.Response:
        response = await self.session.put(url, json=data, **kwargs)
        return response
    
    @ensure_session
    async def patch(
        self, url: str, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> httpx.Response:
        response = await self.session.patch(url, json=data, **kwargs)
        return response
    
    def __del__(self) -> None:
        if self.session and not self.session.closed:
            warnings.warn("APIClient 객체가 close되지 않았습니다.")
