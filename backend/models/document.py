from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    workspace = relationship("Workspace", back_populates="documents")