from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db_config import get_async_session


async def test_get_async_session() -> None:
    agen = get_async_session()
    assert isinstance(agen, AsyncGenerator)
    async_session = await anext(agen)
    assert isinstance(async_session, AsyncSession)
