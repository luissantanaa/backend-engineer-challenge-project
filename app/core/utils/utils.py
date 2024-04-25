import struct
import os
from typing import Tuple
from datetime import datetime
import requests
from requests import Response


def convert_bytes(values: list[int]) -> float:
    value_bytes = bytes(values)
    return struct.unpack("<f", value_bytes)[0]


def convert_timestamp(time: datetime) -> datetime:
    iso_str = time.isoformat()
    return datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S%z")


def is_valid_data_point(tags: list[str], time: datetime) -> Tuple[list[str], bool]:
    valid = True

    current_datetime = datetime.now()
    unix_timestamp = current_datetime.timestamp()
    if (unix_timestamp - time.timestamp()) / 3600 > 1:
        tags.append("too old")

    if "system" in tags or "suspect" in tags or "too old" in tags:
        valid = False

    return [tags, valid]


def get_data_point() -> Response:
    server_url = os.getenv("SERVER_URL")
    server_port = os.getenv("SERVER_PORT")
    response = Response()

    try:
        response = requests.get("http://" + server_url + ":" + server_port, timeout=30)
    except:
        response.status_code = 502

    return response
