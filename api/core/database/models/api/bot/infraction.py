from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.orm import relationship

from api.core.database import Base


class ApiInfraction(Base):
    """An infraction for a Discord user."""

    __tablename__ = 'api_infraction'
    __table_args__ = (
        Index('unique_active_infraction_per_type_per_user', 'user_id', 'type', unique=True),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('api_infraction_id_seq'::regclass)"))
    inserted_at = Column(DateTime(True), nullable=False)
    expires_at = Column(DateTime(True))
    active = Column(Boolean, nullable=False)
    type = Column(String(9), nullable=False)
    reason = Column(Text)
    hidden = Column(Boolean, nullable=False)
    actor_id = Column(ForeignKey('api_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    user_id = Column(ForeignKey('api_user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    actor = relationship('ApiUser', primaryjoin='ApiInfraction.actor_id == ApiUser.id')
    user = relationship('ApiUser', primaryjoin='ApiInfraction.user_id == ApiUser.id')
