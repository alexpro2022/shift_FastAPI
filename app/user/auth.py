from typing import Annotated

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from app.config.app_config import app_conf
from app.services.admin import notify_admin
from app.services.salary import create_salary_record
from app.types import UUID_ID

from .db import User, user_db
from .schemas import UserCreate
from .validators import password_content_validator, password_length_validator


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID_ID]):
    async def validate_password(self, password: str, user: User | UserCreate) -> None:
        password_length_validator(password)
        password_content_validator(password, user.email)

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"Пользователь {user.email} зарегистрирован.")
        if not user.is_superuser:
            await create_salary_record(user_id=user.id)
            await notify_admin(user_id=user.id)


async def get_user_manager(user_db: user_db):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=app_conf.secret_key, lifetime_seconds=app_conf.token_lifetime
    )


auth_backend = AuthenticationBackend(
    name=app_conf.auth_backend_name,
    transport=BearerTransport(tokenUrl=app_conf.token_url),
    get_strategy=get_jwt_strategy,
)

user_manager = Annotated[UserManager, Depends(get_user_manager)]
fastapi_users = FastAPIUsers[User, UUID_ID](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
authorized = Annotated[User, Depends(current_user)]
admin = Depends(current_superuser)
