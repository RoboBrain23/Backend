from sqlalchemy.orm import Session
import api.caregiver_api.db.schemas as schemas, db.models as models
from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import desc
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


def get_notification(db: Session, caregiver_id: int):
    notifications = (
        db.query(models.Notification)
        .filter(caregiver_id == models.Notification.caregiver_id)
        .order_by(desc(models.Notification.date))
        .all()
    )

    if len(notifications) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No notification found"
        )

    for notification in notifications:
        chair = db.query(models.Chair).get(notification.chair_id)
        notification.chair_id = chair.parcode

    return notifications


def create_notification(
    db: Session, notification: schemas.StoreNotification, caregiver_id: int
):
    chair = (
        db.query(models.Chair)
        .filter(notification.chair_id == models.Chair.parcode)
        .first()
    )

    if chair is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chair Not Found"
        )

    caregiver = (
        db.query(models.CareGiver).filter(caregiver_id == models.CareGiver.id).first()
    )

    if caregiver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chair Not Found"
        )

    new_notification = models.Notification(
        sensor=notification.sensor,
        value=notification.value,
        chair_id=chair.id,
        caregiver_id=caregiver.id,
    )

    db.add(new_notification)
    db.commit()
    db.refresh(new_notification)

    return {"details": "Notifications stored successfully"}


def delete_notification(db: Session, notification_id: int):
    wanted_notification = (
        db.query(models.Notification)
        .filter(models.Notification.id == notification_id)
        .first()
    )
    if wanted_notification is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found"
        )

    db.delete(wanted_notification)
    db.commit()

    return {"details": "Notification deleted successfully"}


def get_chair_location(db: Session, chair_id: int):
    chair = db.query(models.Chair).filter(models.Chair.parcode == chair_id).first()

    if chair is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chair not found"
        )

    current_location = (
        db.query(models.Location)
        .filter(models.Location.chair_id == chair.id)
        .order_by(desc(models.Location.id))
        .first()
    )

    if current_location is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Location found"
        )

    return current_location
