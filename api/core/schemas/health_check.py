from pydantic import BaseModel


class HealthCheck(BaseModel):
    description: str
    timestamp: int
