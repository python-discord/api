import re
from typing import Union, NoReturn

from sqlalchemy import Column, String
from sqlalchemy.orm import validates
from api.core.database import Base


class DocumentationLink(Base):
    """A documentation link used by the `!docs` command of the bot."""

    __tablename__ = 'documentationlink'

    package = Column(String(50), primary_key=True, index=True)
    base_url = Column(String(200), nullable=False)
    inventory_url = Column(String(200), nullable=False)

    @validates('base_url')
    def validate_base_url(self, _, url: str) -> Union[None, NoReturn]:
        if not url.endswith("/"):
            raise ValueError("The entered URL must end with a slash.")

    @validates('package')
    def validate_package(self, _, package: str) -> Union[None, NoReturn]:
        pattern = re.compile(r"^[a-z0-9_]+$")
        if not pattern.match(package):
            raise ValueError("Package names can only consist of lowercase a-z letters, digits, and underscores.")
