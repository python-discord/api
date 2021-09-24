from sqlalchemy import ARRAY, BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from api.core.database import Base


class Reminder(Base):
    """A reminder created by a user."""

    __tablename__ = 'reminder'

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, nullable=False)
    channel_id = Column(BigInteger, nullable=False)
    content = Column(String(1500), nullable=False)
    expiration = Column(DateTime(True), nullable=False)
    author_id = Column(ForeignKey('user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    jump_url = Column(String(88), nullable=False)
    mentions = Column(ARRAY(BigInteger()), nullable=False)

    author = relationship('User')

    @validates('channel_id')
    def validate_rchannel_id(self, _, channel_id: int) -> None:
        if channel_id < 0:
            raise ValueError("Channel IDs cannot be negative.")
        return channel_id

    @validates('mentions')
    def validate_mentions(self, _, mentions: int) -> None:
        if mentions < 0:
            raise ValueError("Mention IDs cannot be negative.")
        return mentions
