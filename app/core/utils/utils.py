import struct
from typing import Tuple
import bcrypt
from datetime import datetime, timedelta


def hashPassword(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return str(hashed_password)


def convertBytes(values: list[int]) -> float:
    value_bytes = bytearray(values)
    return struct.unpack("<d", value_bytes)


def convertTimestamp(time: datetime) -> datetime:
    return datetime.fromtimestamp(time).isoformat()


def isValidDataPoint(tags: list[str], time: datetime) -> Tuple[list[str], bool]:
    valid = True
    if "system" in tags or "suspect" in tags:
        valid = False
    else:
        unix_timestamp = (datetime.now() - datetime(1970, 1, 1)).total_seconds()
        if (timedelta.total_seconds(unix_timestamp - time)) / 3600 > 1:
            valid = False
            tags.append("too old")

    return [tags, valid]
