from sqlalchemy.orm import Session
from backend.models.workspaces import Workspace
from backend.schemas.workspace import WorkspaceCreate, WorkspaceUpdate
from typing import Optional, List



def create_workspace(db : Session,
                      workspace : WorkspaceCreate,
                        owner_id : int,
                        ) -> Workspace :
    db_workspace = Workspace(
        name = workspace.name,
        description = workspace.description,
        user_id = owner_id
    )

    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)

    return db_workspace



def get_user_workspace(db : Session,
                        owner_id : int, 
                        skip : int = 0, 
                        limit : int = 100,
                          ) -> List[Workspace] :
    return (db.query(Workspace)
        .filter(Workspace.user_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
        )



def get_workspace_by_id(db: Session, 
                        workspace_id : int, 
                        owner_id : int,
                        ) -> Optional[Workspace]:
    return (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id, Workspace.user_id == owner_id)
        .first()
    )


def update_workspace(db : Session, 
                     workspace_id : int,
                    workspace_data : WorkspaceUpdate, 
                    owner_id : int) -> Optional[Workspace]:
    db_workspace = get_workspace_by_id(db, workspace_id=workspace_id, owner_id=owner_id)
    if not db_workspace:
        return None

    update_dict = workspace_data.model_dump(exclude_unset = True)

    # Only update fields that were explicitly sent in the request body
    for key, value in update_dict.items():
        setattr(db_workspace, key, value)

    db.commit()
    db.refresh(db_workspace)
    return db_workspace


def delete_workspace(db : Session, workspace_id : int, owner_id : int) -> bool:
    db_workspace = get_workspace_by_id(db, workspace_id, owner_id)

    if not db_workspace:
        return False

    db.delete(db_workspace)
    db.commit()
    return True
