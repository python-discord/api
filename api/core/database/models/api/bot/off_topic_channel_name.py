import re

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import validates

from api.core.database import Base


class OffTopicChannelName(Base):
    """An off-topic channel name, used during the daily channel name shuffle."""

    __tablename__ = 'offtopicchannelname'

    name = Column(String(96), primary_key=True, index=True)
    used = Column(Boolean, nullable=False)

    @validates("name")
    def validate_name(self, _, name: str) -> None:
        if not re.match(r"^[a-z0-9\U0001d5a0-\U0001d5b9-ǃ？’']+$", name):
            raise ValueError(f"{name} is not a valid Off Topic channel name!")
        return name
