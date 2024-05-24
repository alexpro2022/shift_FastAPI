from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db_config import get_async_session


async def test_get_async_session() -> None:
    # long check
    agen = get_async_session()
    assert isinstance(agen, AsyncGenerator)
    session = await anext(agen)
    assert isinstance(session, AsyncSession)
    # short check
    async for session in get_async_session():
        assert isinstance(session, AsyncSession)
