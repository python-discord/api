from sqlalchemy import ARRAY, BigInteger, Boolean, CheckConstraint, Column, SmallInteger, String
from sqlalchemy import create_engine
from sqlalchemy.orm import validates, sessionmaker

from api.core.database import Base
from .role import Role
from api.core.settings import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    """A Discord user."""

    __tablename__ = 'user'
    __table_args__ = (
        CheckConstraint('discriminator >= 0'),
    )

    id = Column(BigInteger, primary_key=True)
    name = Column(String(32), nullable=False)
    discriminator = Column(SmallInteger, nullable=False)
    in_guild = Column(Boolean, nullable=False)
    roles = Column(ARRAY(BigInteger()), nullable=False)

    @validates('id')
    def validate_user_id(self, _, user_id: int) -> None:
        if user_id < 0:
            raise ValueError("User IDs cannot be negative.")

    @validates('discriminator')
    def validate_discriminator(self, _, discriminator: int) -> None:
        if discriminator > 9999:
            raise ValueError("Discriminators may not exceed `9999`.")
        return discriminator

    @validates('roles')
    def validate_roles(self, _, roles: list[int]) -> None:
        session = SessionLocal()
        for role in roles:
            if role < 0:
                raise ValueError("Role IDs cannot be negative")
            if not session.query(Role).filter_by(id=role).first():
                raise ValueError(f"Role with ID {role} does not exist")
        return roles
