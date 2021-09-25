from typing import NoReturn, Union

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from api.core.database import Base


class Infraction(Base):
    """An infraction for a Discord user."""

    __tablename__ = 'infraction'
    __table_args__ = (
        Index('unique_active_infraction_per_type_per_user', 'user_id', 'type', unique=True),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    inserted_at = Column(DateTime(True), nullable=False)
    expires_at = Column(DateTime(True))
    active = Column(Boolean, nullable=False)
    type = Column(String(9), nullable=False)
    reason = Column(Text)
    hidden = Column(Boolean, nullable=False)
    actor_id = Column(ForeignKey('user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)
    user_id = Column(ForeignKey('user.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    actor = relationship('User', primaryjoin='Infraction.actor_id == User.id')
    user = relationship('User', primaryjoin='Infraction.user_id == User.id')

    @validates('type')
    def validate_type(self, _key: str, infrtype: str) -> Union[str, NoReturn]:
        """Raise ValueError if the provided Infranction type is not in the list of supported types."""
        type_choices = ("note", "warning", "watch", "mute", "kick", "ban", "superstar", "voice_ban")
        if infrtype not in type_choices:
            raise ValueError(f"{infrtype} is not a valid Infraction type!")
        return infrtype
