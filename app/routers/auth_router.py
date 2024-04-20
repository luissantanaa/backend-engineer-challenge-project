from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.auth.auth_core import crud, models, schemas
from ..core.database import SessionLocal, engine
from ..core.utils.utils import getDataPoint

models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Users"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
