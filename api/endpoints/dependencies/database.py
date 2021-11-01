from api.core.database import session_factory


def create_database_session() -> None:
    """A FastAPI dependency that creates an SQLAlchemy session."""
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
