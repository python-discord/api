import datetime
from typing import NoReturn, Union

from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.orm import validates

from api.core.database import Base


class OffensiveMessage(Base):
    """A message that triggered a filter and that will be deleted one week after it was sent."""

    __tablename__ = 'offensivemessage'

    id = Column(BigInteger, primary_key=True)

    # The channel ID that the message was
    # sent in, taken from Discord.
    channel_id = Column(BigInteger, nullable=False)

    # The date on which the message will be auto-deleted.
    delete_date = Column(DateTime(True), nullable=False)

    @validates('id')
    def validate_ofmessage_id(self, _key: str, message_id: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided id is negative."""
        if message_id < 0:
            raise ValueError("Message IDs cannot be negative.")
        return message_id

    @validates('channel_id')
    def validate_ofchannel_id(self, _key: str, channel_id: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided id is negative."""
        if channel_id < 0:
            raise ValueError("Channel IDs cannot be negative.")
        return channel_id

    @validates('delete_date')
    def future_date_validator(self, _key: str, date: datetime.date) -> Union[datetime.date, NoReturn]:
        """Raise ValueError if the date isn't a future date."""
        if date < datetime.datetime.now(datetime.timezone.utc):
            raise ValueError("Date must be a future date")
        return date
