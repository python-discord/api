from datetime import datetime
from typing import NoReturn, Union

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates

from api.core.database import Base


class Infraction(Base):
    """An infraction for a Discord user."""

    __tablename__ = "api_infraction"
    __table_args__ = (
        Index(
            "unique_active_infraction_per_type_per_user", "user_id", "type", unique=True
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    # The date and time of the creation of this infraction.
    inserted_at = Column(DateTime(True), nullable=False, default=datetime.now)

    # The date and time of the expiration of this infraction.
    # Null if the infraction is permanent or it can't expire.
    expires_at = Column(DateTime(True))

    # Whether the infraction is still active.
    active = Column(Boolean, nullable=False)

    # The type of the infraction.
    type = Column(String(10), nullable=False)

    # The reason for the infraction.
    reason = Column(Text)

    # Whether the infraction is a shadow infraction.
    hidden = Column(Boolean, nullable=False)

    actor_id = Column(
        ForeignKey("api_user.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    user_id = Column(
        ForeignKey("api_user.id", deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )

    # The user which applied the infraction.
    actor = relationship(
        "User", primaryjoin="Infraction.actor_id == User.id", cascade="all, delete"
    )

    # The user to which the infraction was applied.
    user = relationship(
        "User", primaryjoin="Infraction.user_id == User.id", cascade="all, delete"
    )

    @validates("type")
    def validate_type(self, _key: str, infrtype: str) -> Union[str, NoReturn]:
        """Raise ValueError if the provided Infranction type is not in the list of supported types."""
        type_choices = (
            "note",
            "warning",
            "watch",
            "mute",
            "kick",
            "ban",
            "superstar",
            "voice_ban",
            "voice_mute",
        )
        if infrtype not in type_choices:
            raise ValueError(f"{infrtype} is not a valid Infraction type!")
        return infrtype
