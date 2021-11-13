from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.core import settings

engine = create_async_engine(settings.database_url, future=True)
session_factory = sessionmaker(engine, class_=AsyncSession)


async def create_database_session() -> None:
    """A FastAPI dependency that creates an SQLAlchemy session."""
    try:
        async with session_factory() as session:
            yield session
    finally:
        await session.close()
