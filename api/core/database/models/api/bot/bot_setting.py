from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from api.core.database import Base


class BotSetting(Base):
    """A configuration entry for the bot."""

    __tablename__ = 'botsetting'

    name = Column(String(50), primary_key=True, index=True)
    data = Column(JSONB(astext_type=Text()), nullable=False)
