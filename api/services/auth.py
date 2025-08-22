from models import User
from sqlalchemy.orm import Session
from services.security import verify_password, create_access_token, decode_token
from cruds import user_crud
from fastapi import HTTPException, Depends
from database.db import get_db
from log import get_logger
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

log = get_logger(__name__)

async def authenticate_user(db: Session, email: str, password: str):
    user = user_crud.get_one(db, email=email)
    if not user:
        raise HTTPException(status_code=401, detail="Email not found")
    if not await verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return user

async def login_user(db: Session, email: str, password: str):
    user = await authenticate_user(db, email, password)
    return await create_access_token({"sub": user.email})

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Token not found")

    payload = await decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = user_crud.get_one(db, email=payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

async def is_admin(user: User = Depends(get_current_user)):
    """Checks if the user has administrator permissions."""
    if not user.email == "admin@example.com":
        raise HTTPException(status_code=403, detail="You do not have permission to perform this action")
    return user
