import uuid

from app.config.db_config import get_async_session
from app.models.models import Salary
from app.repositories import crud


async def create_salary_record(user_id: uuid.UUID):
    async for session in get_async_session():
        await crud.insert_(session, Salary, user_id=user_id)
