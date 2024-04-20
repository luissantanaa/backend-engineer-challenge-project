from fastapi import APIRouter, status
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.auth.auth_core import crud, models, schemas
from ..core.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Users"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/signup", summary="Create new user")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_in_db = (
        db.query(models.User).where(models.User.username == user.username).first()
    )
    if user_in_db is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this username already exists",
        )
    user = crud.create_user(db, user)
    return user
