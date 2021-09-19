from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, UniqueConstraint, text

from api.core.database import Base


class FilterList(Base):
    """An item that is either allowed or denied."""

    __tablename__ = 'api_filterlist'
    __table_args__ = (
        UniqueConstraint('content', 'type'),
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('api_filterlist_id_seq'::regclass)"))
    created_at = Column(DateTime(True), nullable=False)
    updated_at = Column(DateTime(True), nullable=False)
    type = Column(String(50), nullable=False)
    allowed = Column(Boolean, nullable=False)
    content = Column(Text, nullable=False)
    comment = Column(Text)
