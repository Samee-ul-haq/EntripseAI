from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullabe=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullabe=False)

    user = relationship("User", back_populates="workspace")
    conversations = relationship("Conversation", back_populates="workspace", cascade="all, delete-orphan")
    documents =  relationship("Documment", back_populate="workspace", cascade="all, delete-orphan")
