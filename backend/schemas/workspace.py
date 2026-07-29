from datetime import datetime
from typing import Optional
from pydatic import BaseModel, ConfigDict


class WorkspaceBase(BaseModel):
    title : str
    description : Optional[str] = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None


class WorksapceResponse(WorkspaceBase):
    id : int
    owner_id : int
    created_at : datetime
    updated_at : Optional[datetime] = None
    # Enable ORM mode so Pydantic can read SQLAlchemy model attributes directly
    model_config = ConfigDict(from_attributes=True)