import pytest
from config.app_config import app_conf

from app.main import lifespan
from app.user.admin import create_admin, get_or_create_user
from app.user.db import User

# from tests.conftest import override_get_async_session

USER_CREDS = (app_conf.admin_email, app_conf.admin_password)


def check_user(user: User, is_superuser: bool = True) -> None:
    assert user.email == app_conf.admin_email
    assert user.hashed_password
    assert user.is_superuser == is_superuser


# Needs to patch get_async_session with the override_get_async_session


@pytest.mark.parametrize("is_superuser", (True, False))
async def test_create_user(is_superuser) -> None:
    user = await get_or_create_user(
        # override_get_async_session,
        *USER_CREDS,
        is_superuser,
    )
    check_user(user, is_superuser)


async def test_create_user_uniqueness() -> None:
    assert await get_or_create_user(*USER_CREDS)  # override_get_async_session
    assert await get_or_create_user(*USER_CREDS) is None  # override_get_async_session


async def test_create_admin() -> None:
    user = await create_admin()  # override_get_async_session)
    assert user is not None
    check_user(user)


async def test_lifespan() -> None:
    async with lifespan("") as user:  # override_get_async_session
        assert user is not None
        check_user(user)
