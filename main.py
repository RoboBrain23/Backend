from fastapi import FastAPI
from db.database import engine, SessionLocal
from db.models import Base
from routers.chair import router as chair_router
from routers.patient import router as patient_router

# * Here is the main file that will be used to run the application

app = FastAPI()

# * Create the database tables
Base.metadata.create_all(bind=engine)

# * Include the routers from the other files in the main file to be used by the application
app.include_router(chair_router)
app.include_router(patient_router)
