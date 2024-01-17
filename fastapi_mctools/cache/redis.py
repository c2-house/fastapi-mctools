from redis import asyncio as aioredis
from typing import Any, Optional, Type
from fastapi_mctools.cache.base import CacheStrategy


RedisType = Type[aioredis.Redis]


class RedisCache(CacheStrategy):
    """
    A caching strategy class using Redis.

    Attributes:
        redis_url (str): URL of the Redis server.

    Methods:
        get: Asynchronously retrieves a value corresponding to a key from Redis.
        set: Asynchronously sets a key and value in Redis.
        delete: Asynchronously deletes a cache entry corresponding to a key from Redis.
    """

    def __init__(self, redis_url: str) -> None:
        self.redis: RedisType = aioredis.from_url(redis_url)

    async def get(self, key: str) -> Any:
        """
        Asynchronously retrieves a value corresponding to a given key from Redis.

        Args:
            key (str): The key to be looked up in Redis.

        Returns:
            Any: The cache value corresponding to the key.
        """
        if await self.redis.exists(key):
            return await self.redis.get(key)
        return None

    async def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """
        Asynchronously sets a given key and value in Redis.

        Args:
            key (str): The key to store in Redis.
            value (Any): The value to store in Redis.
            timeout (Optional[int]): The expiration time of the cache in seconds. Default is None.
        """
        await self.redis.setex(key, timeout, value)

    async def delete(self, key: str) -> None:
        """
        Asynchronously deletes a cache entry corresponding to a given key from Redis.

        Args:
            key (str): The key of the cache entry to be deleted from Redis.
        """
        await self.redis.delete(key)
