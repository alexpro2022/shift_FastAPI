from typing import Any, AsyncGenerator, Generator, Literal

import pytest
import pytest_asyncio
from httpx import AsyncClient

from app.main import app
from app.models.base import Base as TestBase
from app.repositories import crud
from app.types import UUID_DEFAULT
from app.user.auth import current_superuser, current_user
from app.user.db import User
from tests.conftest import override_get_async_session
from tests.fixtures.data import DESCR, TITLE, ModelTest

from .db_config import TestingSessionLocal, test_engine


@pytest_asyncio.fixture  # (scope="session")
async def init_db() -> AsyncGenerator[Literal[True], Any]:
    async with test_engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.create_all)
    yield True
    async with test_engine.begin() as conn:
        await conn.run_sync(TestBase.metadata.drop_all)


@pytest_asyncio.fixture
async def get_test_session(init_db) -> AsyncGenerator[None, Any]:
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, Any]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_async_session(monkeypatch, init_db) -> None:
    monkeypatch.setattr("app.user.admin.get_async_session", override_get_async_session)
    monkeypatch.setattr(
        "app.services.salary.get_async_session", override_get_async_session
    )


@pytest.fixture
def create_obj(get_test_session):
    return crud.insert_(get_test_session, ModelTest, title=TITLE, description=DESCR)


@pytest.fixture
def admin_user() -> Generator[None, Any, None]:
    admin = User(
        id=UUID_DEFAULT(),
        is_active=True,
        is_verified=True,
        is_superuser=True,
    )
    app.dependency_overrides[current_superuser] = lambda: admin
    app.dependency_overrides[current_user] = lambda: admin
    yield
    app.dependency_overrides[current_superuser] = current_superuser
    app.dependency_overrides[current_user] = current_user
