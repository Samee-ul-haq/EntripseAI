from sqlalchemy.orm import Session
from typing import Optional, List

from backend.models.conversation import Conversation
from backend.models.workspaces import Workspace
from backend.schemas.conversation import ConversationUpdate, ConversationResponse, ConversationCreate, ConversationDetialResponse


def create_conversation(
        db : Session,
        conversation : ConversationCreate,
        workspace_id : int,
        user_id : int
        ) -> Optional[Conversation]:

    """Creates a conversation inside a workspace if the user owns the workspace."""

    workspace = db.query(Workspace).filter(
                Workspace.id ==  workspace_id,
                workspace.user_id == user_id
    ).first()

    if not workspace:
        return None

    db_conversation = Conversation(
        name = conversation.name,
        workspace_id = workspace_id,
    )

    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)

    return db_conversation



def get_workspace_conversations(
        db : Session,
        worksapce_id : int,
        user_id : int,
        skip :  int = 0,
        limit : int = 100,
) ->  List[Conversation]:   
    """Lists all conversations in a workspace after verifying workspace ownership."""
    workspace = db.query(Workspace).filter(
        Workspace.id == worksapce_id,
        Workspace.user_id == user_id
    )
    if not workspace:
        return []

    return (
        db.query(Conversation)
        .filter(Conversation.workspace_id == worksapce_id)
        .order_by(Conversation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_conversation_by_id(
    db: Session, 
    conversation_id: int, 
    user_id: int
) -> Optional[Conversation]:
    """Retrieves a conversation ensuring it belongs to a workspace owned by user_id."""
    return (
        db.query(Conversation)
        .join(Workspace, Conversation.workspace_id == Workspace.id)
        .filter(Conversation.id == conversation_id, Workspace.user_id == user_id)
        .first()
    )


def update_conversation(
    db: Session, 
    conversation_id: int, 
    conversation_data: ConversationUpdate, 
    user_id: int
) -> Optional[Conversation]:
    """Updates a conversation title if the user owns the underlying workspace."""
    db_conversation = get_conversation_by_id(db, conversation_id=conversation_id, user_id=user_id)
    if not db_conversation:
        return None

    update_dict = conversation_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(db_conversation, field, value)

    db.commit()
    db.refresh(db_conversation)
    return db_conversation



def delete_conversation(db: Session, conversation_id: int, user_id: int) -> bool:
    """Deletes a conversation and its messages if the user owns the workspace."""
    db_conversation = get_conversation_by_id(db, conversation_id=conversation_id, user_id=user_id)
    if not db_conversation:
        return False

    db.delete(db_conversation)
    db.commit()
    return True

