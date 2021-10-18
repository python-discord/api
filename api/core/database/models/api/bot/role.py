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

    __tablename__ = "role"

    # The role ID, taken from Discord.
    id = Column(BigInteger, primary_key=True)

    # The role name, taken from Discord.
    name = Column(String(100), nullable=False)

    # The integer value of the colour of this role from Discord.
    colour = Column(Integer, nullable=False)

    # The integer value of the permission bitset of this role from Discord.
    permissions = Column(BigInteger, nullable=False)

    # The position of the role in the role hierarchy of the Discord Guild.
    position = Column(Integer, nullable=False)

    def __lt__(self, other: "Role") -> bool:
        """Compares the roles based on their position in the role hierarchy of the guild."""
        return self.position < other.position

    def __le__(self, other: "Role") -> bool:
        """Compares the roles based on their position in the role hierarchy of the guild."""
        return self.position <= other.position

    @validates("id")
    def validate_role_id(self, _key: str, role_id: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided id is negative."""
        if role_id < 0:
            raise ValueError("Role IDs cannot be negative.")
        return role_id

    @validates("colour")
    def validate_colour(self, _key: str, colour: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided colour hex is negative."""
        if colour < 0 or colour > 16_777_216:
            raise ValueError(
                "Colour hex cannot be negative, or reach the total hex combinations available."
            )
        return colour

    @validates("permissions")
    def validate_permission(self, _key: str, permission: int) -> Union[int, NoReturn]:
        """Raise ValueError if the provided permission code is negative."""
        if permission < 0:
            raise ValueError("Role permissions cannot be negative.")
        return permission
