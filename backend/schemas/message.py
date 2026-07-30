from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MessageBase(BaseModel):
    content : str
    role : str


class MessageCreate(MessageBase):
    model_name : Optional[str] = None
    tokens_used : Optional[str] = None
    latency_ms  : Optional[str] = None


class MessageResponse(MessageBase):
    id : int
    convesation_id : int
    created_at : datetime
    model_name : Optional[str] = None
    tokens_used : Optional[str] = None
    latency_ms  : Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

