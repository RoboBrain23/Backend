from sqlalchemy.orm import Session
import db.schemas as schemas, db.models as models
from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

# * here we create our CRUD functions that will be used in our routers

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hashed_password(password: str):
    """
    We use this function to hash our password when we stored in the first time

    Args:
        password (str): The password we want to hash

    Returns:
        str : return the password after being hased
    """

    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    This function compare between the hashed_password we store in database
    and the plain_password that come to use from the request when we try
    to login or validate the information

    Args:
        plain_password (str): The password we want to compare or validate
        hashed_password (str): The hased password that stored in the database

    Returns:
        bool : Return True or False depend on the comparison
    """

    return pwd_context.verify(plain_password, hashed_password)


def generate_tokens(id: int, authorize: AuthJWT):
    """
    This Function Generate our JWT token that will be used to authenticate the user

    Args:
        id (int): The ID that will be encoded to use to access the data
        authorize (AuthJWT): The AuthJWT object that we will use to generate the token

    Returns:
        Dict : return a dictionary that contain the access token and refresh token
    """

    access_token = authorize.create_access_token(subject=id)
    refresh_token = authorize.create_refresh_token(subject=id)

    response = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "message": "Success",
    }
    return jsonable_encoder(response)


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

    db_id = (
        db.query(models.CareGiver).filter(models.CareGiver.id == caregiver.id).first()
    )

    # * Create a new instance of CareGiver model to store the caregiver in the database

    caregiver.id = int(caregiver.id)
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
