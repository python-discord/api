from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.orm import relationship

from api.core.database import Base


class ApiNomination(Base):
    """A general helper nomination information created by staff."""

    __tablename__ = 'api_nomination'

    active = Column(Boolean, nullable=False)
    user_id = Column(ForeignKey('api_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    inserted_at = Column(DateTime(True), nullable=False)
    id = Column(Integer, primary_key=True, server_default=text("nextval('api_nomination_id_seq'::regclass)"))
    end_reason = Column(Text, nullable=False)
    ended_at = Column(DateTime(True))
    reviewed = Column(Boolean, nullable=False)

    user = relationship('ApiUser')
