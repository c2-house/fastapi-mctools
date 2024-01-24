import asyncio
import pytest
from sqlalchemy.orm import DeclarativeBase
from fastapi_mctools.test_tools.db_managers import TestConfDBManager

test_db_manager = TestConfDBManager("sqlite:///example.db")


class Base(DeclarativeBase):
    ...


@pytest.fixture
def db():
    yield from test_db_manager.get_db_session(is_meta=True)


@pytest.fixture
async def async_db():
    test_db_manager.db_url = "sqlite+aiosqlite:///example.db"
    async for session in test_db_manager.get_async_db_session(base=Base):
        yield session


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
