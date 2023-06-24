from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from auth.schema import Token
import db.database as database, api.caregiver_api.db.schemas as schemas, api.caregiver_api.db.crud as crud
from typing import Dict


router = APIRouter(tags=["caregiver"], prefix="/caregiver")


# Creating New CareGiver User In DB
@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(
    caregiver: schemas.SignUpCareGiver,
    authorize: AuthJWT = Depends(),
    db: Session = Depends(database.get_db),
):
    return crud.signup_caregiver(caregiver=caregiver, db=db, authorize=authorize)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(
    caregiver: schemas.Login,
    authorize: AuthJWT = Depends(),
    db: Session = Depends(database.get_db),
):
    return crud.login_caregiver(db=db, authorize=authorize, caregiver=caregiver)


@router.get("/info", response_model=schemas.CareGiverInfo, status_code=200)
async def get_info(
    authorize: AuthJWT = Depends(), db: Session = Depends(database.get_db)
):
    try:
        authorize.jwt_required()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )
    current_user = authorize.get_jwt_subject()
    return crud.caregiver_info(caregiver_id=current_user, db=db)

@router.put("/update/{caregiver_id}", response_model=schemas.CareGiverInfo, status_code=status.HTTP_200_OK)
async def update(
    caregiver_id: int,
    caregiver: schemas.EditProfileCareGiver,
    authorize: AuthJWT = Depends(),
    db: Session = Depends(database.get_db)
):
    return crud.update_caregiver(db=db, authorize=authorize, caregiver_id=caregiver_id, caregiver=caregiver)