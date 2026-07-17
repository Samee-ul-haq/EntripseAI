from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username : str= Field(min_length=3, max_length= 100)
    email : EmailStr


class UserCreate(UserBase):
    password : str = Field(min_length= 8,  max_length= 64)



class UserLogin(BaseModel):
    email : EmailStr
    password : str



# class UserUpdate(UserBase):
#     email : EmailStr
#     password : str


class UserResponse(UserBase):
    id : int