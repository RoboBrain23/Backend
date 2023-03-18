from sqlalchemy.orm import Session
import db.schemas as schemas, db.models as models
from fastapi import HTTPException, status, Depends
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


def chair_signup(db: Session, chair: schemas.ChairRegistration):
    """
    We use this function to store the new chair in the database
    We first check if the id that send with the data is already stored in the database or not
    if it stored we raise an exception if not we stored the chair in our database

    Args:
        db (Session): The database session that we will use to store the data
        chair (schemas.ChairRegistration): The data that we want to store in the database (chair_id, password)

    Raises:
        HTTPException: If the chair_id already exist in the database we raise exception with status code 400

    Returns:
        Dict : we return a message tell us that we store the chair data successfully
    """

    db_chair = db.query(models.Chair).filter(chair.chair_id == models.Chair.id).first()

    if db_chair is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Chair ID is already exist",
        )

    new_chair = models.Chair(
        id=chair.chair_id, password=create_hashed_password(chair.password)
    )

    db.add(new_chair)
    db.commit()
    db.refresh(new_chair)

    return {"message": "Chair register successfully"}


def get_chair(db: Session, authorize: AuthJWT, chair: schemas.ChairRegistration):
    """
    This function validate the data that have been sent to login to specific chair
    First we check if the chair_id is exist in the database then verify and compare
    the password that send with the request
    If everything go well then We return a message tell us the login done successfully
    if not then return None which means noting found

    Args:
        db (Session): The database session that we will use to validate the data
        chair (schemas.ChairRegistration): The data that we want to validate with stored data (chair_id, password)
        authorize (AuthJWT): The AuthJWT object that we will use to generate the token

    Returns:
        Dict : We return a message tell us the login done successfully
        None : Return None when no chair exist in the database with this ID and password
    """

    current_chair = (
        db.query(models.Chair).filter(models.Chair.id == chair.chair_id).first()
    )

    if current_chair and verify_password(chair.password, current_chair.password):
        return generate_tokens(id=current_chair.id, authorize=authorize)
    return None


def chair_login(db: Session, authorize: AuthJWT, chair: schemas.ChairRegistration):
    """
    We use this function to login or access the chair with a specific id

    Args:
        db (Session): The database session that we will use to validate the data
        chair (schemas.ChairRegistration): The data that we want to validate with stored data (chair_id, password)
        authorize (AuthJWT): The AuthJWT object that we will use to generate the token

    Raises:
        HTTPException: If the chair_id not exist in the database we raise an exception with status code 404

    Returns:
        Dict : We return a message tell us the login done successfully
    """

    current_chair = get_chair(db=db, chair=chair, authorize=authorize)
    if current_chair is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chair ID or Password Invalid"
        )
    return current_chair


def store_chair_data(db: Session, data: schemas.ReadChairData):
    """
    This fucntion used to store the data coming from sensors but only when the chair is existing in the database
    if the chair not found we raise an exception, otherwise we store the data

    Args:
        db (Session): The database session that we will use to validate the data
        data (schemas.ReadChairData): The sensors' data that we want to store in the database

    Raises:
        HTTPException: We check if the chair is exist in the database, if not we raise an exception with code 404

    Returns:
        Dict : we return a message tell us that the data stored successfully
    """

    db_chair = db.query(models.Chair).filter(models.Chair.id == data.chair_id).first()

    if db_chair is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Chair stored with this ID"
        )

    new_data = models.SensorData(**data.dict())

    chair = db.query(models.Chair).filter(data.chair_id == models.Chair.id).first()

    new_data.chair = chair

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {"message": "Data has been stored successfully"}


def get_chair_data(chair_id: int, db: Session):
    """
    This function used to get the latest data of specific chair that have been stored using the chair_id
    that send with the request to the route and return the data if the chair_id exist

    Args:
        chair_id (int): The id of the chair we want to connect to access his data
        db (Session): The database session that we will use to validate the data

    Raises:
        HTTPException: If the ID not found we raise an exception with status code 404

    Returns:
        Dict: We return the data of the sonsors connected to the chair that have id = chair_id
    """
    sensor_data = (
        db.query(models.SensorData)
        .filter(models.SensorData.chair_id == chair_id)
        .order_by(models.SensorData.id.desc())
        .first()
    )

    if sensor_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data not found"
        )

    return schemas.GetChairData.from_orm(sensor_data)


def add_new_patient(db: Session, patient: schemas.PatientData, chair_id: int):
    """
    We use this function to store the patient's data in the database
    with the chair_id they use

    Args:
        db (Session): The database session that we will use to validate the data
        patient (schemas.PatientData): The patient's data that we want to store in the database
        chair_id (int): The chair_id of the chair that the patient use and stored in the token

    Returns:
        Dict: we return a Dict message tell us we stored patient's data successfully
    """

    new_patient = models.Patient(
        first_name=patient.first_name,
        last_name=patient.last_name,
        gender=patient.gender,
        age=int(patient.age),
        chair_id=chair_id,
    )

    chair = db.query(models.Chair).filter(models.Chair.id == chair_id).first()

    new_patient.chair = chair

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {"message": "Patient's data stored successfully"}


def patient_info(chair_id: int, db: Session):
    db_patient = (
        db.query(models.Patient).filter(chair_id == models.Patient.chair_id).first()
    )

    if db_patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Patient currently use this chair",
        )

    return db_patient


# * Create a function that will store the patient in the database when POST request is sent to the route


# @param db: Session ==> this is the database session that we will use to store the data in the database
# @param patient: schemas.Patient ==> this is the patient that we will store in the database
def signup(db: Session, authorize: AuthJWT, patient: schemas.SignUp):
    # * Check if the email is already exist in the database
    db_email = (
        db.query(models.Patient).filter(models.Patient.email == patient.email).first()
    )

    # * if the email is already exist raise an HTTPException with status code 400 and a message
    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already exist",
        )

    # * Check the username is already exist in the database
    db_username = (
        db.query(models.Patient)
        .filter(models.Patient.username == patient.username)
        .first()
    )

    # * if the username is already exist raise an HTTPException with status code 400 and a message
    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already exist",
        )

    db_id = db.query(models.Patient).filter(models.Patient.id == patient.id).first()

    # * if the username is already exist raise an HTTPException with status code 400 and a message
    if db_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This id is already exist",
        )

    db_phone_number = (
        db.query(models.Patient)
        .filter(models.Patient.phone_number == patient.phone_number)
        .first()
    )

    # * if the username is already exist raise an HTTPException with status code 400 and a message
    if db_phone_number is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Phone Number is already exist",
        )

    # * Create a new instance of Patient model to store the patient in the database

    patient.id = int(patient.id)
    patient.age = int(patient.age)
    patient.password = create_hashed_password(patient.password)

    new_patient = models.Patient(**patient.dict())

    # * Add the new patient to the database session and commit the changes to the database
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return generate_tokens(authorize=authorize, id=new_patient.id)


def get_user(db: Session, authorize: AuthJWT, patient: schemas.Login):
    user = (
        db.query(models.Patient).filter(patient.email == models.Patient.email).first()
    )
    if user and verify_password(patient.password, user.password):
        return generate_tokens(authorize=authorize, id=user.id)
    return None


def login(db: Session, authorize: AuthJWT, patient: schemas.Login):
    user = get_user(db=db, authorize=authorize, patient=patient)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password"
        )
    return user


def user_info(db: Session, user_id: int):
    user = db.query(models.Patient).filter(models.Patient.id == user_id).first()
    return schemas.Info.from_orm(user)
