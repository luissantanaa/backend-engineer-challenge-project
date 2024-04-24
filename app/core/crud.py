from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core import models, schemas
from app.core.utils.utils import convert_bytes, convert_timestamp, is_valid_data_point


async def get_user_data_points(
    db: AsyncSession, start: datetime, end: datetime, skip: int, limit: int
):
    logging.info(
        "GET_USER_DATA_POINTS with start:%s, end:%s, skip:%s, limit:%s",
        start,
        end,
        skip,
        limit,
    )
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
    logging.info(
        "GET_ADMIN_DATA_POINTS with start:%s, end:%s, skip:%s, limit:%s",
        start,
        end,
        skip,
        limit,
    )
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
    logging.info(
        "CREATE_DATA_POINT with time:%s, value:%s, tags:%s",
        data_point.time,
        data_point.value,
        data_point.tags,
    )

    converted_value = convert_bytes(data_point.value)
    converted_time = convert_timestamp(data_point.time)
    tags, valid = is_valid_data_point(data_point.tags, data_point.time)
    db_point = models.DataPoint(
        time=converted_time, value=converted_value, valid=valid, tags=tags
    )
    db.add(db_point)
    await db.commit()
    await db.refresh(db_point)
    return db_point
