from pydantic import BaseModel, EmailStr, Field, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    created_at : datetime


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes = True)
    id : int


class UserUpdate(BaseModel):
    username : str | None = Field(default = None , min_length=3, max_length=100)
    email  : EmailStr | None = None