import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from log import get_logger

log = get_logger(__name__)

class Settings(BaseSettings):
    ENV: str
    SERVER_HOST: str
    SERVER_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


class DevSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env.dev", env_file_encoding="utf-8", case_sensitive=True
    )


class TestSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env.test", env_file_encoding="utf-8", case_sensitive=True
    )


class LocalSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env.local", env_file_encoding="utf-8", case_sensitive=True
    )


class ProdSettings(Settings):
    model_config = SettingsConfigDict(
        env_file=".env.prod", env_file_encoding="utf-8", case_sensitive=True
    )


def get_settings(env: str = None) -> Settings:
    env = env or os.getenv("ENV", "local").lower()

    log.debug("getting settings for env: %s", env)

    settings_classes = {
        "dev": DevSettings,
        "test": TestSettings,
        "local": LocalSettings,
        "prod": ProdSettings,
    }

    if env not in settings_classes:
        raise ValueError(f"Entorno no válido: {env}. Usa: {', '.join(settings_classes.keys())}.")

    return settings_classes[env]()


settings = get_settings()