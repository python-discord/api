import datetime

from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.orm import validates

from api.core.database import Base


class OffensiveMessage(Base):
    """A message that triggered a filter and that will be deleted one week after it was sent."""

    __tablename__ = 'offensivemessage'

    id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger, nullable=False)
    delete_date = Column(DateTime(True), nullable=False)

    @validates('id')
    def validate_ofmessage_id(self, _, message_id: int) -> None:
        if message_id < 0:
            raise ValueError("Message IDs cannot be negative.")

    @validates('channel_id')
    def validate_ofchannel_id(self, _, channel_id: int) -> None:
        if channel_id < 0:
            raise ValueError("Channel IDs cannot be negative.")

    @validates('delete_date')
    def future_date_validator(self, date: datetime.date) -> None:
        """Raise ValidationError if the date isn't a future date."""
        if date < datetime.datetime.now(datetime.timezone.utc):
            raise ValueError("Date must be a future date")
