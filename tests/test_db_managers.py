import pytest
from fastapi_mctools.test_tools.db_managers import TestConfDBManager


test_db_manager = TestConfDBManager("sqlite:///example.db")


@pytest.fixture
def db():
    yield from test_db_manager.get_db_session()


@pytest.fixture
async def async_db():
    test_db_manager.db_url = "sqlite+aiosqlite:///example.db"
    async for session in test_db_manager.get_async_db_session():
        yield session


def test_db_fixture(db):
    assert db is not None


@pytest.mark.asyncio
async def test_async_db_fixture(async_db):
    assert async_db is not None
