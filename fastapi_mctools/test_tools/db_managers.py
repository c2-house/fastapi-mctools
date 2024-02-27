from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from fastapi_mctools.orms import T


class TestConfDBManager:
    """
    DBManager for use in conftest.py.
    Creates synchronous and asynchronous databases for testing.
    """

    __test__ = False

    def __init__(self, db_url: str) -> None:
        self.db_url = db_url

    def get_db_session(self, is_meta: bool = False) -> Session:
        """
        사용:

        @pytest.fixture
        def db():
            yield from test_db_manager.get_db_session()
        """
        engine = create_engine(self.db_url)

        if is_meta:
            meta = MetaData()
            meta.drop_all(engine)
            meta.create_all(engine)

        connection = engine.connect()
        connection.begin()

        session = Session(bind=connection, autoflush=False, autocommit=False)

        yield session

        session.rollback()
        connection.close()
        engine.dispose()

    async def get_async_db_session(self, base: T = None, is_meta: bool = False) -> AsyncSession:
        """
        사용:

        @pytest.fixture
        async def async_db():
            async for session in test_db_manager.get_async_db_session():
                yield session
        """
        engine = create_async_engine(self.db_url)
        if is_meta:
            async with engine.begin() as connection:
                await connection.run_sync(base.metadata.drop_all)
                await connection.run_sync(base.metadata.create_all)

        async_session = async_sessionmaker(
            engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

        async with async_session() as session:
            yield session
            await session.rollback()

        await engine.dispose()
