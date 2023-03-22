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
    temperature: float
    oximeter: float
    pulse_rate: float
    sugar_level: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "temperature": 36.5,
                "oximeter": 125.4,
                "pulse_rate": 122.5,
                "sugar_level": 70.45,
            }
        }


# ? this ReadChairData schema use when creating a route for the upcoming sensors' data
class ReadChairData(GetChairData):
    chair_id: int

    class Config:
        schema_extra = {
            "example": {
                "temperature": 36.5,
                "oximeter": 125.4,
                "pulse_rate": 122.5,
                "sugar_level": 70.45,
                "chair_id": 55,
            }
        }


class PatientData(BaseModel):
    first_name: str
    last_name: str
    gender: str
    age: int
    chair_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "example@mail.com",
                "password": "mypassword",
            }
        }


# * this signup schema used when create signup route to specify the request body
# * it also inherit from the login schema to add the email and password fields and the Config class
class SignUp(Login):
    id: int
    patient_full_name: str
    username: str
    phone_number: str
    address: str
    gender: str
    age: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "patient_full_name": "Mohamed Ali",
                "username": "moAli123",
                "password": "mypassword",
                "email": "example@mail.com",
                "phone_number": "0111122234",
                "address": "Zagazig, Egypt",
                "gender": "male",
                "age": 25,
            }
        }


class Info(BaseModel):
    id: int
    patient_full_name: str
    email: str
    username: str
    phone_number: str
    address: str
    gender: str
    age: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "patient_full_name": "Mohamed Ali",
                "username": "moAli123",
                "email": "example@mail.com",
                "phone_number": "0111122234",
                "address": "Zagazig, Egypt",
                "gender": "male",
                "age": 25,
            }
        }
