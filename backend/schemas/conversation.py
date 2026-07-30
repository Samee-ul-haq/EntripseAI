from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from backend.schemas.message import MessageResponse


class ConversationBase(BaseModel):
    name : str


class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    name : Optional[str] = None


class ConversationResponse(BaseModel):
    id  : int
    workspace_id : int
    created_at : datetime
    updated_at : Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ConversationDetialResponse(ConversationResponse):
    messages : List[MessageResponse] = []
