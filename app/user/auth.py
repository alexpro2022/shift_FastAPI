import uuid
from typing import Annotated

from config.app_config import app_conf
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)

from .db import User, user_db
from .schemas import UserCreate
from .validators import password_content_validator, password_length_validator


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    # reset_password_token_secret = SECRET
    # verification_token_secret = SECRET

    async def validate_password(self, password: str, user: User | UserCreate) -> None:
        password_length_validator(password)
        password_content_validator(password, user.email)

    async def on_after_register(self, user: User, request: Request | None = None):
        print(f"Пользователь {user.email} зарегистрирован.")

    """
    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")
    """


# async def get_user_manager(
# user_db: Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]):
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

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
authorized = Annotated[User, Depends(current_user)]
admin = Annotated[User, Depends(current_superuser)]
