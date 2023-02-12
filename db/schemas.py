from pydantic import BaseModel

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


# * this signup schema used when create signup route to specify the request body
# * it also inherit from the login schema to add the email and password fields and the Config class
class SignUp(Login):
    id: int
    patient_full_name: str
    username: str
    phone_number: str
    address: str
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
                "age": 25,
            }
        }


# * this ChairData schema used when creating a route for the data coming from the rasberry pi
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


class ReadChairData(GetChairData):
    patient_id: int

    class Config:
        schema_extra = {
            "example": {
                "patient_id": 1,
                "body_temperature": 36.5,
                "oximeter": 125.4,
                "heart_rate": 122.5,
                "sugar_level": 70.45,
            }
        }
