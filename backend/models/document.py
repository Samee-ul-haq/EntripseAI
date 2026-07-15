from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database import Base

class Document(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    conversation_id = Column(Integer, ForeignKey("workspace.id"))
    workspace = relationship("Workspace", back_populate="document")