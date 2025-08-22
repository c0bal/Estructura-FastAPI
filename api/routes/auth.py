from fastapi import APIRouter, Depends, Response, HTTPException, Request
from sqlalchemy.orm import Session
from services.auth import login_user
from services.security import hash_password
from database.db import get_db
from fastapi.security import OAuth2PasswordRequestForm
from schemas.user import UserCreate, UserCreateHashed
from cruds import user_crud


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_crud.get_one(db, email=user_in.email)

    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    existing_user = user_crud.get_one(db, username=user_in.username)

    if existing_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado.")

    hashed = await hash_password(user_in.password)
    user_hashed = UserCreateHashed(**user_in.dict(), hashed_password=hashed)
    user = user_crud.create(db, obj_create=user_hashed)

    if not user:
        raise HTTPException(status_code=500, detail="Error al crear el usuario.")
    return {"message": "Registro exitoso"}


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = await login_user(db, email=form_data.username, password=form_data.password)
    return {
        "access_token": token,
        "token_type": "bearer"
    }
