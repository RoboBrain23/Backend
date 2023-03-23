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