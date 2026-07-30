from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.user import User
from backend.routes.user import get_current_user
from backend.schemas.conversation import (
    ConversationCreate,
    ConversationDetailResponse,
    ConversationResponse,
    ConversationUpdate,
    MessageCreate,
    MessageResponse,
)
import backend.crud.conversation as crud_conversation

router = APIRouter(
    tags=["Conversations & Messages"]
)


# ==========================================
# CONVERSATION ENDPOINTS
# ==========================================

@router.post(
    "/workspaces/{workspace_id}/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_conversation(
    workspace_id: int,
    conversation: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new conversation thread inside a specific workspace."""
    db_conversation = crud_conversation.create_conversation(
        db=db, conversation=conversation, workspace_id=workspace_id, user_id=current_user.id
    )
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found or unauthorized",
        )
    return db_conversation


@router.get(
    "/workspaces/{workspace_id}/conversations",
    response_model=List[ConversationResponse],
)
def read_workspace_conversations(
    workspace_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve all conversation threads inside a workspace."""
    return crud_conversation.get_workspace_conversations(
        db=db, workspace_id=workspace_id, user_id=current_user.id, skip=skip, limit=limit
    )


@router.get(
    "/conversations/{conversation_id}",
    response_model=ConversationDetailResponse,
)
def read_conversation_detail(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve a specific conversation along with its full message history."""
    db_conversation = crud_conversation.get_conversation_by_id(
        db=db, conversation_id=conversation_id, user_id=current_user.id
    )
    if not db_conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or unauthorized",
        )
    return db_conversation


@router.put(
    "/conversations/{conversation_id}",
    response_model=ConversationResponse,
)
def update_conversation(
    conversation_id: int,
    conversation: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Rename a conversation thread."""
    updated = crud_conversation.update_conversation(
        db=db, conversation_id=conversation_id, conversation_data=conversation, user_id=current_user.id
    )
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or unauthorized",
        )
    return updated


@router.delete(
    "/conversations/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a conversation thread and all its messages."""
    success = crud_conversation.delete_conversation(
        db=db, conversation_id=conversation_id, user_id=current_user.id
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or unauthorized",
        )
    return None


#