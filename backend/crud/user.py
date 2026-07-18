import bcrypt
from fastapi import HTTPException


from backend.models import User
from backend.schemas.user import (UserCreate, UserLogin, UserResponse)
from sqlalchemy.orm import Session


def create_user(user : UserCreate, db: Session)-> User:
    db_user = User(
        username = user.username, 
        email = user.email,
        )
    db_user.password = user.password

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message":f"{db_user} created successfully"}



def get_user(user_id : int, db : Session) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code = 404, detail="User not found")
    
    return user



def login(user : UserLogin, db : Session):
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db is None:
        return f"user with email {user.email} doesnt exist"

    if bcrypt.checkpw(
        user.password.encode("utf-8"),
        user_db.password.encode("utf-8"),
        ):
        return "login successfull"
    
    else :
        return {"incorrect email or password"}