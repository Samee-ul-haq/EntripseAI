from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class WorkspaceBase(BaseModel):
    name : str
    description : Optional[str] = None


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceUpdate(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None


class WorksapceResponse(WorkspaceBase):
    id : int
    user_id : int
    created_at : datetime
    updated_at : Optional[datetime] = None
    # Enable ORM mode so Pydantic can read SQLAlchemy model attributes directly
    model_config = ConfigDict(from_attributes=True)