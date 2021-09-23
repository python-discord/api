from typing import NoReturn, Union

from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import validates

from api.core.database import Base


class BotSetting(Base):
    """A configuration entry for the bot."""

    __tablename__ = 'botsetting'

    name = Column(String(50), primary_key=True, index=True)
    data = Column(JSONB(astext_type=Text()), nullable=False)

    @validates('name')
    def validate_name(self, _, name: str) -> Union[None, NoReturn]:
        known_settings = (
            'defcon',
            'news',
        )
        if name not in known_settings:
            raise ValueError(f"`{name}` is not a known bot setting name.")
