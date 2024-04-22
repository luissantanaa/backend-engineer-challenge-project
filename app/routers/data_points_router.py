from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from ..core import crud, models, schemas
from ..core.database import engine
from ..core.utils.utils import getDataPoint
from app.auth.auth_core.schemas import UserAuth
from app.deps.dependencies import get_db, get_current_user

models.Base.metadata.create_all(bind=engine)

router = APIRouter(tags=["Data Points"])


@router.get("/data/", response_model=list[schemas.DataPointGet])
def read_data(
    start: datetime = datetime.min,
    end: datetime = datetime.max,
    skip: int = 0,
    limit: int = 100,
    user: UserAuth = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user.role == "admin":
        data = crud.get_admin_data_points(db, start, end)
    else:
        data = crud.get_user_data_points(db, start, end)
    return data


@router.get("/populate/", response_model=schemas.DataPointGet)
def get_data(
    db: Session = Depends(get_db),
    user: UserAuth = Depends(get_current_user),
):

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect username or password",
        )

    reqResponse = getDataPoint()
    if reqResponse.status_code == 200:
        data_point = schemas.DataPointRecieve.model_validate(reqResponse.json())
        data = crud.create_data_point(db, data_point)
        added_data = schemas.DataPointGet(
            time=data.time, value=data.value, valid=data.valid, tags=data.tags
        )
        return added_data
    else:
        raise HTTPException(reqResponse.status_code, detail="No data point available")
