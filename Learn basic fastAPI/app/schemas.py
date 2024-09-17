from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr # type: ignore

class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool = True
    rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True




class UserBase(BaseModel):
    email: EmailStr 

class UserCreate(UserBase):
    password: str

class UserLogin(UserCreate):
    pass

class User(UserBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str