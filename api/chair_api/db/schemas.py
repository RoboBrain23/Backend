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
        schema_extra = {
            "example": {
                "chair_id": 55,
                "password": "mypassword",
            }
        }


# ? this GetChairData schema used when creating a route for sending data from database
class GetChairData(BaseModel):
    temperature: float
    oximeter: float
    pulse_rate: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "temperature": 36.5,
                "oximeter": 125.4,
                "pulse_rate": 122.5,
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
                "chair_id": 55,
            }
        }


class GetChairLocation(BaseModel):
    latitude: float
    longitude: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "latitude": 12.123456,
                "longitude": 47.154789,
            }
        }


class StoreChairLocation(GetChairLocation):
    chair_id: int

    class Config:
        schema_extra = {
            "example": {
                "latitude": 12.123456,
                "longitude": 47.154789,
                "chair_id": 55,
            }
        }
