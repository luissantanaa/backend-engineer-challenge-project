from datetime import datetime
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import crud, schemas
from app.core.utils.utils import get_data_point
from app.auth.auth_core.schemas import UserAuth
from app.deps.dependencies import get_db, get_current_user

router = APIRouter(prefix="/api", tags=["Data Points"])


@router.get(
    "/data",
    response_model=list[schemas.DataPointGet],
    description="Gets data points stored in database within the given range",
)
async def read_data(
    start: datetime = datetime.min,
    end: datetime = datetime.max,
    skip: int = 0,
    limit: int = 100,
    user: UserAuth = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if user.role == "admin":
        data = await crud.get_admin_data_points(db, start, end, skip, limit)
    else:
        data = await crud.get_user_data_points(db, start, end, skip, limit)
    return data


@router.get(
    "/populate",
    response_model=schemas.DataPointGet,
    description="Allows admins to populate the database with calls to external server",
)
async def get_data(
    db: AsyncSession = Depends(get_db),
    user: AsyncSession = Depends(get_current_user),
):

    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized",
        )

    req_response = get_data_point()
    if req_response.status_code == 200:
        data_point = schemas.DataPointRecieve.model_validate(req_response.json())
        data = await crud.create_data_point(db, data_point)
        added_data = schemas.DataPointGet(
            time=data.time, value=data.value, valid=data.valid, tags=data.tags
        )
        return added_data
    else:
        raise HTTPException(req_response.status_code, detail="No data point available")
