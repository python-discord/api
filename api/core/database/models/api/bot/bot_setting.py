from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from api.core.database import Base


class ApiBotsetting(Base):
    """A configuration entry for the bot."""

    __tablename__ = 'api_botsetting'

    name = Column(String(50), primary_key=True, index=True)
    data = Column(JSONB(astext_type=Text()), nullable=False)
