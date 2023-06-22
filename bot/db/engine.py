from config import DB_ECHO
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine


def create_async_engine(url: URL | str) -> AsyncEngine:
    return _create_async_engine(url=url, echo=DB_ECHO, pool_pre_ping=True)  # проверять соединение


# async def proceed_schemas(engine: AsyncEngine, metadata: MetaData):
#     # типа схема-миграция
#     async with engine.begin() as conn:
#         await conn.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine, expire_on_commit=False)  # class_=AsyncEngine
