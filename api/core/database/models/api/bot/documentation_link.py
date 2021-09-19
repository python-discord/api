from sqlalchemy import Column, String

from api.core.database import Base


class DocumentationLink(Base):
    """A documentation link used by the `!docs` command of the bot."""

    __tablename__ = 'api_documentationlink'

    package = Column(String(50), primary_key=True, index=True)
    base_url = Column(String(200), nullable=False)
    inventory_url = Column(String(200), nullable=False)
