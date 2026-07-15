from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    role = Column(String, nullable=False)

    conversation_id = Column(Integer, ForeignKey("conversations.id"),nullable=False)

    conversation = relationship("Conversation", back_populates="messages")