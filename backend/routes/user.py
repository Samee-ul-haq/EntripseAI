from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.user import UserResponse, UserCreate, UserLogin
from backend.models import User
from backend import crud

router = APIRouter(prefix="/users",tags=["Users"])


@router.post("/register")
async def register_user(user : UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(user, db)
    

@router.get("/{user_id}/")
async def user_response(user_id : int, db: Session = Depends(get_db)) -> UserResponse:
    return crud.get_user(user_id, db)


@router.post("/login/")
async def login_user(user : UserLogin, db : Session = Depends(get_db)):
    return crud.login(user, db)