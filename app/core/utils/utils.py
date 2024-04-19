import struct
import os
from typing import Tuple
import bcrypt
from datetime import datetime, timedelta
import requests
from requests import Response


def hashPassword(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    return str(hashed_password)


def convertBytes(values: list[int]) -> float:
    value_bytes = bytes(values)
    return struct.unpack("<f", value_bytes)[0]


def convertTimestamp(time: datetime) -> datetime:
    return time.isoformat()


def isValidDataPoint(tags: list[str], time: datetime) -> Tuple[list[str], bool]:
    valid = True
    if "system" in tags or "suspect" in tags:
        valid = False
    else:
        # unix_timestamp = datetime.fromtimestamp(
        #     datetime.now() - datetime(1970, 1, 1)
        # ).total_seconds()

        current_datetime = datetime.now()
        unix_timestamp = current_datetime.timestamp()
        if (unix_timestamp - time.timestamp()) / 3600 > 1:
            valid = False
            tags.append("too old")

    return [tags, valid]


def getDataPoint() -> Response:
    server_url = os.getenv("SERVER_URL")
    server_port = os.getenv("SERVER_PORT")
    req = requests.get("http://" + server_url + ":" + server_port)

    return req
