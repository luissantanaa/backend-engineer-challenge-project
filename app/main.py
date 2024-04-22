from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import sessionmanager
from .routers import data_points_router, auth_router

description = """
Data Points API

## Data Points

Regular users can use to API to get a certain range of valid data points stored in the database.
Admins can populate the database and get all of the data points in the database

## Users

The user section allows the creation and authorization of users.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(description=description, lifespan=lifespan)

app.include_router(data_points_router.router)
app.include_router(auth_router.router)
