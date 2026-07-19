from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    username : str= Field(min_length=3, max_length= 100)
    email : EmailStr


class UserCreate(UserBase):
    password : str = Field(min_length= 8,  max_length= 64)



class UserLogin(BaseModel):
    email : EmailStr
    password : str


class UserResponseMe(UserBase):
    created_at : datetime


class UserResponse(UserBase):
    id : int


class UserUpdate(BaseModel):
    username : str | None = None
    email  : EmailStr | None = None