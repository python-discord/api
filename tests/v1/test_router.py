"""Tests API routing and fallback functionality."""
import http
from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient, Response

from api.v1 import router


@pytest.mark.asyncio
@pytest.mark.parametrize('route', ('/api/i-definitely-do-not-exist',))
async def test_forwards_to_old_api_for_undefined_routes(
    client: AsyncClient,
    route: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """
    Tests undefined endpoints proxying to the old API.

    This is kind of problematic to test, since a proper test would require us
    starting the old site backend on both CI and local development environments,
    a mess that nobody wants. So instead, we simply mock away the HTTP client.
    """
    old_api_response = Response(
        status_code=http.HTTPStatus.OK,
        headers={'X-Clacks-Overhead': 'GNU Terry Pratchett, Joe Armstrong'},
        content='ok',
    )

    client_mock = MagicMock(spec=AsyncClient)
    # This mocking has to be a bit ugly, due to the context manager involved. Sorry :(
    mock_aenter = client_mock.return_value.__aenter__
    mock_aenter.return_value.request.return_value = old_api_response
    monkeypatch.setattr(router, 'AsyncClient', client_mock)

    response = await client.get(route)

    # Check that the response matches the mocked response from above.
    assert response.status_code is http.HTTPStatus.OK
    assert response.content == b'ok'
    assert response.headers == {
        **old_api_response.headers,
        'Via': 'HTTP/1.1 new-api',
    }
