from pydantic import BaseModel, Field
from typing import Optional
from typing import List
from datetime import datetime

# * Here we put our schemas to be used in the routes and the database models
# * schemas work as blueprints for the database models and the routes request and response bodies


# * this login schema used when create login route to specify the request body
class Login(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "example@mail.com",
                "password": "mypassword",
            }
        }


class SignUpCareGiver(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    age: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "first_name": "Ahmed",
                "last_name": "Esmail",
                "username": "ahmedesmail07",
                "email": "example@mail.com",
                "password": "mypassword",
                "age": 23,
            }
        }


class CareGiverInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    age: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Ahmed",
                "last_name": "Esmail",
                "username": "ahmedesmail07",
                "email": "example@mail.com",
                "password": "mypassword",
                "age": 23,
            }
        }


class EditProfileCareGiver(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str
    age: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "first_name": "Ahmed",
                "last_name": "Ali",
                "username": "manga07",
                "email": "manga@mail.com",
                "password": "examplepassword",
                "age": 23,
            }
        }


class CareGiverAssignment(BaseModel):
    caregiver_id: int
    patient_ids: List[int]


class StoreNotification(BaseModel):
    sensor: str
    value: float
    chair_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "sensor": "Body temperature",
                "value": 37.5,
                "chair_id": 77,
            }
        }


class GetNotification(StoreNotification):
    date: datetime

    class Config:
        schema_extra = {
            "example": {
                "sensor": "Body temperature",
                "value": 37.5,
                "chair_id": 77,
                "date": "2023-07-04T09:45:00",
            }
        }
