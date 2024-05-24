from http import HTTPStatus

from httpx import AsyncClient

from app.config.app_config import app_conf
from app.models.models import User
from app.types import UUID_ID
from tests.fixtures import data as d
from tests.utils import db_empty

REGISTER_URL = app_conf.URL_PREFIX.format("auth/register")
LOGIN_URL = app_conf.URL_PREFIX.format("auth/jwt/login")


async def _post(client: AsyncClient, url: str, **kwargs):
    response = await client.post(url, **kwargs)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)
    return response


async def register_user(client: AsyncClient, session) -> UUID_ID:
    assert await db_empty(session, User)
    response = await _post(client, REGISTER_URL, json=d.USER_REGISTER_DATA)
    assert not await db_empty(session, User)
    return response.json()["id"]


async def get_registered(client: AsyncClient, user: dict) -> None:
    response = await _post(client, REGISTER_URL, json=user)
    created_user = response.json()
    assert created_user.get("id") is not None
    assert created_user.get("password") is None
    for key in ("email", "is_active", "is_superuser", "is_verified"):
        assert created_user[key] == user[key]


async def get_auth_user_token(
    client: AsyncClient, user: dict = d.USER_REGISTER_DATA, registration: bool = True
) -> str:
    if registration:
        await get_registered(client, user)
    user = user.copy()
    user["username"] = user["email"]
    response = await _post(client, LOGIN_URL, data=user)
    token = response.json()["access_token"]
    assert isinstance(token, str)
    return token


def get_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
