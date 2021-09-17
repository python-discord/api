from sqlalchemy import Boolean, Column, String

from api.core.database import Base


class ApiOfftopicchannelname(Base):
    """An off-topic channel name, used during the daily channel name shuffle."""

    __tablename__ = 'api_offtopicchannelname'

    name = Column(String(96), primary_key=True, index=True)
    used = Column(Boolean, nullable=False)
