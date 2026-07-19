from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from sqlalchemy.orm import Session
from typing import Annotated
import jwt
import os


from backend.database import get_db
from backend.schemas.user import UserResponse, UserCreate, UserLogin, UserResponseMe, UserUpdate
from backend.models import User
from backend import crud


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


router = APIRouter(prefix="/users",tags=["Users"])


def get_current_user(
        access_token : Annotated[str | None, Cookie()] = None
) -> int:
    
    credientials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Not authenticated or session expired"
    )

    if not access_token :
        raise credientials_exception
    
    try:
        token_type , token  = access_token.split(" ", 1)
        if token_type.lower() != "bearer":
            raise credientials_exception
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id : int  = payload.get("sub")

        if user_id is None:
            raise credientials_exception
        
        return int(user_id)

    except (jwt.PyJWTError, ValueError):
        raise credientials_exception
    

@router.post("/register")
async def register_user(user : UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(user, db)




@router.post("/login/")
async def login_user(user : UserLogin,
                        response: Response,
                        db : Session = Depends(get_db)):
    auth_data = crud.login(user, db)

    if  auth_data is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers = {"WWW.Authenticate": "Bearer"}
        )
    
    token = auth_data["access_token"]
    response.set_cookie(
        key = "access_token",
        value = f"Bearer {token}",
        httponly = True,
        max_age = 3600,
        expires = 3600,
        samesite = "lax",
        secure = False
    )

    return {"message":"Login successfull"}





@router.get("/me")
async def send_user(user_id : Annotated[int, Depends(get_current_user)] ,db : Session = Depends(get_db)) -> UserResponseMe:
    if user_id is None:
        return  "You are not valid for this access"
    return crud.send_me(user_id, db)




@router.put("/me")
async def put_content(user_id: Annotated[int, Depends(get_current_user)], 
                      user : UserUpdate,
                       db : Session = Depends(get_db),
                       ):
    return crud.populate(user_id, db ,user)



@router.delete("/me")
async def delete_user(user_id : Annotated[int, Depends(get_current_user)],
                       db : Session = Depends(get_db),
                       ):
    return crud.delete(user_id, db)




@router.post("/logout")
async def logout_user(response : Response):
    response.delete_cookie("access_token")
    return {"message": "Logout user successfully"}




@router.get("/{user_id}/")
async def user_response(user_id : int, db: Session = Depends(get_db)) -> UserResponse:

    return crud.get_user(user_id, db)

