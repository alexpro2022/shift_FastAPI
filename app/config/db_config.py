from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config._base import DB_URL_PATTERN, BaseConf, SecretStr
from app.types import AsyncGenAsyncSession


class Settings(BaseConf):
    postgres_user: SecretStr = "postgres"
    postgres_password: SecretStr = "postgrespw"
    db_host: str = "db"
    db_port: SecretStr = "5432"
    db_name: SecretStr = "postgres"

    @property
    def database_url(self) -> str:
        return DB_URL_PATTERN.format(
            user=self.postgres_user.get_secret_value(),
            password=self.postgres_password.get_secret_value(),
            host=self.db_host,
            port=int(self.db_port.get_secret_value()),
            db_name=self.db_name.get_secret_value(),
        )


db_conf = Settings()
engine = create_async_engine(db_conf.database_url, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenAsyncSession:
    async with AsyncSessionLocal() as async_session:
        yield async_session


async_session = Annotated[AsyncSession, Depends(get_async_session)]
