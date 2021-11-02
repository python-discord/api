"""
The main API module that houses the FastAPI app.

This app will receive the various routers created by the
individual API versions, which in turn hold the routers
of the individual endpoints within an API version.

The app is initialized with the TokenAuthentication back-end
that defaults to requiring authentication on *all* endpoints,
except the `/docs` and the /openapi.json endpoint manifest
in DEBUG mode.
"""

import datetime
import typing

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware

from api.core.middleware import TokenAuthentication, on_auth_error
from api.core.schemas import ErrorMessage, HealthCheck
from api.core.settings import settings
from api.endpoints import bot_router

app = FastAPI()
app.include_router(bot_router)

# Add our middleware that will try to authenticate
# all requests, excluding /docs and /openapi.json
# in DEBUG mode.

app.add_middleware(
    AuthenticationMiddleware,
    backend=TokenAuthentication(token=settings.auth_token),
    on_error=on_auth_error,
)


@app.exception_handler(RequestValidationError)
async def handle_req_validation_error(
    req: Request, exc: RequestValidationError
) -> JSONResponse:
    """A default handler to handle malformed request bodies."""
    return JSONResponse(status_code=400, content={"error": exc.errors()})


@app.exception_handler(ValueError)
async def handle_validation_value_error(req: Request, exc: ValueError) -> JSONResponse:
    """A default handler to handle value errors raised by pydantic model field validators."""
    return JSONResponse(status_code=400, content={"error": f"{exc}"})


@app.get("/", response_model=HealthCheck, responses={403: {"model": ErrorMessage}})
async def health_check() -> dict[str, typing.Union[str, int, list[str]]]:
    """Perform an API health check, including timestamp and commit sha."""
    return {
        "description": "Python Discord API Health Check",
        "commit_sha": settings.commit_sha,
        "timestamp": datetime.datetime.utcnow().timestamp(),
    }
