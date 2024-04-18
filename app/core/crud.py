from sqlalchemy.orm import Session

from . import models, schemas
from utils.utils import hashPassword


def get_user_data_points(db: Session):
    return db.query(models.DataPoint).where(models.DataPoint.valid).all()


def get_admin_data_points(db: Session):
    return db.query(models.DataPoint).where(models.DataPoint.valid).all()


def create_data_point(db: Session, data_point: schemas.DataPointCreate):
    hashedPassword = hashPassword(user.password)
    db_user = models.User(username=user.username, hashed_password=hashedPassword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user(db: Session, user: schemas.UserCreate):
    hashedPassword = hashPassword(user.password)
    db_user = models.User(username=user.username, hashed_password=hashedPassword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
