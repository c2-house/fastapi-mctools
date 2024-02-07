from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


class DB:
    """
    db connection by sqlalchemy, Syncronous version
    usage:
        get_db = DB(db_url)
    """

    def __init__(self, db_url: str) -> None:
        self.engine = create_engine(db_url, pool_pre_ping=True)
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def __call__(self) -> Session:
        db = self.session()
        try:
            yield db
        finally:
            db.close()


class AsyncDB:
    """
    db connection by sqlalchemy, Asyncronous version
    usage:
        get_db = AsyncDB(db_url)
    """

    def __init__(self, db_url: str, meta: MetaData = None, **kwargs) -> None:
        self.db_url = db_url
        self.meta = meta
        self.__engine = create_async_engine(db_url)
        self.__async_session = async_sessionmaker(self.__engine, **kwargs)

    @property
    def engine(self) -> Engine:
        return self.__engine

    @property
    def async_session(self) -> AsyncSession:
        return self.__async_session

    async def run_sync(self) -> None:
        async with self.engine.begin() as conn:
            return await conn.run_sync(self.meta)

    async def __call__(self) -> AsyncSession:
        if self.meta:
            await self.run_sync()

        db = self.async_session()
        try:
            yield db
        finally:
            await db.close()
