from fastapi import APIRouter

from backend.schemas.user import (UserCreate, UserLogin, UserResponse)

router = APIRouter()

@router.post("/register/")
async def create_user(user : UserCreate):
    return {"message":f"{user.username} created successfully"}

@router.get("/user/{user_id}/", response_model= UserResponse)
async def get_user(user_id : int):
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    return {user}


@router.post("/login/")
async def login(user : UserLogin):
    return {"login successfulll"}