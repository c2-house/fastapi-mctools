import asyncio
from typing import Any, Optional, Tuple, Dict
from fastapi_mctools.cache.base import CacheStrategy


class MemoryCache(CacheStrategy):
    """
    메모리 기반 캐싱 전략 클래스.

    Attributes:
        maxsize (int): 캐시의 최대 크기.

    Methods:
        get: 메모리에서 키에 해당하는 값을 비동기적으로 가져옵니다.
        set: 메모리에 키와 값을 비동기적으로 설정합니다.
        delete: 메모리에서 키에 해당하는 캐시를 비동기적으로 삭제합니다.
    """

    def __init__(self, maxsize: int = 100) -> None:
        self.cache: Dict[str, Tuple[Any, Optional[float]]] = dict()
        self.maxsize = maxsize
        self.lock = asyncio.Lock()

    async def get(self, key: str) -> Any:
        """
        메모리에서 주어진 키에 해당하는 값을 비동기적으로 가져옵니다.
        캐시에 키가 존재하면 값을 반환하고, 없으면 None을 반환합니다.

        Args:
            key (str): 메모리에서 조회할 키.

        Returns:
            Any: 키에 해당하는 캐시 값, 또는 None.
        """
        async with self.lock:
            item = self.cache.get(key, (None, None))
            value, expire_at = item

            current_time = await self._get_current_time()
            if expire_at is not None and expire_at < current_time:
                await self.delete(key)
                return None

            return value

    async def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """
        메모리에 주어진 키와 값을 비동기적으로 설정합니다.

        Args:
            key (str): 메모리에 저장할 키.
            value (Any): 메모리에 저장할 값.
            timeout (Optional[int]): 캐시의 만료 시간(초). 기본값은 None입니다.
        """
        current_time = await self._get_current_time()
        async with self.lock:
            if len(self.cache) >= self.maxsize:
                self.cache.popitem(last=False)
            expire_at = current_time + timeout if timeout else None
            self.cache[key] = (value, expire_at)

    async def delete(self, key: str) -> None:
        """
        메모리에서 주어진 키에 해당하는 캐시를 비동기적으로 삭제합니다.

        Args:
            key (str): 메모리에서 삭제할 키.
        """
        async with self.lock:
            if key in self.cache:
                del self.cache[key]

    async def _get_current_time(self) -> float:
        return asyncio.get_event_loop().time()
