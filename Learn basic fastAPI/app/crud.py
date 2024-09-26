from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import func
from fastapi import status, HTTPException # type: ignore
import models, schemas, utils

def get_posts(db:Session, skip:int=0, limit:int=100):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).offset(skip).limit(limit).all()
    return posts

def get_post(db:Session, id:int):
    return db.query(models.Post).filter(models.Post.id == id).first()


def create_post(db:Session, post:schemas.PostCreate, user_id:int):
    post = models.Post(**post.dict(), owner_id=user_id)
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

def update_post(db:Session, id:int, post: schemas.PostBase, user_id:int):
    update_post = get_post(db, id)
    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if update_post.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to update post with id {id}")
    
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
