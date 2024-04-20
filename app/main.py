from fastapi import FastAPI
from .routers import data_points_router, auth_router


app = FastAPI()

app.include_router(data_points_router.router)
app.include_router(auth_router.router)
