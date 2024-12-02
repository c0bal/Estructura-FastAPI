from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from config import Settings, settings


def build_sqlalchemy_database_url_from_settings(_settings: Settings) -> str:
    return (
        f"postgresql://{_settings.DB_USER}:{_settings.DB_PASSWORD}"
        f"@{_settings.DB_HOST}:{_settings.DB_PORT}/{_settings.DB_NAME}"
    )


def get_engine(database_url: str, echo=False) -> Engine:
    engine = create_engine(database_url, echo=echo)
    return engine


def get_local_session(database_url: str, echo=False, **kwargs) -> sessionmaker:
    engine = get_engine(database_url, echo)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return session


SQLALCHEMY_DATABASE_URL = build_sqlalchemy_database_url_from_settings(settings)
