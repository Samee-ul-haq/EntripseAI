from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List


from backend.schemas.workspace import WorksapceResponse, WorkspaceCreate, WorkspaceUpdate
from backend.routes.user import get_current_user
from backend.models.user import User
from backend.database import get_db
import backend.crud.workspace as crud_workspace


router =  APIRouter(prefix = "/workspaces", tags = ['Workspaces'])


@router.post("/", response_model = WorksapceResponse, status_code = status.HTTP_201_CREATED)
def create_workspace(workspace : WorkspaceCreate,
                      db : Session = Depends(get_db),
                      current_user : User = Depends(get_current_user),
                      ):

    return crud_workspace.create_workspace(
        db=db, workspace=workspace, owner_id = current_user
    )


@router.get("/", response_model = List[WorksapceResponse])
def read_workspaces(db : Session = Depends(get_db),
                   current_user : User = Depends(get_current_user),
                   skip = 0,
                   limit = 100,
                   ):
    return crud_workspace.get_user_workspace(
        db = db , owner_id=current_user, skip=skip, limit=limit
    )


@router.get("/{workspace_id}", response_model = WorksapceResponse)
def read_workspace(workspace_id : int,
                   db : Session = Depends(get_db),
                   curent_user : User = Depends(get_current_user)
                   ):
    
    db_worksapce = crud_workspace.get_workspace_by_id(
        db = db ,workspace_id=workspace_id, owner_id=curent_user
    )

    if not db_worksapce:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )

    return db_worksapce 


@router.put("/{workspace_id}", response_model = WorksapceResponse)
def update_workspace(workspace_id : int,
                     workspace : WorkspaceUpdate,
                    db : Session = Depends(get_db),       
                    current_user : User = Depends(get_current_user),
                    ):
    updated_workspace = crud_workspace.update_workspace(
        db=db, workspace_id = workspace_id, workspace_data = workspace, owner_id = current_user
    )

    if not updated_workspace:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail="Workspace not found or unauthorized"
        )

    return updated_workspace


@router.delete("/{workspace_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_workspace(workspace_id : int,
                    db : Session = Depends(get_db),
                     current_user : User = Depends(get_current_user)
                     ):
    success = crud_workspace.delete_workspace(
        db = db, workspace_id = workspace_id, owner_id = current_user
    )

    if not success:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Workspace not found or unauthorized"
        )

    return None
    
