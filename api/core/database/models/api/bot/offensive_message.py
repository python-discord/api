from sqlalchemy import BigInteger, Column, DateTime

from api.core.database import Base


class OffensiveMessage(Base):
    """A message that triggered a filter and that will be deleted one week after it was sent."""

    __tablename__ = 'api_offensivemessage'

    id = Column(BigInteger, primary_key=True)
    channel_id = Column(BigInteger, nullable=False)
    delete_date = Column(DateTime(True), nullable=False)
