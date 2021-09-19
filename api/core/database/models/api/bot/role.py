from sqlalchemy import BigInteger, Column, Integer, String

from api.core.database import Base


class Role(Base):

    """
    A role on our Discord server.
    The comparison operators <, <=, >, >=, ==, != act the same as they do with Role-objects of the
    discord.py library, see https://discordpy.readthedocs.io/en/latest/api.html#discord.Role
    """

    __tablename__ = 'api_role'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    colour = Column(Integer, nullable=False)
    permissions = Column(BigInteger, nullable=False)
    position = Column(Integer, nullable=False)
