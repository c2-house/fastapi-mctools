from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
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

    def __init__(self, db_url: str) -> None:
        self.engine = create_async_engine(db_url)
        self.async_session = async_sessionmaker(
            self.engine, autoflush=False, autocommit=False
        )
        self.meta = MetaData()

    async def __call__(self) -> AsyncSession:
        async with self.engine.begin() as conn:
            await conn.run_sync(self.meta.create_all)

        db = self.async_session()
        try:
            yield db
        finally:
            await db.close()
