"""
Schemas used by the Python Discord API.

This package contains the schemas used by the various
endpoints of the API. Schemas are represented by pydantic
models, which simplifies data coercion and validation.
"""

from .errors import ErrorMessage
from .health_check import HealthCheck
