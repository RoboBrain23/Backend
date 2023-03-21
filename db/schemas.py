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
                "first_name": "Mohamed",
                "last_name": "Badr",
                "gender": "male",
                "age": 23,
                "chair_id": 7,
            }
        }

class PatientDataRegister(PatientData):
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "first_name": "Mohamed",
                "last_name": "Badr",
                "gender": "male",
                "age": 23,
                "chair_id": 55,
                "password": "mypassword"
            }
        }