from sqlalchemy.orm import Session # type: ignore
from fastapi import status, HTTPException # type: ignore
import models, schemas, utils

def get_posts(db:Session, skip:int=0, limit:int=100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_post(db:Session, id:int):
    return db.query(models.Post).filter(models.Post.id == id).first()


def create_post(db:Session, post:schemas.PostCreate):
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def delete_post(db:Session, id:int):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    delete_post_id = post.id
    db.delete(post)
    db.commit()
    return delete_post_id

def update_post(db:Session, id:int, post: schemas.PostBase):
    update_post = get_post(db, id)
    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    for key, value in post.dict().items():
        setattr(update_post, key, value)
    db.commit()
    db.refresh(update_post)
    return update_post

def get_users(db:Session):
    return db.query(models.User).all()

def get_user_by_email(db:Session, email:int):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db:Session, id:int):
    return db.query(models.User).filter(models.User.id == id).first()

def create_user(db:Session, create_user:schemas.UserCreate):
    create_user.password = utils.get_password_hash(create_user.password)
    new_user = models.User(**create_user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db:Session, email:str, password:str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not utils.verify_password(password, user.password):
        return False
    return user
