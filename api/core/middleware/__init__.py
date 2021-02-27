"""Custom middleware for the Python Discord API."""

from .token_authentication import TokenAuthentication, on_auth_error
