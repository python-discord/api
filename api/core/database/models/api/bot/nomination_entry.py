from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from api.core.database import Base


class ApiNominationentry(Base):
    """A nomination entry created by a single staff member."""

    __tablename__ = 'nominationentry'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reason = Column(Text, nullable=False)
    inserted_at = Column(DateTime(True), nullable=False)
    actor_id = Column(ForeignKey('api_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    nomination_id = Column(
        ForeignKey('nomination.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True
    )

    actor = relationship('User')
    nomination = relationship('Nomination')
