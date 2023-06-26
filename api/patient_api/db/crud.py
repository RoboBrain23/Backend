from sqlalchemy.orm import Session
import db.models as models
from api.chair_api.db.schemas import ChairRegistration
from api.patient_api.db.schemas import PatientDataRegister
import api.chair_api.db.crud as chair_crud
from fastapi import HTTPException, status


def patient_info(chair_id: int, db: Session, update: bool | None = None):
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

    db_chair = db.query(models.Chair).filter(models.Chair.parcode == chair_id).first()

    if db_chair is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Chair with such ID."
        )

    db_patient = (
        db.query(models.Patient).filter(db_chair.id == models.Patient.chair_id).first()
    )

    if db_patient is None and update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Patient currently use this chair",
        )
    elif db_patient is None and update:
        return None

    db_patient.chair_id = db_chair.parcode

    return db_patient


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

    chair = (
        db.query(models.Chair).filter(models.Chair.parcode == patient.chair_id).first()
    )

    if not chair.available and db_chair:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Chair is already in use.",
        )

    new_patient = models.Patient(
        first_name=patient.first_name,
        last_name=patient.last_name,
        gender=patient.gender,
        age=int(patient.age),
        chair_id=patient.chair_id,
    )

    new_patient.chair = chair

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    chair.parcode = chair.parcode
    chair.password = chair.password
    chair.available = False

    db.commit()
    db.refresh(chair)

    new_patient.chair_id = chair.parcode

    return new_patient


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
    db_patient = patient_info(chair_id=current_chair_id, db=db)

    login_to_new_chair = chair_crud.chair_login(db=db, chair=new_chair)

    new_chair_info = (
        db.query(models.Chair)
        .filter(models.Chair.parcode == new_chair.chair_id)
        .first()
    )

    if login_to_new_chair and not new_chair_info.available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This chair is already connected to other patient",
        )

    db_patient.chair_id = new_chair.chair_id

    db_patient.chair = new_chair_info

    db.commit()
    db.refresh(db_patient)

    new_chair_info.available = False

    old_chair = (
        db.query(models.Chair).filter(models.Chair.parcode == current_chair_id).first()
    )
    old_chair.available = True

    db.commit()
    db.refresh(new_chair_info)
    db.refresh(old_chair)

    return {"details": "Patient Chair update successfully."}
