from typing import NoReturn, Union

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import validates

from api.core.database import Base


class BotSetting(Base):
    """A configuration entry for the bot."""

    __tablename__ = "api_botsetting"

    name = Column(String(50), primary_key=True, index=True)

    # The actual settings of this setting.
    data = Column(JSONB(astext_type=Text()), nullable=False)

    @validates("name")
    def validate_name(self, _key: str, name: str) -> Union[str, NoReturn]:
        """Raise ValueError if the provided name is not in the known settings."""
        known_settings = (
            "defcon",
            "news",
        )
        if name not in known_settings:
            raise ValueError(f"`{name}` is not a known bot setting name.")
        return name
