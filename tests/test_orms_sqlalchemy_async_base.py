import pytest
from fastapi_mctools.orms.sqlalchemy.async_base import ACreateBase, AReadBase


class TestAsyncBase:
    @pytest.fixture
    def orm_obj(self, item):
        class Create(ACreateBase):
            ...

        class Read(AReadBase):
            ...

        class ORM(Read, Create):
            def __init__(self, model):
                self.model = model

        return ORM(item)

    @pytest.mark.asyncio
    async def test_create(self, orm_obj, async_db):
        item = await orm_obj.create(async_db, name="test")
        assert item.name == "test"
