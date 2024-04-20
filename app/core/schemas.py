from pydantic import BaseModel
from datetime import datetime


class DataPointBase(BaseModel):
    time: datetime


class DataPointRecieve(DataPointBase):
    value: list[int]
    tags: list[str]


class DataPointCreate(DataPointBase):
    value: float
    valid: bool
    tags: list[str]


class DataPointUserGet(DataPointBase):
    value: float

    class Config:
        orm_mode = True


class DataPointAdminGet(DataPointBase):
    value: float
    valid: bool
    tags: list[str]

    class Config:
        orm_mode = True
