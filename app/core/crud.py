from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models, schemas
from .utils.utils import convertBytes, convertTimestamp, isValidDataPoint


async def get_user_data_points(
    db: AsyncSession, start: datetime, end: datetime, skip: int, limit: int
):
    query = (
        select(models.DataPoint)
        .where(models.DataPoint.valid)
        .where(models.DataPoint.time >= start)
        .where(models.DataPoint.time <= end)
        .limit(limit)
        .offset(skip)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_admin_data_points(
    db: AsyncSession, start: datetime, end: datetime, skip: int, limit: int
):
    query = (
        select(models.DataPoint)
        .where(models.DataPoint.time >= start)
        .where(models.DataPoint.time <= end)
        .limit(limit)
        .offset(skip)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def create_data_point(db: AsyncSession, data_point: schemas.DataPointRecieve):
    converted_value = convertBytes(data_point.value)
    converted_time = convertTimestamp(data_point.time)
    tags, valid = isValidDataPoint(data_point.tags, data_point.time)
    db_point = models.DataPoint(
        time=converted_time, value=converted_value, valid=valid, tags=tags
    )
    db.add(db_point)
    await db.commit()
    await db.refresh(db_point)
    return db_point
