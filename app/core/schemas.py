from pydantic import BaseModel, float
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class DataPointBase(BaseModel):
    time: datetime


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
