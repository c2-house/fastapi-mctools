import pytest
from fastapi_mctools.lifespan import Lifespan


class TestLifespan:
    @pytest.fixture
    def lifespan(self):
        return Lifespan()

    @pytest.mark.asyncio
    async def test_add_startup(self, lifespan):
        async def startup_event():
            pass

        lifespan.add_startup(startup_event)
        assert len(lifespan.startup_events.events) == 1

    @pytest.mark.asyncio
    async def test_add_shutdown(self, lifespan):
        async def shutdown_event():
            pass

        lifespan.add_shutdown(shutdown_event)
        assert len(lifespan.shutdown_runner.events) == 1

    @pytest.mark.asyncio
    async def test_states_property(self, lifespan):
        states = {"key": "value"}
        lifespan.states = states
        assert lifespan.states == states

    @pytest.mark.asyncio
    async def test_states_property_callable(self, lifespan):
        def get_states():
            return {"key": "value"}

        lifespan.states = get_states
        assert lifespan.states == {"key": "value"}

    @pytest.mark.asyncio
    async def test_states_property_invalid(self, lifespan):
        with pytest.raises(ValueError):
            lifespan.states = "invalid"
            lifespan.states

    @pytest.mark.asyncio
    async def test_lifespan_context_manager(self, lifespan):
        async def startup_event():
            pass

        async def shutdown_event():
            pass

        lifespan.add_startup(startup_event)
        lifespan.add_shutdown(shutdown_event)

        async with lifespan:
            assert len(lifespan.startup_events.events) == 1
            assert len(lifespan.shutdown_runner.events) == 1
