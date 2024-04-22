from pydantic import BaseModel, ConfigDict
from datetime import datetime


class DataPointBase(BaseModel):
    time: datetime


class DataPointRecieve(DataPointBase):
    value: list[int]
    tags: list[str]


class DataPointGet(DataPointBase):
    model_config = ConfigDict(from_attributes=True)
    value: float
    valid: bool
    tags: list[str]
