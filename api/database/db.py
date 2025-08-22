from typing import Generator
from database.session import get_local_session, SQLALCHEMY_DATABASE_URL
from sqlalchemy.ext.declarative import declarative_base
from log import get_logger

log = get_logger(__name__)

Base = declarative_base()

def get_db() -> Generator:
    db = get_local_session(SQLALCHEMY_DATABASE_URL, False)()
    try:
        yield db
    finally:
        db.close()
