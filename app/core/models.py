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


class DataPoint(Base):
    __tablename__ = "data_points"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(type_=TIMESTAMP(timezone=True))
    value = Column(DOUBLE_PRECISION)
    valid = Column(Boolean)
    tags = Column(ARRAY(String))
