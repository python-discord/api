from sqlalchemy import ARRAY, BigInteger, Boolean, CheckConstraint, Column, SmallInteger, String

from api.core.database import Base


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
