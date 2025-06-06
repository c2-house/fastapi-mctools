import pytest
from fastapi_mctools.lifespan import Lifespan


@pytest.mark.asyncio
async def test_lifespan_startup_and_shutdown_called():
    events = []

    async def startup():
        events.append("startup")

    async def shutdown():
        events.append("shutdown")

    lifespan = Lifespan()
    lifespan.add_startup(startup)
    lifespan.add_shutdown(shutdown)
    async with lifespan:
        assert "startup" in events
    assert "shutdown" in events


@pytest.mark.asyncio
async def test_lifespan_sync_and_async_events():
    events = []

    def sync_startup():
        events.append("sync_startup")

    async def async_shutdown():
        events.append("async_shutdown")

    lifespan = Lifespan()
    lifespan.add_startup(sync_startup)
    lifespan.add_shutdown(async_shutdown)
    async with lifespan:
        assert "sync_startup" in events
    assert "async_shutdown" in events


@pytest.mark.asyncio
async def test_lifespan_states_property():
    lifespan = Lifespan()
    # Set states as dict
    lifespan.states = {"foo": "bar"}
    assert lifespan.states == {"foo": "bar"}
    # Set states as callable
    lifespan.states = lambda: {"baz": 123}
    assert lifespan.states == {"baz": 123}
    # Set states as invalid type
    with pytest.raises(ValueError):
        lifespan.states = "not a dict"
        _ = lifespan.states
