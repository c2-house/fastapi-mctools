from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_mctools.orms import ORMBase, T
from fastapi_mctools.orms.sqlalchemy.filters import FilterBackend


class ACreateBase(ORMBase):
    """
    CreateBase is the preset of Create query.
    """

    async def create(self, db: AsyncSession, **kwargs) -> T:
        """
        INSERT INTO {table_name(self.model)} ({key1}, {key2}, ...) VALUES ({value1}, {value2}, ...)
        """
        db_obj = self.model(**kwargs)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def bulk_create(self, db: AsyncSession, data_list: list[dict]) -> None:
        """
        INSERT INTO {table_name(self.model)} ({key1}, {key2}, ...) VALUES ({value1}, {value2}, ...), ({value1}, {value2}, ...)
        """
        query = insert(self.model).values(data_list)
        await db.execute(query)
        await db.commit()


class AReadBase(ORMBase):
    """
    ReadBase is the preset of Read query.
    when using filter, the operator can be specified.
    :param operator: eq, ne, lt, lte, gt, gte

    """

    async def get_by_id(self, db: AsyncSession, id: int | str, columns: list[str] | None = None) -> T:
        """
        SELECT * or ... FROM {table_name(self.model)} WHERE id = {id}
        """
        columns = self.get_columns(columns)
        query = select(*columns).filter(self.model.id == id)
        result = await db.execute(query)
        return self.get_result(result, columns)

    async def get_by_filters(
        self,
        db: AsyncSession,
        columns: list[str] | None = None,
        operator="eq",
        filter_backend: FilterBackend = None,
        page: int | None = None,
        page_size: int | None = None,
        **filters,
    ):
        """
        SELECT * or ... FROM {table_name(self.model)} WHERE {key} = {value} AND ...
        """
        columns = self.get_columns(columns)
        if filter_backend:
            filters = filter_backend.compile()
            query = select(*columns).filter(filters)
        else:
            filters = self.get_filters_by_operator(filters, operator)
            query = select(*columns).filter(*filters)
        if page and page_size:
            query = query.limit(page_size).offset(page_size * (page - 1))
        results = await db.execute(query)
        return self.get_results(results, columns)


class AUpdateBase(ORMBase):
    """
    UpdateBase is the preset of Update query.
    """

    async def update_by_obj(self, db: AsyncSession, db_obj: T, **kwargs) -> T:
        """
        UPDATE {table_name(self.model)} SET {key1} = {value1}, {key2} = {value2}, ... WHERE id = {db_obj.id}
        """
        for key, value in kwargs.items():
            setattr(db_obj, key, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_by_id(self, db: AsyncSession, id: int | str, **kwargs) -> None:
        """
        UPDATE {table_name(self.model)} SET {key1} = {value1}, {key2} = {value2}, ... WHERE id = {id}
        """
        query = update(self.model).where(self.model.id == id).values(**kwargs)
        await db.execute(query)
        await db.commit()

    async def update_by_filters(self, db: AsyncSession, filters: list, **kwargs) -> None:
        """
        UPDATE {table_name(self.model)} SET {key1} = {value1}, {key2} = {value2}, ... WHERE {filters}
        """
        query = update(self.model).where(*filters).values(**kwargs)
        await db.execute(query)
        await db.commit()


class ADeleteBase(ORMBase):
    """
    DeleteBase is the preset of Delete query.
    """

    async def delete(self, db: AsyncSession, db_obj: T) -> None:
        """
        DELETE FROM {table_name(self.model)} WHERE id = {db_obj.id}
        """
        await db.delete(db_obj)
        await db.commit()
