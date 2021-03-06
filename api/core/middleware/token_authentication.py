"""Middleware for Bearer token authentication."""

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.core.settings import settings

NO_AUTHORIZATION_HEADER = "no `Authorization` header in request."
INVALID_CREDENTIALS = "invalid credentials."
NO_AUTH_DEBUG_ENDPOINTS = ("/docs", "/openapi.json")


class TokenAuthentication(AuthenticationBackend):
    """Simple token authentication."""

    def __init__(self, token: str) -> None:
        self.expected_auth_header = f"Bearer {token}"

    async def authenticate(
        self, request: Request
    ) -> tuple[AuthCredentials, SimpleUser]:
        """Authenticate the request based on the Authorization header."""
        if settings.DEBUG and request.url.path.startswith(NO_AUTH_DEBUG_ENDPOINTS):
            credentials = AuthCredentials(scopes=["debug"])
            user = SimpleUser(username="api_client")
            return credentials, user

        authorization_header = request.headers.get("Authorization")

        if not authorization_header:
            raise AuthenticationError(NO_AUTHORIZATION_HEADER)

        if authorization_header != self.expected_auth_header:
            raise AuthenticationError(INVALID_CREDENTIALS)

        credentials = AuthCredentials(scopes=["authenticated"])
        user = SimpleUser(username="api_client")

        return credentials, user


def on_auth_error(_request: Request, exc: Exception) -> JSONResponse:
    """Send an authentication error message serialized as JSON."""
    return JSONResponse({"error": str(exc)}, status_code=403)
