from fastapi import FastAPI
from db.database import engine
from db.models import Base
from api.chair_api.routers.chair import router as chair_router
from api.patient_api.routers.patient import router as patient_router
from routers.caregiver import router as caregiver_router
from auth.schema import Settings
from fastapi_jwt_auth import AuthJWT

# * Here is the main file that will be used to run the application

app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


# * Create all the tables in the database if they don't exist already
# ? we can import Base from models.py or from database.py both will work
Base.metadata.create_all(bind=engine)

# * Include the routers from the other files in the main file to be used by the application
app.include_router(chair_router)
app.include_router(patient_router)
app.include_router(caregiver_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
