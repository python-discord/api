from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class ReminderResponse(BaseModel):
    """Scheme representing a response for a Reminder."""

    active: bool
    author: int = Field(alias="author_id")
    mentions: list[int]
    content: str
    expiration: datetime  # ISO-formatted datetime
    id: int
    channel_id: int
    jump_url: str

    @validator("expiration")
    def parse_expiration(cls, value: datetime) -> str:  # noqa N805
        """A parser that transforms datetimes into isoformat."""
        return value.isoformat()

    class Config:
        """Configuration class to enable ORM mode."""

        allow_population_by_field_name = False
        orm_mode = True


class ReminderCreateIn(BaseModel):
    """A model representing an incoming Reminder on creation."""

    author_id: int = Field(alias="author")
    mentions: list[int]
    content: str
    expiration: datetime  # ISO-formatted datetime
    channel_id: int
    jump_url: str


class ReminderPatchIn(BaseModel):
    """A model representing a batch of data what has to be updated on a Reminder."""

    mentions: Optional[list[int]] = Field(None)
    content: Optional[str] = Field(None)
    expiration: Optional[str] = Field(None)  # ISO-formatted datetime


class ReminderFilter(BaseModel):
    """A schema representing possible choices for filtering Reminder queries."""

    author_id: Optional[int] = Field(alias="author__id")
    active: Optional[bool]
