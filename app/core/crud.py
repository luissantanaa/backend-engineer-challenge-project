from sqlalchemy.orm import Session

from . import models, schemas
from .utils.utils import hashPassword, convertBytes, convertTimestamp, isValidDataPoint


def get_user_data_points(db: Session):
    return db.query(models.DataPoint).where(models.DataPoint.valid).all()


def get_admin_data_points(db: Session):
    return db.query(models.DataPoint).all()


def create_data_point(db: Session, data_point: schemas.DataPointRecieve):
    converted_value = convertBytes(data_point.value)
    converted_time = convertTimestamp(data_point.time)
    valid = isValidDataPoint(data_point.tags, data_point.time)
    db_point = models.DataPoint(
        time=converted_time, value=converted_value, valid=valid[1], tags=valid[0]
    )
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point


def create_user(db: Session, user: schemas.UserCreate):
    hashedPassword = hashPassword(user.password)
    db_user = models.User(username=user.username, hashed_password=hashedPassword)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
