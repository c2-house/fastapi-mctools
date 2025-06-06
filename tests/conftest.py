import pytest
from sqlalchemy import INTEGER, String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from fastapi_mctools.test_tools.db_managers import TestConfDBManager

test_db_manager = TestConfDBManager("sqlite:///example.db")


class Base(DeclarativeBase): ...


class Item(Base):
    __tablename__ = "items"
    id = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name = mapped_column(String(255), nullable=False)


@pytest.fixture
async def item():
    return Item


@pytest.fixture
async def async_db():
    test_db_manager.db_url = "sqlite+aiosqlite:///example.db"
    async for session in test_db_manager.get_async_db_session(base=Base, is_meta=True):
        yield session
