from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import db.schemas as schemas, db.database as database, db.crud as crud, db.models as models
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from auth.schema import Token


router = APIRouter(tags=["patient"], prefix="/patient")

"""
# * Create a route that will register a new patient in the database when POST request is sent to the route
@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    patient: schemas.SignUp,
    authorize: AuthJWT = Depends(),
    db: Session = Depends(database.get_db),
):
    return crud.signup(patient=patient, db=db, authorize=authorize)


# TODO: Create 2 Routes

# ? Create a route that will login the patient
# * POST  ==>  "/login"


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    patient: schemas.Login,
    authorize: AuthJWT = Depends(),
    db: Session = Depends(database.get_db),
):
    return crud.login(db=db, authorize=authorize, patient=patient)


# ? Create a route that will return the patient data when authontication is successful
# * GET  ==>  "/me"


@router.get("/me",response_model=schemas.Info, status_code=200)
async def get_info(
    authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)
):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    current_user = authorize.get_jwt_subject()
    return crud.user_info(user_id=current_user, db=db)
"""


@router.post("/info", status_code=status.HTTP_201_CREATED)
async def register_patient(
    patient: schemas.PatientData,
    authorize: AuthJWT = Depends(),
    db: Session = Depends(database.get_db),
):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    chair_id = authorize.get_jwt_subject()
    return crud.add_new_patient(db=db, patient=patient, chair_id=chair_id)


# TODO: Complete the following route for returning patient information
@router.get(
    "/info/{chair_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PatientData,
)
async def get_patient_data(chair_id: int, db: Session = Depends(database.get_db)):
    return crud.patient_info(chair_id=chair_id, db=db)


# TODO: Complete the following route for updating patient information
@router.put("/chair-update", status_code=status.HTTP_200_OK)
async def update_chair():
    pass
