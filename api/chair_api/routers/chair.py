from fastapi import APIRouter, status, Depends, HTTPException
import db.database as database, api.chair_api.db.schemas as schemas, api.chair_api.db.crud as crud
from sqlalchemy.orm import Session
from auth.schema import Token
from fastapi_jwt_auth import AuthJWT

# * Here are the routes that related to the data coming from the chair

router = APIRouter(tags=["chair"], prefix="/chair")


# * Register a new chair to use in the database
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def chair_registration(
    chair: schemas.ChairRegistration, db: Session = Depends(database.get_db)
):
    return crud.chair_signup(chair=chair, db=db)


# * Caregiver login to the chair to access sensor's data
@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def chair_login(
    chair: schemas.ChairRegistration,
    db: Session = Depends(database.get_db),
    authorize: AuthJWT = Depends(),
):
    return crud.chair_login(chair=chair, db=db, authorize=authorize)


# * Create a route that will store the data in the database when POST request is sent to the route
@router.post("/data", status_code=status.HTTP_201_CREATED)
def read_new_chair_data(
    data: schemas.GetChairData,
    db: Session = Depends(database.get_db),
    authorize: AuthJWT = Depends(),
):
    try:
        authorize.jwt_required()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    current_chair = authorize.get_jwt_subject()
    return crud.store_chair_data(data=data, db=db, chair_id=current_chair)


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


@router.post("/location", status_code=status.HTTP_201_CREATED)
async def recieve_location(
    location: schemas.StoreChairLocation, db: Session = Depends(database.get_db)
):
    return crud.post_chair_location(db=db, location=location)
