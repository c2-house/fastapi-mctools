import asyncio
from typing import Any, Optional, Tuple
from collections import OrderedDict
from fastapi_mctools.cache.base import CacheStrategy


class MemoryCache(CacheStrategy):
    """
    Memory-based caching strategy class.

    Attributes:
        maxsize (int): The maximum size of the cache.

    Methods:
        get: Asynchronously retrieves a value corresponding to a key from memory.
        set: Asynchronously sets a key and value in memory.
        delete: Asynchronously deletes a cache entry corresponding to a key from memory.
    """

    def __init__(self, maxsize: int = 100) -> None:
        self.cache: OrderedDict[str, Tuple[Any, Optional[float]]] = OrderedDict()
        self.maxsize = maxsize
        self.lock = asyncio.Lock()

    async def get(self, key: str) -> Any:
        """
        Asynchronously retrieves a value corresponding to a given key from memory.
        Returns the value if the key exists in the cache, or None if it does not.

        Args:
            key (str): The key to be looked up in memory.

        Returns:
            Any: The cache value corresponding to the key, or None.
        """
        async with self.lock:
            item = self.cache.get(key, (None, None))
            value, expire_at = item

            current_time = await self._get_current_time()
            if expire_at is not None and expire_at < current_time:
                del self.cache[key]
                return None

            return value

    async def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """
        Asynchronously sets a given key and value in memory.

        Args:
            key (str): The key to store in memory.
            value (Any): The value to store in memory.
            timeout (Optional[int]): The expiration time of the cache in seconds. Default is None.
        """
        current_time = await self._get_current_time()
        async with self.lock:
            if len(self.cache) >= self.maxsize:
                self.cache.popitem(last=False)
            expire_at = current_time + timeout if timeout else None
            self.cache[key] = (value, expire_at)

    async def delete(self, key: str) -> None:
        """
        Asynchronously deletes a cache entry corresponding to a given key from memory.

        Args:
            key (str): The key of the cache entry to be deleted from memory.
        """
        async with self.lock:
            if key in self.cache:
                del self.cache[key]

    async def _get_current_time(self) -> float:
        """
        Retrieves the current time in the event loop.

        Returns:
            float: The current time.
        """
        return asyncio.get_event_loop().time()
