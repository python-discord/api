from sqlalchemy import ARRAY, BigInteger, Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from api.core.database import Base


class Message(Base):
    """A message, sent somewhere on the Discord server."""

    __tablename__ = 'message'

    id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger, nullable=False)
    content = Column(String(4000), nullable=False)
    embeds = Column(ARRAY(JSONB(astext_type=Text())), nullable=False)
    author_id = Column(ForeignKey('user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    attachments = Column(ARRAY(String(length=512)), nullable=False)

    author = relationship('User')

    @validates('id')
    def validate_message_id(self, _, message_id: int) -> None:
        if message_id < 0:
            raise ValueError("Message IDs cannot be negative.")

    @validates('channel_id')
    def validate_channel_id(self, _, channel_id: int) -> None:
        if channel_id < 0:
            raise ValueError("Channel IDs cannot be negative.")
