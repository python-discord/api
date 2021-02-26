import typing

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.core.settings import settings


class TokenAuthentication(AuthenticationBackend):
    """Simple token authentication."""

    def __init__(self, token: str) -> None:
        self.expected_auth_header = f"Bearer {token}"

    async def authenticate(
        self, request: Request
    ) -> typing.Optional[tuple[AuthCredentials, SimpleUser]]:
        """Authenticate the request based on the Authorization header."""
        if settings.DEBUG and request.url.path.startswith(("/docs", "/openapi.json")):
            return

        authorization_header = request.headers.get("Authorization")

        if not authorization_header:
            raise AuthenticationError("'Authorization' header not found.")

        if authorization_header != self.expected_auth_header:
            raise AuthenticationError("invalid credentials.")

        credentials = AuthCredentials(scopes=["authenticated"])
        user = SimpleUser(username="api_client")

        return credentials, user


def on_auth_error(_request: Request, exc: Exception):
    return JSONResponse({"error": str(exc)}, status_code=403)
