from pydantic import BaseModel


class ConversationBase(BaseModel):
    name = str
