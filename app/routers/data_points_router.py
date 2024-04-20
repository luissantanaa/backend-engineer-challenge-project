from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..core import crud, models, schemas
from ..core.database import SessionLocal, engine
from ..core.utils.utils import getDataPoint

models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Data Points"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/data/", response_model=list[schemas.DataPointUserGet])
def read_data(
    start: datetime = datetime.min,
    end: datetime = datetime.max,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    data = crud.get_user_data_points(db, start, end)
    return data


@router.get("/populate/", response_model=schemas.DataPointUserGet)
def get_data(db: Session = Depends(get_db)):
    reqResponse = getDataPoint()
    if reqResponse.status_code == 200:
        data_point = schemas.DataPointRecieve.model_validate(reqResponse.json())
        data = crud.create_data_point(db, data_point)
        added_data = schemas.DataPointUserGet(time=data.time, value=data.value)
        return added_data
    else:
        raise HTTPException(
            status_code=reqResponse[0], detail="No data point available"
        )
