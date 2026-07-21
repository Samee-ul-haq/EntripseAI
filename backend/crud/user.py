import bcrypt
import jwt
import os
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session


from backend.models import User
from backend.schemas.user import (UserCreate, UserLogin, UserResponse, UserResponseMe, UserUpdate)



ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
SECRET_KEY  = os.getenv("SECRET_KEY")
ALGORITHM  = os.getenv("ALGORITHM")


def create_user(user : UserCreate, db: Session)-> User:
    user_db = db.query(User).filter_by(email = user.email).first()

    if user_db :
        raise HTTPException( status_code = 409 , detail = "A user with this email already exists")

    db_user = User(
        username = user.username, 
        email = user.email,
        )
    db_user.password = user.password

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



def get_user(user_id : int, db : Session) -> UserResponse:
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code = 404, detail="User not found")
    
    return user



def login(user : UserLogin, db : Session):
    user_db = db.query(User).filter(User.email == user.email).first()

    if user_db is None:
        return None

    if bcrypt.checkpw(
        user.password.encode("utf-8"),
        user_db.password.encode("utf-8"),
        ):

        expire = datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {
            "sub" : str(user_db.id),
            "exp" : expire
        }

        encoded_jwt = jwt.encode(token_data, SECRET_KEY,algorithm= ALGORITHM)

        return {
            "access_token" : encoded_jwt,
            "token_type" : "bearer"
        }
    
    else :
        return None
    



def send_me(user_id : int , db :  Session) -> UserResponseMe:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail= "User not found")

    return user



def populate(user_id : int , db : Session , user : UserUpdate):
    user_db = db.query(User).filter(User.id == user_id).first()

    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    model_dump = user.model_dump(exclude_unset = True)
    for key, value in model_dump.items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)
    return user_db



def delete(user_id : int ,db : Session):
    user_db = db.query(User).filter(User.id == user_id).first()

    if user_db is None:
        raise HTTPException(status_code = 404, detail="User not found")
    
    db.delete(user_db)
    db.commit()

    return f"{user_db.username} deleted successfully"
