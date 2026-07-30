from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    role = Column(String, nullable = False)
    model_name = Column(String, nullable = True)
    tokens_used = Column(Integer , nullable = True)
    latency_ms = Column(Integer, nullable = True)

    #Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    

    conversation_id = Column(Integer, ForeignKey("conversations.id"),nullable=False)

    conversation = relationship("Conversation", back_populates="messages")