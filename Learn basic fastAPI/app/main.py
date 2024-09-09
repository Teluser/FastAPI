from typing import Optional
from fastapi import FastAPI, Depends, Response, status, HTTPException # type: ignore
from fastapi.params import Body # type: ignore
from sqlalchemy.orm import Session # type: ignore
import schemas
import models
from database import engine, get_db
import crud

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

@app.get("/posts/", response_model=list[schemas.Post])
def get_posts(db:Session = Depends(get_db)):
    return crud.get_posts(db)

@app.post("/post/", response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db:Session = Depends(get_db)): 
    return crud.create_post(db, new_post)

@app.get("/post/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db:Session = Depends(get_db)): 
    post = crud.get_post(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post

@app.delete("/post/{id}")
def delete_post(id: int, db:Session = Depends(get_db)):
    post = crud.get_post(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return crud.delete_post(db, id)
       
@app.put("/post/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostBase, db:Session = Depends(get_db)):
    return crud.update_post(db, id, update_post)
   
