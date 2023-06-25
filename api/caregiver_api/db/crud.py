from sqlalchemy.orm import Session
import api.caregiver_api.db.schemas as schemas, db.models as models
from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from db.crud import create_hashed_password, verify_password, generate_tokens


def signup_caregiver(
    db: Session, authorize: AuthJWT, caregiver: schemas.SignUpCareGiver
):
    # Check for mail if it is stored in the db or not
    db_email = (
        db.query(models.CareGiver)
        .filter(models.CareGiver.email == caregiver.email)
        .first()
    )

    # * if the email is already exist raise an HTTPException with status code 400 and a message
    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already exist",
        )
    db_username = (
        db.query(models.CareGiver)
        .filter(models.CareGiver.username == caregiver.username)
        .first()
    )

    # * if the username is already exist raise an HTTPException with status code 400 and a message
    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already exist",
        )

    # db_id = (
    #     db.query(models.CareGiver).filter(models.CareGiver.id == caregiver.id).first()
    # )

    # * Create a new instance of CareGiver model to store the caregiver in the database

    # caregiver.id = int(caregiver.id)
    caregiver.age = int(caregiver.age)
    caregiver.password = create_hashed_password(caregiver.password)

    new_caregiver = models.CareGiver(**caregiver.dict())

    # * Add the new caregiver to the database session and commit the changes to the database
    db.add(new_caregiver)
    db.commit()
    db.refresh(new_caregiver)

    return generate_tokens(authorize=authorize, id=new_caregiver.id)


def get_caregiver(db: Session, authorize: AuthJWT, caregiver: schemas.Login):
    db_caregiver = (
        db.query(models.CareGiver)
        .filter(caregiver.email == models.CareGiver.email)
        .first()
    )

    if db_caregiver and verify_password(caregiver.password, db_caregiver.password):
        return generate_tokens(authorize=authorize, id=db_caregiver.id)
    return None


def login_caregiver(db: Session, authorize: AuthJWT, caregiver: schemas.Login):
    db_caregiver = get_caregiver(db=db, authorize=authorize, caregiver=caregiver)
    if db_caregiver is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password"
        )
    return db_caregiver


def caregiver_info(db: Session, caregiver_id: int):
    caregiver = (
        db.query(models.CareGiver).filter(models.CareGiver.id == caregiver_id).first()
    )
    return schemas.CareGiverInfo.from_orm(caregiver)


def update_caregiver(
    db: Session,
    authorize: AuthJWT,
    caregiver_id: int,
    caregiver: schemas.EditProfileCareGiver,
):
    # Check if the caregiver with given id exists in the database
    db_caregiver = (
        db.query(models.CareGiver).filter(models.CareGiver.id == caregiver_id).first()
    )
    if not db_caregiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Caregiver not found"
        )

    # Update the caregiver's attributes with the new values
    # May be edited soon
    db_caregiver.first_name = caregiver.first_name
    db_caregiver.last_name = caregiver.last_name
    db_caregiver.username = caregiver.username
    db_caregiver.email = caregiver.email
    db_caregiver.password = caregiver.password
    db_caregiver.age = caregiver.age

    # If the password is provided, hash it and update it in the database
    if caregiver.password:
        db_caregiver.password = create_hashed_password(caregiver.password)

    # Commit the changes to the database
    db.commit()
    db.refresh(db_caregiver)

    return db_caregiver
