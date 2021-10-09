from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from api.core.database import Base


class Nomination(Base):
    """A general helper nomination information created by staff."""

    __tablename__ = 'nomination'

    # Whether this nomination is still relevant.
    active = Column(Boolean, nullable=False)

    user_id = Column(ForeignKey('user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    # The creation date of this nomination.
    inserted_at = Column(DateTime(True), nullable=False, default=datetime.now)

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Why the nomination was ended.
    end_reason = Column(Text, nullable=False)

    # When the nomination was ended.
    ended_at = Column(DateTime(True))

    # Whether a review was made.
    reviewed = Column(Boolean, nullable=False, default=False)

    # The nominated user.
    user = relationship('User', cascade="all, delete")
