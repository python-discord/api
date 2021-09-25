from typing import NoReturn, Union

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import validates

from api.core.database import Base


class FilterList(Base):
    """An item that is either allowed or denied."""

    __tablename__ = 'filterlist'
    __table_args__ = (
        UniqueConstraint('content', 'type'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    type = Column(String(50), nullable=False)
    allowed = Column(Boolean, nullable=False)
    content = Column(Text, nullable=False)
    comment = Column(Text)

    @validates('type')
    def validate_type(self, _key: str, typeval: str) -> Union[str, NoReturn]:
        """Raise ValueError if the provided type is not in the list of valid types."""
        choices = ('GUILD_INVITE', 'FILE_FORMAT', 'DOMAIN_NAME', 'FILTER_TOKEN')
        if typeval not in choices:
            raise ValueError(f"{typeval} is not a valid FilterList type")
        return typeval
