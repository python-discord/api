import asyncio
from typing import Callable, Generator
from urllib.parse import urlsplit, urlunsplit

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from api.core.database import Base
from api.core.settings import settings
from api.endpoints.dependencies.database import create_database_session
from api.main import app as main_app

AUTH_HEADER = {"Authorization": f"Bearer {settings.auth_token}"}
test_engine = create_async_engine(settings.database_url, future=True, isolation_level="AUTOCOMMIT")


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def create_test_database_engine() -> Generator:
    async with test_engine.begin() as conn:
        await conn.execute(text("CREATE DATABASE test;"))
        test_db_url = urlsplit(settings.database_url)._replace(path="/test")
        engine = create_async_engine(urlunsplit(test_db_url), future=True)
        yield engine
        await engine.dispose()
        await conn.execute(text("DROP DATABASE test;"))


@pytest.fixture()
async def async_db_session(create_test_database_engine: AsyncEngine) -> AsyncSession:
    async with create_test_database_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async with AsyncSession(bind=conn, expire_on_commit=False) as session:
            yield session
            await session.close()


@pytest.fixture(scope="session", autouse=True)
async def global_teardown(create_test_database_engine: AsyncEngine):
    yield
    async with create_test_database_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture()
def override_db_session(async_db_session: AsyncSession):
    async def _override_db_session():
        yield async_db_session

    yield _override_db_session


@pytest.fixture()
def app(override_db_session: Callable):
    main_app.dependency_overrides[create_database_session] = override_db_session
    yield main_app


@pytest.fixture()
async def unauthed_client(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://testserver") as httpx_client:
        yield httpx_client


@pytest.fixture()
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://testserver", headers=AUTH_HEADER) as httpx_client:
        yield httpx_client
