from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import db.schemas as schemas, db.database as database, db.crud as crud, db.models as models

router = APIRouter(tags=["patient"], prefix="/patient")

# * Create all the tables in the database if they don't exist already
# ? we can import Base from models.py or from database.py both will work
models.Base.metadata.create_all(bind=database.engine)


# * Create a route that will register a new patient in the database when POST request is sent to the route
@router.post(
    "/signup", response_model=schemas.SignUp, status_code=status.HTTP_201_CREATED
)
async def signup(patient: schemas.SignUp, db: Session = Depends(database.get_db)):
    return crud.signup(patient=patient, db=db)


# TODO: Create 2 Routes

# ? Create a route that will login the patient
# * POST  ==>  "/login"

# ? Create a route that will return the patient data when authontication is successful
# * GET  ==>  "/me"
