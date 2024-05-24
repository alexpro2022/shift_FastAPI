from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.messages import MSG_OBJECT_NOT_FOUND
from app.types import UUID_ID


async def fetch_one(session: AsyncSession, stmt):
    result = await session.scalars(stmt)
    await session.commit()
    return result.first()


async def insert_(session: AsyncSession, model, **create_data):
    stmt = insert(model).values(**create_data).returning(model)
    return await fetch_one(session, stmt)


async def update_(session: AsyncSession, model, id, **update_data):
    stmt = update(model).where(model.id == id).values(**update_data).returning(model)
    return await fetch_one(session, stmt)


async def get(
    session: AsyncSession,
    model,
    exception: bool = False,
    msg: str = MSG_OBJECT_NOT_FOUND,
    fetch_one: bool = False,
    **filter_data,
):
    stmt = select(model).filter_by(**filter_data)
    result = await session.scalars(stmt)
    res = result.first() if filter_data.get("id") or fetch_one else result.all()
    if not res and exception:
        raise HTTPException(status.HTTP_404_NOT_FOUND, msg)
    return res


async def get_all(session: AsyncSession, model):
    return await get(session, model)


async def get_or_404(session: AsyncSession, model, id: int | UUID_ID):
    return await get(session, model, exception=True, id=id)
