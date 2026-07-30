from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base
from sqlalchemy.sql import func

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    content = Column(Text , nullable=True)
    
    #Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    

    workspace = relationship("Workspace", back_populates="conversations")
    messages  =  relationship("Message",  back_populates="conversation", cascade="all, delete-orphan")