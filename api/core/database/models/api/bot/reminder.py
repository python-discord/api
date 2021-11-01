from typing import NoReturn, Union

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from api.core.database import Base


class Reminder(Base):
    """A reminder created by a user."""

    __tablename__ = "api_reminder"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Whether this reminder is still active.
    # If not, it has been sent out to the user.
    active = Column(Boolean, nullable=False, default=True)
    # The channel ID that this message was
    # sent in, taken from Discord.
    channel_id = Column(BigInteger, nullable=False)

    # The content that the user wants to be reminded of.
    content = Column(String(1500), nullable=False)

    # When this reminder should be sent.
    expiration = Column(DateTime(True), nullable=False)

    # Number of times we attempted to send the reminder and failed.
    failures = Column(Integer, default=0, nullable=False)

    author_id = Column(
        ForeignKey(
            "api_user.id", deferrable=True, initially="DEFERRED", ondelete="CASCADE"
        ),
        nullable=False,
        index=True,
    )

    # The jump url to the message that created the reminder
    jump_url = Column(String(88), nullable=False)
    # IDs of roles or users to ping with the reminder.
    mentions = Column(ARRAY(BigInteger()), nullable=False, default=[])

    # The creator of this reminder.
    author = relationship("User", passive_deletes=True)

    @validates("channel_id")
    def validate_rchannel_id(self, _key: str, channel_id: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided id is negative."""
        if channel_id < 0:
            raise ValueError("Channel IDs cannot be negative.")
        return channel_id

    @validates("mentions")
    def validate_mentions(
        self, _key: str, mentions: list[int]
    ) -> Union[list[int], NoReturn]:
        """Raise ValueError if either of the provided mentions is negative."""
        for mention in mentions:
            if mention < 0:
                raise ValueError("Mention IDs cannot be negative.")
        return mentions
