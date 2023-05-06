from pydantic import BaseModel


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
                "password": "mypassword",
            }
        }
