from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from api.core.database import Base


class Nominationentry(Base):
    """A nomination entry created by a single staff member."""

    __tablename__ = "api_nominationentry"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Why the actor nominated this user.
    reason = Column(Text, nullable=False)

    # The creation date of this nomination entry.
    inserted_at = Column(DateTime(True), nullable=False, default=datetime.now)

    actor_id = Column(
        ForeignKey(
            "api_user.id", deferrable=True, initially="DEFERRED", ondelete="CASCADE"
        ),
        nullable=False,
        index=True,
    )
    nomination_id = Column(
        ForeignKey(
            "api_nomination.id",
            deferrable=True,
            initially="DEFERRED",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # The staff member that nominated this user.
    actor = relationship("User", passive_deletes=True)

    # "The nomination this entry belongs to.
    nomination = relationship("Nomination", passive_deletes=True)
