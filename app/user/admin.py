import logging
from contextlib import asynccontextmanager

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from config.app_config import app_conf
from config.db_config import get_async_session

from .auth import get_user_manager
from .db import User, get_user_db
from .schemas import UserCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create superuseruser programmatically
async def get_or_create_user(
    email: EmailStr,
    password: str,
    is_superuser: bool = False,
) -> User:
    async with (
        asynccontextmanager(get_async_session)() as session,  # type: ignore
        asynccontextmanager(get_user_db)(session) as user_db,
        asynccontextmanager(get_user_manager)(user_db) as user_manager,
    ):
        try:
            user = await user_manager.create(
                UserCreate(email=email, password=password, is_superuser=is_superuser)
            )
            msg = "Админ создан"
        except UserAlreadyExists:
            user = await user_manager.get_by_email(email)
            msg = "Админ уже существует"
    logger.info(msg)
    return user


async def create_admin() -> User | None:
    if all((app_conf.admin_email, app_conf.admin_password)):
        return await get_or_create_user(
            email=app_conf.admin_email,
            password=app_conf.admin_password,
            is_superuser=True,
        )
    return None
