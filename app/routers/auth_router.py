from fastapi import APIRouter, status
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.auth_core import crud, schemas
from app.auth.auth_utils.auth_utils import (
    verifyPassword,
    create_access_token,
    create_refresh_token,
)

from app.deps.dependencies import get_db


router = APIRouter(prefix="/auth", tags=["Users"])


@router.post(
    "/signup",
    summary="Create new user",
    description="Allows for the creation of a new user",
)
async def signup(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user_in_db = await crud.get_user(db, user.username)
    if user_in_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    user = await crud.create_user(db, user)
    return user


@router.post(
    "/login",
    response_model=schemas.TokenSchema,
    description="Logs in user",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user_in_db = await crud.get_user(db, form_data.username)
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
