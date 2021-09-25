from typing import NoReturn, Union

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
    def validate_role_id(self, _key: str, role_id: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided id is negative."""
        if role_id < 0:
            raise ValueError("Role IDs cannot be negative.")
        return role_id

    @validates('colour')
    def validate_colour(self, _key: str, colour: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided colour hex is negative."""
        if colour < 0:
            raise ValueError("Colour hex cannot be negative.")
        return colour

    @validates('permissions')
    def validate_permission(self, _key: str, permission: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided permission code is negative."""
        if permission < 0:
            raise ValueError("Role permissions cannot be negative.")
        return permission
