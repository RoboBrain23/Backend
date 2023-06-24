from sqlalchemy.orm import Session
import api.chair_api.db.schemas as schemas
import db.models as models
from db.crud import create_hashed_password, verify_password, generate_tokens
from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT


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
        Dict : we return a detail tell us that we store the chair data successfully
    """

    db_chair = (
        db.query(models.Chair).filter(chair.chair_id == models.Chair.parcode).first()
    )

    if db_chair is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Chair ID is already exist",
        )

    new_chair = models.Chair(
        parcode=chair.chair_id, password=create_hashed_password(chair.password)
    )

    db.add(new_chair)
    db.commit()
    db.refresh(new_chair)

    return {"detail": "Chair register successfully"}


def get_chair(db: Session, chair: schemas.ChairRegistration):
    """
    This function validate the data that have been sent to login to specific chair
    First we check if the chair_id is exist in the database then verify and compare
    the password that send with the request
    If everything go well then We return a detail tell us the login done successfully
    if not then return None which means noting found

    Args:
        db (Session): The database session that we will use to validate the data
        chair (schemas.ChairRegistration): The data that we want to validate with stored data (chair_id, password)

    Returns:
        Dict : We return a detail tell us the login done successfully
        None : Return None when no chair exist in the database with this ID and password
    """

    current_chair = (
        db.query(models.Chair).filter(models.Chair.parcode == chair.chair_id).first()
    )

    if current_chair and verify_password(chair.password, current_chair.password):
        return {"detail": "Chair login successfully"}
    return None


def chair_login(
    db: Session, chair: schemas.ChairRegistration, authorize: AuthJWT | None = None
):
    """
    We use this function to login or access the chair with a specific id

    Args:
        db (Session): The database session that we will use to validate the data
        chair (schemas.ChairRegistration): The data that we want to validate with stored data (chair_id, password)

    Raises:
        HTTPException: If the chair_id not exist in the database we raise an exception with status code 404

    Returns:
        Dict : We return a detail tell us the login done successfully
    """

    current_chair = get_chair(db=db, chair=chair)
    if current_chair is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chair ID or Password Invalid"
        )
    if authorize is None:
        return {"details": "Patient Added successfully"}

    return generate_tokens(id=chair.chair_id, authorize=authorize)


def store_chair_data(db: Session, data: schemas.GetChairData, chair_id: int):
    """
    This fucntion used to store the data coming from sensors but only when the chair is existing in the database
    if the chair not found we raise an exception, otherwise we store the data

    Args:
        db (Session): The database session that we will use to validate the data
        data (schemas.ReadChairData): The sensors' data that we want to store in the database

    Raises:
        HTTPException: We check if the chair is exist in the database, if not we raise an exception with code 404

    Returns:
        Dict : we return a detail tell us that the data stored successfully
    """

    db_chair = db.query(models.Chair).filter(models.Chair.parcode == chair_id).first()

    if db_chair is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Chair stored with this ID"
        )

    new_data = models.SensorData(chair_id=chair_id, **data.dict())

    chair = db.query(models.Chair).filter(chair_id == models.Chair.parcode).first()

    new_data.chair = chair

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {"detail": "Data has been stored successfully"}


def get_chair_data(chair_id: int, db: Session):
    """
    This function used to get the latest data of specific chair that have been stored using the chair_id
    that send with the request to the route and return the data if the chair_id exist

    Args:
        chair_id (int): The id of the chair we want to connect to access his data
        db (Session): The database session that we will use to validate the data

    Raises:
        HTTPException: If the ID not found we raise an exception with status code 404
        HTTPException: If there is no Data recorded related to this chair id we raise exception with status code 404

    Returns:
        Dict: We return the data of the sonsors connected to the chair that have id = chair_id
    """
    db_chair = db.query(models.Chair).filter(models.Chair.parcode == chair_id).first()

    if db_chair is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chair not found"
        )

    sensor_data = (
        db.query(models.SensorData)
        .filter(models.SensorData.chair_id == chair_id)
        .order_by(models.SensorData.id.desc())
        .first()
    )

    if sensor_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No data recorded for this chair id",
        )

    return schemas.GetChairData.from_orm(sensor_data)
