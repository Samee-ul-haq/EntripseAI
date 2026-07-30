from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.schemas.message import MessageResponse,  MessageCreate
from backend.routes.user import get_current_user
from backend.database import get_db
from backend.models import User
from backend.crud.message import crud_message


router = APIRouter(tags=["Messages"])


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_message(
    conversation_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Append a message to an existing conversation thread."""
    db_message = crud_message.create_message(
        db=db, message=message, conversation_id=conversation_id, user_id=current_user.id
    )
    if not db_message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or unauthorized",
        )
    return db_message


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=List[MessageResponse],
)
def read_conversation_messages(
    conversation_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve message history for a conversation chronologically."""
    return crud_message.get_conversation_messages(
        db=db, conversation_id=conversation_id, user_id=current_user.id, skip=skip, limit=limit
    )