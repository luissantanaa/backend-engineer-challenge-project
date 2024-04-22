from fastapi import APIRouter, status
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth.auth_core import crud, models, schemas
from app.auth.auth_utils.auth_utils import (
    verifyPassword,
    create_access_token,
    create_refresh_token,
)
from ..core.database import engine
from app.deps.dependencies import get_db

models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Users"])


@router.post("/signup", summary="Create new user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_in_db = crud.get_user(db, user.username)
    if user_in_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    user = crud.create_user(db, user)
    return user


@router.post("/login/", response_model=schemas.TokenSchema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user_in_db = crud.get_user(db, form_data.username)
    if user_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    correct_login = verifyPassword(form_data.password, user_in_db.hashed_password)
    if not correct_login:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    return {
        "access_token": create_access_token(form_data.username),
        "refresh_token": create_refresh_token(form_data.username),
    }
