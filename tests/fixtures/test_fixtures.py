import asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_provided_loop_is_running_loop(
    event_loop: asyncio.AbstractEventLoop,
) -> None:
    assert event_loop is asyncio.get_running_loop()


def test_async_client_fixture(async_client):
    assert isinstance(async_client, AsyncClient)


def test_init_db_fixture(init_db):
    assert init_db


def test_get_test_session_fixture(get_test_session):
    assert isinstance(get_test_session, AsyncSession)
