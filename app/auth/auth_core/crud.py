from sqlalchemy.orm import Session


from app.auth.auth_utils.auth_utils import hashPassword
from app.auth.auth_core import schemas, models


def create_user(db: Session, user: schemas.UserCreate):
    hashedPassword = hashPassword(user.password)
    db_user = models.User(username=user.username, hashed_password=hashedPassword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_in_db = schemas.UserGet(username=db_user.username)
    return user_in_db


def get_user(db: Session, username: str):
    return db.query(models.User).where(models.User.username == username).first()
