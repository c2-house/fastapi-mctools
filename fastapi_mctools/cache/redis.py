from redis import asyncio as aioredis
from typing import Any, Optional, Type
from fastapi_mctools.cache.base import CacheStrategy


RedisType = Type[aioredis.Redis]


class RedisCache(CacheStrategy):
    """
    Redis를 사용하는 분산 캐싱 전략 클래스.

    Attributes:
        redis_url (str): Redis 서버의 URL.

    Methods:
        get: Redis에서 키에 해당하는 값을 비동기적으로 가져옵니다.
        set: Redis에 키와 값을 비동기적으로 설정합니다.
        delete: Redis에서 키에 해당하는 캐시를 비동기적으로 삭제합니다.
    """

    def __init__(self, redis_url: str) -> None:
        self.redis: RedisType = aioredis.from_url(redis_url)

    async def get(self, key: str) -> Any:
        """
        Redis에서 주어진 키에 해당하는 값을 비동기적으로 가져옵니다.

        Args:
            key (str): Redis에서 조회할 키.

        Returns:
            Any: 키에 해당하는 캐시 값.
        """

        if await self.redis.exists(key):
            return await self.redis.get(key)
        return None

    async def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """
        Redis에 주어진 키와 값을 비동기적으로 설정합니다.

        Args:
            key (str): Redis에 저장할 키.
            value (Any): Redis에 저장할 값.
            timeout (Optional[int]): 캐시의 만료 시간(초). 기본값은 None입니다.
        """
        await self.redis.setex(key, timeout, value)

    async def delete(self, key: str) -> None:
        """
        Redis에서 주어진 키에 해당하는 캐시를 비동기적으로 삭제합니다.

        Args:
            key (str): Redis에서 삭제할 키.
        """
        await self.redis.delete(key)
