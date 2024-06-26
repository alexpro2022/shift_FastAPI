from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db_config import get_async_session
from app.main import app

from .fixtures.db_config import TestingSessionLocal

pytest_plugins = [
    "tests.fixtures.fixtures",
]


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session
