"""Schemas for API health checks."""

from pydantic import BaseModel


class HealthCheck(BaseModel):
    """A schema representing a simple health check response."""

    description: str
    timestamp: int
