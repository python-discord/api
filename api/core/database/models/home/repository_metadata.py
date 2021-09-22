from sqlalchemy import Column, DateTime, Integer, String

from api.core.database import Base


class RepositoryMetaData(Base):
    """Information about one of our repos fetched from the GitHub API."""

    __tablename__ = 'repositorymetadata'

    last_updated = Column(DateTime(True), nullable=False)
    repo_name = Column(String(40), primary_key=True, index=True)
    description = Column(String(400), nullable=False)
    forks = Column(Integer, nullable=False)
    stargazers = Column(Integer, nullable=False)
    language = Column(String(20), nullable=False)
