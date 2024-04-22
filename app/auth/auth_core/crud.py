from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.auth_utils.auth_utils import hashPassword
from app.auth.auth_core import schemas, models


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashedPassword = hashPassword(user.password)
    db_user = models.User(username=user.username, hashed_password=hashedPassword)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    user_in_db = schemas.UserGet(username=db_user.username)
    return user_in_db


async def get_user(db: AsyncSession, username: str):
    query = select(models.User).where(models.User.username == username)
    result = await db.execute(query)
    return result.scalars().first()
