"""
The settings module for the Python Discord API.

The settings will be automatically loaded from environment
variables with the same name as the class attributes. In
addition, a `.env`-file will automatically be parsed in a
development environment.

To use settings in other parts of the application, you can
import the name `settings` from `api.core` directly.
"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    A Settings class that will parse env variables.

    When this class is instantiated, it will automatically
    try to get missing values from the environment. In a dev
    environment, if `python-dotenv` is installed, it will also
    try to load a `.env`-file from the root of the project.

    If no default value is given and no matching environment
    variable is found, instantiating this class will raise a
    `pydantic.error_wrappers.ValidationError` exception.
    """
    database_url: str
    auth_token: str
    commit_sha: str = "development"
    DEBUG: bool = False

    class Config:
        """Configure Settings to load a `.env` file if present."""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
