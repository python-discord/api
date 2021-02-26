from pydantic import BaseSettings


class Settings(BaseSettings):
    auth_token: str
    DEBUG: bool = False


settings = Settings()
