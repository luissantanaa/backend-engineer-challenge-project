from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas
from .utils.utils import convertBytes, convertTimestamp, isValidDataPoint


def get_user_data_points(
    db: Session, start: datetime, end: datetime, skip: int, limit: int
):
    return (
        db.query(models.DataPoint)
        .where(models.DataPoint.valid)
        .where(models.DataPoint.time >= start)
        .where(models.DataPoint.time <= end)
        .limit(limit)
        .offset(skip)
        .all()
    )


def get_admin_data_points(
    db: Session, start: datetime, end: datetime, skip: int, limit: int
):
    return (
        db.query(models.DataPoint)
        .where(models.DataPoint.time >= start)
        .where(models.DataPoint.time <= end)
        .limit(limit)
        .offset(skip)
        .all()
    )


def create_data_point(db: Session, data_point: schemas.DataPointRecieve):
    converted_value = convertBytes(data_point.value)
    converted_time = convertTimestamp(data_point.time)
    tags, valid = isValidDataPoint(data_point.tags, data_point.time)
    db_point = models.DataPoint(
        time=converted_time, value=converted_value, valid=valid, tags=tags
    )
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point
