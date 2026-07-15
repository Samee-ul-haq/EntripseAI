from sqlalchemy import Column, Integer, String, Foreignkey
from sqlalchemy.orm import relationship

from backend.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    conversation_id = Column(Integer, Foreignkey("conversations.id"),nullable=False)

    conversation = relationship("Conversation", back_populate="message")