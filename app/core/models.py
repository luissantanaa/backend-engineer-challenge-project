from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    TIMESTAMP,
    DOUBLE_PRECISION,
    ARRAY,
)
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    created_at = Column(TIMESTAMP, server_default=func.now())


class DataPoint(Base):
    __tablename__ = "data_points"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(TIMESTAMP)
    value = Column(DOUBLE_PRECISION)
    valid = Column(Boolean)
    tags = Column(ARRAY(String))
    created_at = Column(TIMESTAMP, server_default=func.now())
