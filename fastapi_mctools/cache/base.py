from typing import Protocol, Any, Optional, runtime_checkable


@runtime_checkable
class CacheStrategy(Protocol):
    """
    Protocol to define a caching strategy.
    Defines the basic methods for cache management.

    Methods:
        get: Retrieves a value corresponding to a key from the cache.
        set: Sets a key and value in the cache.
        delete: Deletes a value corresponding to a key from the cache.
    """

    async def get(self, key: str) -> Any:
        """
        Asynchronously retrieves a value corresponding to a given key from the cache.

        Args:
            key (str): The key to be looked up in the cache.

        Returns:
            Any: The cache value corresponding to the key.
        """
        ...

    async def set(self, key: str, value: Any, timeout: Optional[int] = None) -> None:
        """
        Asynchronously sets a given key and value in the cache.

        Args:
            key (str): The key to store in the cache.
            value (Any): The value to store in the cache.
            timeout (Optional[int]): The expiration time of the cache in seconds. Default is None.
        """
        ...

    async def delete(self, key: str) -> None:
        """
        Asynchronously deletes a value corresponding to a given key from the cache.

        Args:
            key (str): The key of the cache to be deleted.
        """
        ...
