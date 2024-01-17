from typing import Any, Optional
from fastapi_mctools.cache.base import CacheStrategy


class CacheManager:
    """
    Cache management class.
    Manages various caching strategies.

    Attributes:
        strategy (CacheStrategy): The caching strategy to use.

    Methods:
        get: Retrieves a cache value corresponding to a key.
        set: Sets a key and value in the cache.
        delete: Deletes the cache corresponding to a key.
    """

    def __init__(self, strategy: CacheStrategy) -> None:
        self.strategy = strategy

    async def get(self, key: str) -> Any:
        """
        Retrieves a value corresponding to a given key from the cache.

        Args:
            key (str): The key to be looked up in the cache.

        Returns:
            Any: The cache value corresponding to the key.
        """
        return await self.strategy.get(key)

    async def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """
        Sets a given key and value in the cache.

        Args:
            key (str): The key to store in the cache.
            value (Any): The value to store in the cache.
            timeout (Optional[int]): The expiration time of the cache in seconds. Default is None.
        """
        await self.strategy.set(key, value, timeout)

    async def delete(self, key: str) -> None:
        """
        Deletes a cache entry corresponding to a given key.

        Args:
            key (str): The key of the cache entry to be deleted.
        """
        await self.strategy.delete(key)
