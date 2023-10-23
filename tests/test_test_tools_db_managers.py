import pytest


def test_db_fixture(db):
    assert db is not None


@pytest.mark.asyncio
async def test_async_db_fixture(async_db):
    assert async_db is not None
