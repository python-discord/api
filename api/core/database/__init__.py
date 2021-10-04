"""
The database package of the Python Discord API.

This package contains the ORM models, migrations, and
other functionality related to database interop.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata
