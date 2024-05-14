from pydantic import EmailStr, SecretStr  # noqa
from pydantic_settings import BaseSettings, SettingsConfigDict

DB_URL_PATTERN = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"


class BaseConf(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )
