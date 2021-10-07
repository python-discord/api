

from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.orm import relationship


from api.core.database import Base


class DeletedMessage(Base):
    """A deleted message, previously sent somewhere on the Discord server."""

    __tablename__ = 'deletedmessage'

    id = Column(BigInteger, primary_key=True)
    deletion_context_id = Column(
        ForeignKey('messagedeletioncontext.id', deferrable=True, initially='DEFERRED'),
        nullable=False,
        index=True
    )

    # The deletion context this message is part of.
    deletion_context = relationship('MessageDeletionContext', cascade="all, delete")
