import schemas, crud
from database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, APIRouter # type: ignore

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=list[schemas.User])
def get_users(db:Session = Depends(get_db)):
    return crud.get_users(db)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def creare_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return crud.create_user(db, user)