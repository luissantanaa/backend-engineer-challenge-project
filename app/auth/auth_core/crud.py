from sqlalchemy.orm import Session
from . import models, schemas
from app.auth.auth_utils.auth_utils import hashPassword


def create_user(db: Session, user: schemas.UserCreate):
    hashedPassword = hashPassword(user.password)
    db_user = models.User(username=user.username, hashed_password=hashedPassword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
