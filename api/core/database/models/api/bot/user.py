from typing import NoReturn, Union

from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    CheckConstraint,
    Column,
    SmallInteger,
    String,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, validates

from api.core.database import Base
from api.core.settings import settings
from .role import Role

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    """A Discord user."""

    __tablename__ = "api_user"
    __table_args__ = (CheckConstraint("discriminator >= 0"),)

    # The ID of this user, taken from Discord.
    id = Column(BigInteger, primary_key=True)

    # The username, taken from Discord.
    name = Column(String(32), nullable=False)

    # Discriminators may not exceed `9999`."
    discriminator = Column(SmallInteger, nullable=False)

    # Whether this user is in our server.
    in_guild = Column(Boolean, nullable=False, default=True)

    # IDs of roles the user has on the server
    roles = Column(ARRAY(BigInteger()), nullable=False, default=[])

    @validates("id")
    def validate_user_id(self, _key: str, user_id: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided id is negative."""
        if user_id < 0:
            raise ValueError("User IDs cannot be negative.")
        return user_id

    @validates("discriminator")
    def validate_discriminator(
        self, _key: str, discriminator: int
    ) -> Union[int, NoReturn]:
        """Raise ValueError if the provided discriminator is exceeds `9999`."""
        if discriminator > 9999 or discriminator <= 0:
            raise ValueError("Discriminators may not exceed `9999` or be below `0001`.")
        return discriminator

    @validates("roles")
    def validate_roles(self, _key: str, roles: list[int]) -> Union[list[int], NoReturn]:
        """Raise ValueError if the provided role(s) is negative or non-existent."""
        session = SessionLocal()
        for role in roles:
            if role < 0:
                raise ValueError("Role IDs cannot be negative")
            if not session.query(Role).filter_by(id=role).first():
                raise ValueError(f"Role with ID {role} does not exist")
        return roles
