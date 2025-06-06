from sqlalchemy.orm import Session
from fastapi_mctools.orms import ORMBase, T


class CreateBase(ORMBase):
    """
    CreateBase는 일반적인 Create를 미리 구현해놓은 클래스입니다.
    """

    def create(self, db: Session, **kwargs) -> T:
        """
        INSERT INTO {table_name(self.model)} ({key1}, {key2}, ...) VALUES ({value1}, {value2}, ...)
        """
        db_obj = self.model(**kwargs)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def bulk_create(self, db: Session, data_list: list[dict]) -> None:
        """
        INSERT INTO {table_name(self.model)} ({key1}, {key2}, ...) VALUES ({value1}, {value2}, ...)
        """

        db.bulk_insert_mappings(self.model, data_list)
        db.commit()


class ReadBase(ORMBase):
    """
    ReadBase는 많이 사용되는 Read 쿼리를 미리 구현해놓은 ORM입니다.
    """

    def get(self, db: Session, id: int | str, columns: list[str] = None) -> T:
        """
        SELECT * or ... FROM {table_name(self.model)} WHERE id = {id}
        """
        columns = self.get_columns(columns)
        return db.query(*columns).filter(self.model.id == id).first()

    def get_by_filters(self, db: Session, columns: list[str] = None, **kwargs) -> T:
        """
        SELECT * or ... FROM {table_name(self.model)} WHERE {key} = {value} AND ...
        """
        columns = self.get_columns(columns)

        filters = [(getattr(self.model, k) == v) for k, v in kwargs.items() if hasattr(self.model, k)]
        return db.query(*columns).filter(*filters).first()

    def get_all(
        self,
        db: Session,
        page: int | None = None,
        page_size: int | None = None,
        columns: list[str] = None,
    ) -> list[T]:
        """
        SELECT * or ... FROM {table_name(self.model)}
        or
        SELECT * or ... FROM {table_name(self.model)} LIMIT {page_size} OFFSET {page_size * (page - 1)}
        """
        columns = self.get_columns(columns)

        if page and page_size:
            return db.query(*columns).offset((page - 1) * page_size).limit(page_size).all()
        return db.query(*columns).all()

    def get_all_by_filters(
        self,
        db: Session,
        page: int | None = None,
        page_size: int | None = None,
        columns: list[str] = None,
        **kwargs,
    ) -> list[T]:
        """
        SELECT * or ... FROM {table_name(self.model)} WHERE {key} = {value} AND ...
        """
        columns = self.get_columns(columns)

        filters = [(getattr(self.model, k) == v) for k, v in kwargs.items() if hasattr(self.model, k)]
        if page and page_size:
            return db.query(*columns).filter(*filters).offset((page - 1) * page_size).limit(page_size).all()

        return db.query(*columns).filter(*filters).all()


class UpdateBase(ORMBase):
    def update_by_obj(self, db, db_obj, **kwargs) -> T:
        """
        ALTER TABLE {table_name(self.model)} SET {key1} = {value1}, {key2} = {value2}, ... WHERE id = {db_obj.id}
        """
        for key, value in kwargs.items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj


class DeleteBase(ORMBase):
    def delete(self, db, db_obj) -> T:
        """
        DELETE FROM {table_name(self.model)} WHERE id = {db_obj.id}
        """
        db.delete(db_obj)
        db.commit()
        return db_obj
