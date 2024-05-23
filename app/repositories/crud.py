import uuid

from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

MSG_OBJECT_NOT_FOUND = "Объект не найден"


async def fetch_one(session: AsyncSession, stmt):
    result = await session.scalars(stmt)
    return result.first()


async def insert_(session: AsyncSession, model, **create_data):
    stmt = insert(model).values(**create_data).returning(model)
    return await fetch_one(session, stmt)


async def update_(session: AsyncSession, model, id, **update_data):
    stmt = update(model).where(model.id == id).values(**update_data).returning(model)
    return await fetch_one(session, stmt)


async def get(session: AsyncSession, model, exception: bool = False, **filter_data):
    stmt = select(model).filter_by(**filter_data)
    result = await session.scalars(stmt)
    res = result.all() if filter_data.get("id") is None else result.first()
    if not res and exception:
        raise HTTPException(status.HTTP_404_NOT_FOUND, MSG_OBJECT_NOT_FOUND)
    return res


async def get_all(session: AsyncSession, model):
    return await get(session, model)


async def get_or_404(session: AsyncSession, model, id: int | uuid.UUID):
    return await get(session, model, exception=True, id=id)


'''
from sqlalchemy.exc import IntegrityError
from . import exceptions as exc


async def create(session: AsyncSession, obj):
    session.add(obj)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise exc.ObjectExistsError("Объект уже существует.")
    await session.refresh(obj)
    return obj



async def create(obj, asession: async_sessionmaker[AsyncSession] = async_session):
    """Saves `obj` to DB or raises `ObjectExistsError` if object already exists."""
    async with asession() as session:
        session.add(obj)
        try:
            await session.commit()
        except exc.IntegrityError:
            await session.rollback()
            raise ObjectExistsError("Объект уже существует.")
        await session.refresh(obj)
    return obj


async def get(
    model,
    asession: async_sessionmaker[AsyncSession] = async_session,
    exception: bool = False,
    **kwargs,
):
    """Returns `list[obj]` if no `id` in `kwargs` else the `obj`."""
    stmt = select(model).filter_by(**kwargs)
    async with asession() as session:
        result = await session.scalars(stmt)
    res = result.all() if kwargs.get("id") is None else result.first()
    if not res and exception:
        raise ObjectNotFoundError("Объект не найден")
    return res


async def get_or_404(
    model, id: int, asession: async_sessionmaker[AsyncSession] = async_session
):
    """Returns `obj` found by `id` else raises `ObjectNotFoundError`."""
    return await get(model, asession, exception=True, id=id)


async def get_all(model, asession: async_sessionmaker[AsyncSession] = async_session):
    """Returns list of all DB records of the model if any or empty list []."""
    return await get(model, asession)
'''
