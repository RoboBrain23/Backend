from fastapi import APIRouter, status, Depends
import db.database as database, api.chair_api.db.schemas as schemas, api.chair_api.db.crud as crud
from sqlalchemy.orm import Session

# * Here are the routes that related to the data coming from the chair

router = APIRouter(tags=["chair"], prefix="/chair")


# * Create a route that will return the last chair data for a specific patient
@router.get(
    "/data/{chair_id}",
    response_model=schemas.GetChairData,
    status_code=status.HTTP_200_OK,
)
def get_chair_data(
    chair_id: int,
    db: Session = Depends(database.get_db),
):
    return crud.get_chair_data(chair_id=chair_id, db=db)


# * Create a route that will store the data in the database when POST request is sent to the route
@router.post("/data", status_code=status.HTTP_201_CREATED)
def read_new_chair_data(
    data: schemas.ReadChairData, db: Session = Depends(database.get_db)
):
    return crud.store_chair_data(data=data, db=db)


# * Register a new chair to use in the database
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def chair_registration(
    chair: schemas.ChairRegistration, db: Session = Depends(database.get_db)
):
    return crud.chair_signup(chair=chair, db=db)


# * Caregiver login to the chair to access sensor's data
@router.post("/login", status_code=status.HTTP_200_OK)
def chair_login(
    chair: schemas.ChairRegistration,
    db: Session = Depends(database.get_db),
):
    return crud.chair_login(chair=chair, db=db)