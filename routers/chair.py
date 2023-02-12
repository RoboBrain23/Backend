from fastapi import APIRouter, HTTPException, status, Depends
import db.database as database, db.schemas as schemas, db.crud as crud, db.models as models
from sqlalchemy.orm import Session

# * Here are the routes that related to the data coming from the chair

router = APIRouter(
    tags=["chair"],
    prefix="/chair",
)


# * Create a route that will return the last chair data for a specific patient
@router.get(
    "/data/{patient_id}",
    response_model=schemas.GetChairData,
    status_code=status.HTTP_200_OK,
)
async def get_chair_data(patient_id: int, db: Session = Depends(database.get_db)):
    return crud.get_chair_data(patient_id=patient_id, db=db)


# * Create a route that will store the data in the database when POST request is sent to the route
@router.post(
    "/data", response_model=schemas.ReadChairData, status_code=status.HTTP_202_ACCEPTED
)
async def read_new_chair_data(
    data: schemas.ReadChairData, db: Session = Depends(database.get_db)
):
    return crud.store_chair_data(data=data, db=db)
