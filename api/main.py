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

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.middleware.authentication import AuthenticationMiddleware

from api.core.database import Base
from api.core.middleware import TokenAuthentication, on_auth_error
from api.core.schemas import ErrorMessage, HealthCheck
from api.core.settings import settings

app = FastAPI()

# Add our middleware that will try to authenticate
# all requests, excluding /docs and /openapi.json
# in DEBUG mode.
app.add_middleware(
    AuthenticationMiddleware,
    backend=TokenAuthentication(token=settings.auth_token),
    on_error=on_auth_error,
)

engine = create_engine(settings.database_url)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)


@app.get("/", response_model=HealthCheck, responses={403: {"model": ErrorMessage}})
async def health_check() -> dict[str, typing.Union[str, int, list[str]]]:
    """Perform an API health check, including timestamp and commit sha."""
    return {
        "description": "Python Discord API Health Check",
        "commit_sha": settings.commit_sha,
        "timestamp": datetime.datetime.utcnow().timestamp(),
    }
