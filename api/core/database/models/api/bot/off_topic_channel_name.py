import re
from typing import NoReturn, Union

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import validates

from api.core.database import Base


class OffTopicChannelName(Base):
    """An off-topic channel name, used during the daily channel name shuffle."""

    __tablename__ = "offtopicchannelname"

    # The actual channel name that will be used on our Discord server.
    name = Column(String(96), primary_key=True, index=True)

    # Whether or not this name has already been used during this rotation
    used = Column(Boolean, nullable=False, default=False)

    @validates("name")
    def validate_name(self, _key: str, name: str) -> Union[str, NoReturn]:
        """Raise ValueError if the provided Off-topic name does not meet the conditions."""
        if not re.match(r"^[a-z0-9\U0001d5a0-\U0001d5b9-ǃ？’'＜＞]+$", name):
            raise ValueError(f"{name} is not a valid Off Topic channel name!")
        return name
