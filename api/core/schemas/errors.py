"""Schemas for error messages sent by the API."""

from pydantic import BaseModel


class ErrorMessage(BaseModel):
    """An ErrorMessage schema defining a simple error response."""

    error: str
