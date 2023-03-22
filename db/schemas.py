from pydantic import BaseModel

# * Here we put our schemas to be used in the routes and the database models
# * schemas work as blueprints for the database models and the routes request and response bodies


# ? This schema is used to register to the chair when we try
# ? to access chair data to display on the application
class ChairRegistration(BaseModel):
    chair_id: int
    password: str

    class Config:
        orm_mode = True
        schema_extra = {"example": {"chair_id": 55, "password": "mypassword"}}


# ? this GetChairData schema used when creating a route for sending data from database
class GetChairData(BaseModel):
    body_temperature: float
    oximeter: float
    heart_rate: float
    sugar_level: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "body_temperature": 36.5,
                "oximeter": 125.4,
                "heart_rate": 122.5,
                "sugar_level": 70.45,
            }
        }


# ? this ReadChairData schema use when creating a route for the upcoming sensors' data
class ReadChairData(GetChairData):
    chair_id: int

    class Config:
        schema_extra = {
            "example": {
                "body_temperature": 36.5,
                "oximeter": 125.4,
                "heart_rate": 122.5,
                "sugar_level": 70.45,
                "chair_id": 55,
            }
        }


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
            "Example": {
                "id": 1,
                "first_name": "Ahmed",
                "last_name": "Esmail",
                "username": "ahmedesmail07",
                "email": "example@mail.com",
                "password": "mypassword",
                "age": 23,
            }
        }
