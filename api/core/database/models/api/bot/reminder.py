from sqlalchemy import ARRAY, BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from api.core.database import Base


class Reminder(Base):
    """A reminder created by a user."""

    __tablename__ = 'api_reminder'

    id = Column(Integer, primary_key=True, server_default=text("nextval('api_reminder_id_seq'::regclass)"))
    active = Column(Boolean, nullable=False)
    channel_id = Column(BigInteger, nullable=False)
    content = Column(String(1500), nullable=False)
    expiration = Column(DateTime(True), nullable=False)
    author_id = Column(ForeignKey('api_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    jump_url = Column(String(88), nullable=False)
    mentions = Column(ARRAY(BigInteger()), nullable=False)

    author = relationship('ApiUser')
