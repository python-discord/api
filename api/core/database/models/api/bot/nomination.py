from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from api.core.database import Base


class Nomination(Base):
    """A general helper nomination information created by staff."""

    __tablename__ = 'nomination'

    active = Column(Boolean, nullable=False)
    user_id = Column(ForeignKey('user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    inserted_at = Column(DateTime(True), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    end_reason = Column(Text, nullable=False)
    ended_at = Column(DateTime(True))
    reviewed = Column(Boolean, nullable=False)

    user = relationship('User')
