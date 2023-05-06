from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

# * here we create our CRUD functions that will be used in our routers

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hashed_password(password: str):
    """
    We use this function to hash our password when we stored in the first time

    Args:
        password (str): The password we want to hash

    Returns:
        str : return the password after being hased
    """

    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    This function compare between the hashed_password we store in database
    and the plain_password that come to use from the request when we try
    to login or validate the information

    Args:
        plain_password (str): The password we want to compare or validate
        hashed_password (str): The hased password that stored in the database

    Returns:
        bool : Return True or False depend on the comparison
    """

    return pwd_context.verify(plain_password, hashed_password)


def generate_tokens(id: int, authorize: AuthJWT):
    """
    This Function Generate our JWT token that will be used to authenticate the user

    Args:
        id (int): The ID that will be encoded to use to access the data
        authorize (AuthJWT): The AuthJWT object that we will use to generate the token

    Returns:
        Dict : return a dictionary that contain the access token and refresh token
    """

    access_token = authorize.create_access_token(subject=id)
    refresh_token = authorize.create_refresh_token(subject=id)

    response = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "message": "Success",
    }
    return jsonable_encoder(response)
