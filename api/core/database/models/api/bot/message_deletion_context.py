from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from api.core.database import Base


class MessageDeletionContext(Base):
    """
    Represents the context for a deleted message.

    The context includes its creation date, as well as the actor associated with the deletion.
    This helps to keep track of message deletions on the server.
    """

    __tablename__ = 'messagedeletioncontext'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # When this deletion took place.
    creation = Column(DateTime(True), nullable=False)

    actor_id = Column(ForeignKey('user.id', deferrable=True, initially='DEFERRED'), index=True)

    # The original actor causing this deletion. Could be the author
    # of a manual clean command invocation, the bot when executing
    # automatic actions, or nothing to indicate that the bulk
    # deletion was not issued by us.
    actor = relationship('User', cascade="all, delete")
