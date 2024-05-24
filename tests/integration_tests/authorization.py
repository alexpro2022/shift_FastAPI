import uuid
from http import HTTPStatus

from httpx import AsyncClient

from app.config.app_config import app_conf
from app.models.models import User
from tests.fixtures import data as d
from tests.utils import db_empty

REGISTER_URL = app_conf.URL_PREFIX.format("auth/register")
LOGIN_URL = app_conf.URL_PREFIX.format("auth/jwt/login")


async def _post(client: AsyncClient, url: str, **kwargs):  # ,user_payload: dict):
    response = await client.post(url, **kwargs)  # json=user_payload)
    assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)
    return response


async def register_user(client: AsyncClient, session) -> uuid.UUID:
    assert await db_empty(session, User)
    # response = await client.post(URL, json=d.USER_REGISTER_DATA)
    # assert response.status_code == HTTPStatus.CREATED
    response = await _post(client, REGISTER_URL, json=d.USER_REGISTER_DATA)
    assert not await db_empty(session, User)
    return response.json()["id"]


async def get_registered(client: AsyncClient, user: dict) -> None:
    # response = await async_client.post(URL, json=user)
    # assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED)
    response = await _post(client, REGISTER_URL, json=user)
    created_user = response.json()
    # assert isinstance(created_user['id'], uuid.UUID), created_user['id']
    assert created_user.get("id") is not None
    assert created_user.get("password") is None
    for key in ("email", "is_active", "is_superuser", "is_verified"):
        assert created_user[key] == user[key]
    # assert auth_user['is_active'] == True
    # assert auth_user['is_superuser'] == False
    # assert auth_user['is_verified'] == False


async def get_auth_user_token(
    client: AsyncClient, user: dict = d.USER_REGISTER_DATA, registration: bool = True
) -> str:
    if registration:
        await get_registered(client, user)
    user = user.copy()
    user["username"] = user["email"]
    # response = await client.post(LOGIN_URL, data=user)
    # assert response.status_code == HTTPStatus.OK
    response = await _post(client, LOGIN_URL, data=user)
    token = response.json()["access_token"]
    assert isinstance(token, str)
    return token


def get_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
