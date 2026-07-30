from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.message import Message
from backend.schemas.message import MessageResponse, MessageCreate
from .conversation import get_conversation_by_id


def create_message(
    db: Session, 
    message: MessageCreate, 
    conversation_id: int, 
    user_id: int
) -> Optional[Message]:
    """Appends a new message to a conversation after validating workspace ownership."""
    conversation = get_conversation_by_id(db, conversation_id=conversation_id, user_id=user_id)
    if not conversation:
        return None

    db_message = Message(
        content=message.content,
        sender_type=message.sender_type,
        conversation_id=conversation_id,
        model_name=message.model_name,
        tokens_used=message.tokens_used,
        latency_ms=message.latency_ms,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message



def get_conversation_messages(
    db: Session, 
    conversation_id: int, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[Message]:
    """Retrieves all messages for a thread, ordered chronologically."""
    conversation = get_conversation_by_id(db, conversation_id=conversation_id, user_id=user_id)
    if not conversation:
        return []

    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )

