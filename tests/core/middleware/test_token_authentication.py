import itertools
import json
import typing
from unittest.mock import Mock, patch

import pytest
from hypothesis import assume, given
from hypothesis.strategies import text
from starlette.authentication import AuthCredentials, AuthenticationError, SimpleUser
from starlette.responses import JSONResponse

from api.core import settings
from api.core.middleware import TokenAuthentication
from api.core.middleware.token_authentication import (
    INVALID_CREDENTIALS,
    NO_AUTH_DEBUG_ENDPOINTS,
    NO_AUTHORIZATION_HEADER,
    on_auth_error,
)

pytestmark = pytest.mark.asyncio

API_TOKEN = "api_token_only_for_testing"


def create_request(path: str, token: typing.Optional[str]) -> Mock:
    """Create a mocked Request with a path and optional authorization header."""
    request = Mock()
    request.url.path = path
    request.headers = {}

    if token is not None:
        request.headers["Authorization"] = f"Bearer {token}"

    return request


@pytest.fixture(scope="module")
def auth_middleware() -> TokenAuthentication:
    """Return a TokenAuthentication back-end with a fixed token."""
    return TokenAuthentication(API_TOKEN)


@pytest.fixture(autouse=True)
def mock_settings() -> Mock:
    """Set `DEBUG=False` as a default for running tests."""
    with patch.object(settings, "DEBUG") as mock_settings:
        mock_settings.DEBUG = False
        yield mock_settings


async def test_authenticates_with_valid_token(
    auth_middleware: TokenAuthentication,
) -> None:
    """Test authentication with a valid token."""
    request = create_request("/", API_TOKEN)
    credentials, user = await auth_middleware.authenticate(request)

    assert isinstance(credentials, AuthCredentials)
    assert credentials.scopes == ["authenticated"]

    assert isinstance(user, SimpleUser)
    assert user.username == "api_client"


async def test_authentication_fails_without_auth_header(
    auth_middleware: TokenAuthentication,
) -> None:
    """Test authentication without providing a Authentication header."""
    request = create_request("/", None)
    with pytest.raises(AuthenticationError) as exc:
        await auth_middleware.authenticate(request)

    assert NO_AUTHORIZATION_HEADER in exc.value.args


@given(text())
async def test_authentication_fails_with_incorrect_token(
    auth_middleware: TokenAuthentication,
    invalid_token: str,
) -> None:
    """Test authentication with an invalid token."""
    assume(invalid_token != API_TOKEN)

    request = create_request("/", invalid_token)
    with pytest.raises(AuthenticationError) as exc:
        await auth_middleware.authenticate(request)

    assert INVALID_CREDENTIALS in exc.value.args


@pytest.mark.parametrize(
    argnames=("debug_path", "token"),
    argvalues=itertools.product(
        NO_AUTH_DEBUG_ENDPOINTS,
        (None, "invalid token"),
    ),
)
async def test_debug_unauthenticated_access(
    auth_middleware: TokenAuthentication,
    debug_path: str,
    token: str,
    mock_settings: Mock,
) -> None:
    """Test unauthenticated access to some endpoints in DEBUG mode."""
    request = create_request(debug_path, token)
    mock_settings.DEBUG = True

    credentials, user = await auth_middleware.authenticate(request)

    assert credentials.scopes == ["debug"]
    assert user.username == "api_client"


def test_on_auth_error_serialized_exception_message() -> None:
    """Test the serialization of an auth error as JSON."""
    error_message = "Error message"
    request = create_request("/", None)
    exc = AuthenticationError(error_message)
    response = on_auth_error(request, exc)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 403
    assert json.loads(response.body) == {"error": error_message}
