from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import validates

from api.core.database import Base


class Role(Base):
    """
    A role on our Discord server.

    The comparison operators <, <=, >, >=, ==, != act the same as they do with Role-objects of the
    discord.py library, see https://discordpy.readthedocs.io/en/latest/api.html#discord.Role
    """

    __tablename__ = 'role'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    colour = Column(Integer, nullable=False)
    permissions = Column(BigInteger, nullable=False)
    position = Column(Integer, nullable=False)

    @validates('id')
    def validate_role_id(self, _, role_id: int):
        if role_id < 0:
            raise ValueError("Role IDs cannot be negative.")

    @validates('colour')
    def validate_colour(self, _, colour: int):
        if colour < 0:
            raise ValueError("Colour hex cannot be negative.")
        else:
            return colour

    @validates('permissions')
    def validate_permission(self, _, permission: int):
        if permission < 0:
            raise ValueError("Role permissions cannot be negative.")
        else:
            return permission
