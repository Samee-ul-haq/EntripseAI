from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.schemas.user import (UserCreate, UserLogin, UserResponse)
from backend.database import SessionLocal
from backend.database import get_db

from backend.models import User

router = APIRouter(prefix="/users",tags=["Users"])


@router.post("/register/")
async def create_user(user : UserCreate, db : Session= Depends(get_db)):
    db.query(User).create(user)
    return {"message":f"{user.username} created successfully"}


@router.get("/{user_id}/", response_model= UserResponse)
async def get_user(user_id : int, db : Session= Depends(get_db)) -> UserResponse :
    user = db.query(User).filter(User.id == user_id).first()
    return user


@router.post("/login/")
async def login(user : UserLogin, db : Session= Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db is None:
        return f"user with email {user.email} doesnt exist"

    if user.password == user_db.password:
        return {"login successfull"}
    
    else :
        return {"incorrect email or password"}