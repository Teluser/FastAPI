import schemas, crud
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Response, status, HTTPException, APIRouter # type: ignore
import oauth2

router = APIRouter(
    prefix="/posts", # prefix of the url
    tags=["Posts"] # show API docs group with this tag
)
@router.get("/", response_model=list[schemas.Post])
def get_posts(db:Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    return crud.get_posts(db)

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db:Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)): 
    return crud.create_post(db, new_post)

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response, db:Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)): 
    post = crud.get_post(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    return post

@router.delete("/{id}")
def delete_post(id: int, db:Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    post = crud.get_post(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    deleted_post_id = crud.delete_post(db, id)
    return {"message": f"Successfully deleted, deleted_post_id = {deleted_post_id}"}
       
@router.put("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostBase, db:Session = Depends(get_db), user_id: str = Depends(oauth2.get_current_user)):
    return crud.update_post(db, id, update_post)