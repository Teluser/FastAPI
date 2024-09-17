from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from sqlalchemy.orm import Session
import crud, schemas, utils
from constants import DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    tags=["Authentication"]
)

#login with user_name, password
@router.post("/login", status_code=status.HTTP_200_OK)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user.email, user.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = utils.create_access_token(data={"user": user.email})
    return {"token": "Successfully logged in"}

@router.post("/token")
async def get_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> schemas.Token:
    # call request with form_data oauth2 (user_name,password) => return schemas.Token
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"user": user.id}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

# get current user by token
@router.post("/users/me/", status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_current_user(token: schemas.Token, db: Session = Depends(get_db)) :
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = utils.decode_access_token(token.access_token)
    user_id = payload.get("user")
    user = crud.get_user_by_id(db, id=user_id)
    if user is None:
        raise credentials_exception
    return user
