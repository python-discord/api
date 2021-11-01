from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.orm import relationship

from api.core.database import Base


class DeletedMessage(Base):
    """A deleted message, previously sent somewhere on the Discord server."""

    __tablename__ = "api_deletedmessage"

    id = Column(BigInteger, primary_key=True)
    deletion_context_id = Column(
        ForeignKey(
            "api_messagedeletioncontext.id",
            deferrable=True,
            initially="DEFERRED",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # The deletion context this message is part of.
    deletion_context = relationship("MessageDeletionContext", passive_deletes=True)
