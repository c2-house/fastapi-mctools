from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


class TestConfDBManager:
    """
    conftest.py에서 사용할 DBManager
    테스트에 사용할 동기 DB, 비동기 DB를 생성합니다.
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
            meta.create_all(engine)

        connection = engine.connect()
        connection.begin()

        session = Session(bind=connection, autoflush=False, autocommit=False)

        yield session

        session.rollback()
        connection.close()
        engine.dispose()

    async def get_async_db_session(self, is_meta: bool = False) -> AsyncSession:
        """
        사용:

        @pytest.fixture
        async def async_db():
            async for session in test_db_manager.get_async_db_session():
                yield session
        """
        engine = create_async_engine(self.db_url)
        if is_meta:
            meta = MetaData()
            async with engine.begin() as connection:
                await connection.run_sync(meta.create_all)

        async with engine.begin() as connection:
            transaction = await connection.begin()
            async_session = async_sessionmaker(
                connection, autoflush=False, autocommit=False, expire_on_commit=False
            )
            async with async_session() as session:
                await session.begin()

                yield session

                await transaction.rollback()
