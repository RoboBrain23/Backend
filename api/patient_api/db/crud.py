from sqlalchemy.orm import Session
import db.models as models
from api.chair_api.db.schemas import ChairRegistration
from api.patient_api.db.schemas import PatientDataRegister
import api.chair_api.db.crud as chair_crud
from fastapi import HTTPException, status


def add_new_patient(db: Session, patient: PatientDataRegister):
    """
    We use this function to store the patient's data in the database
    with the chair_id they use

    Args:
        db (Session): The database session that we will use to validate the data
        patient (PatientDataRegistration): The patient's data that we want to store in the database

    Returns:
        Dict: we return a Dict message tell us we stored patient's data successfully
    """

    chair_info = {"chair_id": patient.chair_id, "password": patient.password}

    login_chair_schema = ChairRegistration(**chair_info)

    db_chair = chair_crud.chair_login(db=db, chair=login_chair_schema)

    new_patient = models.Patient(
        first_name=patient.first_name,
        last_name=patient.last_name,
        gender=patient.gender,
        age=int(patient.age),
        chair_id=patient.chair_id,
    )

    chair = db.query(models.Chair).filter(models.Chair.id == patient.chair_id).first()

    new_patient.chair = chair

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


def patient_info(chair_id: int, db: Session):
    """
    We use this function to return patient's informations by recieving chair id

    Args:
        chair_id (int): The id of the chair that patient uses
        db (Session): The database session that we will use to validate the data

    Raises:
        HTTPException: if there is no patient use the chair with id chair_id, we raise exception with status code 404

    Returns:
        Dict: we return a Dict with information of the patient that connect to the chair
    """
    db_patient = (
        db.query(models.Patient).filter(chair_id == models.Patient.chair_id).first()
    )

    if db_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Patient currently use this chair",
        )

    return db_patient


def update_patient_chair(
    current_chair_id: int, new_chair: ChairRegistration, db: Session
):
    """
    We use this function to update the current chair the patient use

    Args:
        current_chair_id (int): The chair that the user currently use
        new_chair (ChairRegistration): The new chair id and password to connect it to the patient
        db (Session): The database session that we will use to validate the data

    Returns:
        Dict: Return an Dict with patient information after updating the chair
    """
    db_patient = (
        db.query(models.Patient)
        .filter(models.Patient.chair_id == current_chair_id)
        .first()
    )

    login_to_new_chair = chair_crud.chair_login(db=db, chair=new_chair)

    db_patient.chair_id = new_chair.chair_id

    db_chair = (
        db.query(models.Chair).filter(models.Chair.id == new_chair.chair_id).first()
    )

    db_patient.chair = db_chair

    db.commit()
    db.refresh(db_patient)

    return db_patient
