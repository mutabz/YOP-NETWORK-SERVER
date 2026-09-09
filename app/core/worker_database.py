from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool

from app.core.config import settings


DATABASE_URL = settings.DATABASE_URL


worker_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)


WorkerAsyncSessionLocal = async_sessionmaker(
    bind=worker_engine,
    expire_on_commit=False,
)


Base = declarative_base()


async def get_worker_db():
    async with WorkerAsyncSessionLocal() as session:
        yield session