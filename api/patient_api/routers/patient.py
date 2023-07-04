from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import db.database as database, api.patient_api.db.crud as crud
from api.patient_api.db.schemas import PatientData, PatientDataRegister
from api.chair_api.db.schemas import ChairRegistration
from fastapi_jwt_auth import AuthJWT

router = APIRouter(tags=["patient"], prefix="/patient")


@router.post("/info", status_code=status.HTTP_201_CREATED)
def register_patient(
    patient: PatientDataRegister,
    db: Session = Depends(database.get_db),
    authorize: AuthJWT = Depends(),
):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    caregiver_id = authorize.get_jwt_subject()
    return crud.add_new_patient(db=db, patient=patient, caregiver_id=caregiver_id)


@router.post("/track", status_code=status.HTTP_200_OK)
async def track_patient(
    chair: ChairRegistration,
    db: Session = Depends(database.get_db),
    authorize: AuthJWT = Depends(),
):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    caregiver_id = authorize.get_jwt_subject()
    return crud.connect_patient(db=db, chair=chair, caregiver_id=caregiver_id)


@router.get(
    "/info/{chair_id}",
    status_code=status.HTTP_200_OK,
    response_model=PatientData,
)
def get_patient_data(chair_id: int, db: Session = Depends(database.get_db)):
    return crud.patient_info(chair_id=chair_id, db=db)


# TODO: Add a logic for checking if the new chair is currently used or not before use it
@router.put("/chair-update/{chair_id}", status_code=status.HTTP_200_OK)
def update_chair(
    chair_id: int,
    new_chair: ChairRegistration,
    db: Session = Depends(database.get_db),
):
    return crud.update_patient_chair(
        current_chair_id=chair_id, new_chair=new_chair, db=db
    )
