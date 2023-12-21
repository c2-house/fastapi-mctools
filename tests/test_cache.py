import pytest
import asyncio
from fastapi_mctools.cache import MemoryCache, CacheManager


@pytest.mark.asyncio
async def test_memory_cache_set_and_get():
    cache = MemoryCache(maxsize=2)
    await cache.set("key1", "value1", 1)

    assert await cache.get("key1") == "value1"

    await asyncio.sleep(1.1)  # 캐시 만료 대기
    assert await cache.get("key1") is None


@pytest.mark.asyncio
async def test_memory_cache_eviction():
    cache = MemoryCache(maxsize=2)
    await cache.set("key1", "value1")
    await cache.set("key2", "value2")
    await cache.set("key3", "value3")

    assert await cache.get("key1") is None
    assert await cache.get("key2") == "value2"
    assert await cache.get("key3") == "value3"


@pytest.mark.asyncio
async def test_cache_manager_with_memory_cache():
    memory_cache = MemoryCache(maxsize=2)
    cache_manager = CacheManager(memory_cache)

    await cache_manager.set("key1", "value1")
    assert await cache_manager.get("key1") == "value1"

    await cache_manager.delete("key1")
    assert await cache_manager.get("key1") is None
