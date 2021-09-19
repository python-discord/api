from sqlalchemy import Column, DateTime, ForeignKey, Integer, text
from sqlalchemy.orm import relationship

from api.core.database import Base


class MessageDeletionContext(Base):
    """
    Represents the context for a deleted message.

    The context includes its creation date, as well as the actor associated with the deletion.
    This helps to keep track of message deletions on the server.
    """

    __tablename__ = 'api_messagedeletioncontext'

    id = Column(
        Integer,
        primary_key=True,
        server_default=text("nextval('api_messagedeletioncontext_id_seq'::regclass)")
    )
    creation = Column(DateTime(True), nullable=False)
    actor_id = Column(ForeignKey('api_user.id', deferrable=True, initially='DEFERRED'), index=True)

    actor = relationship('ApiUser')
