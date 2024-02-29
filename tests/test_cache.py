import pytest
from fastapi_mctools.cache import MemoryCache


@pytest.mark.asyncio
async def test_memory_cache_set_and_get():
    cache = MemoryCache(maxsize=2)
    await cache.set("key1", "value1", 1)

    assert await cache.get("key1") == "value1"


@pytest.mark.asyncio
async def test_memory_cache_eviction():
    cache = MemoryCache(maxsize=2)
    await cache.set("key1", "value1")
    await cache.set("key2", "value2")
    await cache.set("key3", "value3")

    assert await cache.get("key1") is None
    assert await cache.get("key2") == "value2"
    assert await cache.get("key3") == "value3"
