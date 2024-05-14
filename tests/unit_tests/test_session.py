from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..conftest import get_async_session


async def test_get_async_session() -> None:
    agen = get_async_session()
    assert isinstance(agen, AsyncGenerator)
    async_session = await anext(agen)
    assert isinstance(async_session, AsyncSession)


"""
from redis import asyncio as aioredis
from ..conftest import get_aioredis

async def test_get_aioredis():
    assert isinstance(get_aioredis(), aioredis.Redis)
"""
