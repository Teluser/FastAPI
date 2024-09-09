from sqlalchemy.orm import Session # type: ignore
from fastapi import status, HTTPException # type: ignore


import models, schemas

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
    db.delete(post)
    db.commit()
    db.refresh(post)
    return True

def update_post(db:Session, id:int, post: schemas.PostBase):
    update_post = get_post(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    for key, value in post.dict().items():
        setattr(update_post, key, value)
    db.commit()
    db.refresh(post)
    return post

