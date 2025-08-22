from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from models import User
from services.auth import is_admin
from cruds import user_crud

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users")
async def get_users(db: Session = Depends(get_db), _: User = Depends(is_admin)):
    users = user_crud.get_many(db)
    return users
