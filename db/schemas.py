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


# ? this ChairData schema used when creating a route for the data coming from the rasberry pi
class ReadChairData(BaseModel):
    body_temperature: float
    oximeter: float
    heart_rate: float
    sugar_level: float
    chair_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "body_temperature": 36.5,
                "oximeter": 125.4,
                "heart_rate": 122.5,
                "sugar_level": 70.45,
                "chair_id": 55,
            }
        }
