import datetime
import typing

from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from api.core.middleware import TokenAuthentication, on_auth_error
from api.core.schemas import ErrorMessage, HealthCheck
from api.core.settings import settings

app = FastAPI()

# Add our middleware that will try to authenticate
# all requests, excluding
app.add_middleware(
    AuthenticationMiddleware,
    backend=TokenAuthentication(token=settings.auth_token),
    on_error=on_auth_error,
)


@app.get("/", response_model=HealthCheck, responses={403: {"model": ErrorMessage}})
async def health_check() -> dict[str, typing.Union[str, int, list[str]]]:
    return {
        "description": "Python Discord API",
        "timestamp": datetime.datetime.utcnow().timestamp(),
    }
