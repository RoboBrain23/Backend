from pydantic import BaseModel
from datetime import timedelta


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "b9fa6ccd09b489c17b9b27856fe5a72b3a89df88d9c9b5c86b7bef3867cf0eae"
    )
    authjwt_algorithm: str = "HS256"


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    message: str
