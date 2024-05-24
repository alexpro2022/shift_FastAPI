from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.config._base import DB_URL_PATTERN, BaseConf


class Settings(BaseConf):
    postgres_user_test: str = "postgres"
    postgres_password_test: str = "postgrespw"
    db_host_test: str = "0.0.0.0"
    db_port_test: str = "5432"
    db_name_test: str = "postgres"

    @property
    def test_db_url(self) -> str:
        return DB_URL_PATTERN.format(
            user=self.postgres_user_test,
            password=self.postgres_password_test,
            host=self.db_host_test,
            port=int(self.db_port_test),
            db_name=self.db_name_test,
        )


test_db_conf = Settings()
test_engine = create_async_engine(test_db_conf.test_db_url, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(
    test_engine, expire_on_commit=False, autocommit=False, autoflush=False
)
