from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import db.schemas as schemas, db.database as database, db.crud as crud, db.models as models
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from auth.schema import Token


router = APIRouter(tags=["patient"], prefix="/patient")


@router.post("/info", status_code=status.HTTP_201_CREATED)
def register_patient(
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
def get_patient_data(chair_id: int, db: Session = Depends(database.get_db)):
    return crud.patient_info(chair_id=chair_id, db=db)


# TODO: Complete the following route for updating patient information
@router.put("/chair-update", status_code=status.HTTP_200_OK)
def update_chair():
    pass
