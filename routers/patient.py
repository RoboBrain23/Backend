from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import db.schemas as schemas, db.database as database, db.crud as crud, db.models as models
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


router = APIRouter(tags=["patient"], prefix="/patient")


# * Create a route that will register a new patient in the database when POST request is sent to the route
@router.post(
    "/signup", response_model=schemas.SignUp, status_code=status.HTTP_201_CREATED
)
async def signup(patient: schemas.SignUp, authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)):
    return crud.signup(patient=patient, db=db, authorize=authorize)


# TODO: Create 2 Routes

# ? Create a route that will login the patient
# * POST  ==>  "/login"


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(patient: schemas.Login, authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.Patient).filter(patient.email == models.Patient.email).first()
    if user and crud.verify_password(patient.password, user.password):
        access_token = authorize.create_access_token(subject=user.id)
        refresh_token = authorize.create_refresh_token(subject=user.id)

        response = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "message": "Success",
        }
        return jsonable_encoder(response)
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid email or password"
    )


# ? Create a route that will return the patient data when authontication is successful
# * GET  ==>  "/me"
