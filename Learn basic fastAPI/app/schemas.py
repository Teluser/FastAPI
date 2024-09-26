from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr # type: ignore
from pydantic.types import conint

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
    owner_id: int # because create post need authentication, owner_id get from token, so not need to be in PostBase

    class Config:
        orm_mode = True

class PostVote(BaseModel):
    Post: Post # post need to be uppercase first letter, if not it will raise error
    votes: int
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


class VoteBase(BaseModel):
    post_id: int
    dir: conint(le=1)

class VoteCreate(VoteBase):
    pass