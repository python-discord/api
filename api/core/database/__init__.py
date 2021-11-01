"""
The database package of the Python Discord API.

This package contains the ORM models, migrations, and
other functionality related to database interop.
"""
from unittest.mock import Mock

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from api.core.settings import settings

Base = declarative_base()
metadata = Base.metadata

if settings.TESTING:
    session_factory = Mock()
else:
    engine = create_engine(settings.database_url)
    session_factory = sessionmaker(bind=engine)
