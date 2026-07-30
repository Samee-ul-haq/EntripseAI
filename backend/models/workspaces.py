from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from backend.database import Base
from sqlalchemy.sql import func

class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    #Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    user = relationship("User", back_populates="workspaces")
    conversations = relationship("Conversation", back_populates="workspace", cascade="all, delete-orphan")
    documents =  relationship("Document", back_populates="workspace", cascade="all, delete-orphan")
