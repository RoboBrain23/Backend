from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import db.schemas as schemas, db.database as database, db.crud as crud, db.models as models
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from auth.schema import Token


router = APIRouter(tags=["patient"], prefix="/patient")


@router.post(
    "/info", response_model=schemas.PatientData, status_code=status.HTTP_201_CREATED
)
def register_patient(
    patient: schemas.PatientDataRegister,
    db: Session = Depends(database.get_db),
):
    return crud.add_new_patient(db=db, patient=patient)


@router.get(
    "/info/{chair_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PatientData,
)
def get_patient_data(chair_id: int, db: Session = Depends(database.get_db)):
    return crud.patient_info(chair_id=chair_id, db=db)


# TODO: Add a logic for checking if the new chair is currently used or not before use it
@router.put("/chair-update/{chair_id}", status_code=status.HTTP_200_OK)
def update_chair(
    chair_id: int,
    new_chair: schemas.ChairRegistration,
    db: Session = Depends(database.get_db),
):
    return crud.update_patient_chair(
        current_chair_id=chair_id, new_chair=new_chair, db=db
    )
