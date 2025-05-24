import pytest
from fastapi_mctools.orms.sqlalchemy.async_base import ACreateBase, AReadBase
from fastapi_mctools.orms.sqlalchemy.filters import FilterBackend


class TestAsyncBase:
    @pytest.fixture
    def orm_obj(self, item):
        class Create(ACreateBase): ...

        class Read(AReadBase): ...

        class ORM(Read, Create):
            def __init__(self, model):
                self.model = model

        return ORM(item)

    @pytest.mark.asyncio
    async def test_create(self, orm_obj, async_db):
        item = await orm_obj.create(async_db, name="test")
        assert item.name == "test"

    @pytest.mark.asyncio
    async def test_read_with_simple_filters(self, orm_obj, async_db):
        item = await orm_obj.create(async_db, name="test")
        result = await orm_obj.get_by_id(async_db, id=1)
        assert result.name == item.name

        results = await orm_obj.get_by_filters(async_db, name="test")
        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_read_with_filter_backend(self, orm_obj, async_db):
        await orm_obj.bulk_create(
            async_db,
            [
                {"name": "fast"},
                {"name": "api"},
                {"name": "test123"},
                {"name": "test456"},
            ],
        )
        filter_backend = FilterBackend()
        filter_backend.set_model(orm_obj.model)
        filter_backend.add_filter({"name": "%test%"}, "like")
        results = await orm_obj.get_by_filters(async_db, filter_backend=filter_backend)
        assert len(results) == 2

        filter_backend.add_filter({"id": 3})
        results = await orm_obj.get_by_filters(async_db, filter_backend=filter_backend)
        assert len(results) == 1

        filter_backend = FilterBackend()
        filter_backend.set_model(orm_obj.model)
        filter_backend.add_filter({"name": "fast"}, is_and=False)
        filter_backend.add_filter({"name": "api"}, is_and=False)
        results = await orm_obj.get_by_filters(async_db, filter_backend=filter_backend)
        assert len(results) == 2
