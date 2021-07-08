import asyncio
import contextlib

import pytest
from httpx import AsyncClient

from api.core.settings import settings
from api.main import app


@pytest.fixture(scope='session')
def event_loop() -> asyncio.AbstractEventLoop:
    """
    Yield an asyncio event loop.

    This is redefined from ``pytest-asyncio`` to allow for a ``session``
    lifetime event loop to exist, which can be used in fixtures living
    for longer than single test case.
    """
    loop = asyncio.get_event_loop()
    with contextlib.closing(loop):
        yield loop


@pytest.fixture(scope='session')
def auth_token() -> str:
    """Return an authorization token for tests."""
    return settings.auth_token


# This is session-lived, because we really do not need to run initialization
# and teardown of the FastAPI app (and thus database connections etc.) for
# every test case utilizing the client.
@pytest.fixture(scope='session')
async def client(auth_token: str) -> AsyncClient:
    """
    Return a client that can be used for issuing HTTP requests to the API.

    The returned client will have a working authorization token passed for
    all requests, removing the need to manually configure this in tests.

    Further information about this can be found at:
    - the FastAPI documentation on asynchronous tests:
      https://fastapi.tiangolo.com/advanced/async-tests/
    - The HTTPX client website: https://www.python-httpx.org
    """
    headers = {'Authorization': f'Bearer {auth_token}'}
    async with AsyncClient(app=app, base_url='http://test', headers=headers) as client:
        yield client
