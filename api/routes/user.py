from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from cruds import user_crud
from schemas.user import UserUpdate, UserResponse
from database.db import get_db
from services.auth import get_current_user
from services.security import hash_password
from models import User

router = APIRouter(prefix="/user", tags=["User"])


@router.get("", response_model=UserResponse)
async def get_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.patch("", response_model=UserResponse)
async def update_user_profile(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the profile of the currently authenticated user. Only update fields that are provided in the request.
    """
    if user_in.password:
        hashed = await hash_password(user_in.password)
        user_in = User(**user_in.dict(exclude={"password"}))
        user_in.hashed_password = hashed

    return user_crud.update(db, current_user, user_in)


@router.delete("", response_model=dict)
async def delete_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete the profile of the currently authenticated user.
    """
    user_crud.delete(db, current_user)
    return {"message": "User successfully deleted."}
