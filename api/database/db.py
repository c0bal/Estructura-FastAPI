from typing import Generator
from database.session import get_local_session, SQLALCHEMY_DATABASE_URL
from log import get_logger


log = get_logger(__name__)


def get_db() -> Generator:
    log.debug("getting database session")
    db = get_local_session(SQLALCHEMY_DATABASE_URL, False)()
    try:
        yield db
    finally:
        log.debug("closing database session")
        db.close()
