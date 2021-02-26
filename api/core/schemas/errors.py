from pydantic import BaseModel


class ErrorMessage(BaseModel):
    error: str
