from logging import Logger

import pytest
from fastapi_users.authentication import JWTStrategy
from pydantic_core import ValidationError

from app.config.app_config import app_conf
from app.user.admin import create_admin, get_or_create_user
from app.user.auth import get_jwt_strategy
from app.user.db import User
from tests.utils import USER_CREDS, check_user


def test_get_jwt_startegy(monkeypatch):
    mock_counter = 0

    class MockJWTStrategy:
        def __init__(self, secret, lifetime_seconds):
            nonlocal mock_counter
            assert secret == app_conf.secret_key
            assert lifetime_seconds == app_conf.token_lifetime
            mock_counter += 1

    assert isinstance(get_jwt_strategy(), JWTStrategy)
    monkeypatch.setattr("app.user.auth.JWTStrategy", MockJWTStrategy)
    assert isinstance(get_jwt_strategy(), MockJWTStrategy)
    assert mock_counter == 1


@pytest.mark.parametrize(
    "email, password",
    (
        (None, app_conf.admin_password),
        (app_conf.admin_email, None),
    ),
)
async def test_get_or_create_user_invalid_args(
    mock_async_session, email, password
) -> None:
    with pytest.raises(ValidationError):
        await get_or_create_user(email, password)


@pytest.mark.parametrize("is_superuser", (True, False))
async def test_get_or_create_user_creates_new_user(
    mock_async_session, is_superuser
) -> None:
    user = await get_or_create_user(*USER_CREDS, is_superuser)
    check_user(user, is_superuser)


async def test_get_or_create_user_gets_existing_user(
    monkeypatch, mock_async_session
) -> None:
    message = ""
    mock_counter = 0

    class MockLogger(Logger):
        def info(self, msg, *args, **kwargs):
            nonlocal message, mock_counter
            message = msg
            mock_counter += 1

    monkeypatch.setattr("app.user.admin.logger", MockLogger(""))
    # creates new user
    new_user = await get_or_create_user(*USER_CREDS)
    assert isinstance(new_user, User)
    assert message == "Пользователь создан"
    # gets existing user
    existing_user = await get_or_create_user(*USER_CREDS)
    assert isinstance(existing_user, User)
    assert message == "Пользователь уже существует"
    assert new_user._asdict() == existing_user._asdict()
    assert mock_counter == 2


async def test_create_admin(mock_async_session) -> None:
    user = await create_admin()
    assert user is not None
    check_user(user, True)
