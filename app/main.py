from fastapi import FastAPI
from .routers import data_points_router, auth_router

description = """
Data Points API

## Data Points

Regular users can use to API to get a certain range of valid data points stored in the database.
Admins can populate the database and get all of the data points in the database

## Users

The user section allows the creation and authorization of users.
"""


app = FastAPI(
    description=description,
)

app.include_router(data_points_router.router)
app.include_router(auth_router.router)
