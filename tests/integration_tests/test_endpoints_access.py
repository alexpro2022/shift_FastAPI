from http import HTTPStatus

import pytest
from httpx import AsyncClient

from app.config.app_config import app_conf
from app.main import app
from app.models.models import Salary
from tests.utils import db_empty

from ..fixtures import data as d
from .utils import Json, check_response, reverse

# pytestmark = pytest.mark.skipif(..., reason="Not ready yet")


@pytest.mark.parametrize(
    "view_name, expected_result",
    (
        ("get_all_users", d.ALL_USERS),  # needs fixture creating the two users
        ("get_all_salaries", d.ALL_SALARIES),
    ),
)
async def test_get_all_xxx(
    init_db, async_client: AsyncClient, view_name: str, expected_result: Json
) -> None:
    url = reverse(app, view_name)
    response = await async_client.get(url)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert check_response(response_json, expected_result) == "DONE"


async def test_on_register_creates_salary_record(
    init_db, async_client: AsyncClient, get_test_session, mock_async_session
):
    payload = {
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    }
    assert await db_empty(get_test_session, Salary)
    url = app_conf.URL_PREFIX.format("auth/register")
    response = await async_client.post(url, json=payload)
    assert response.status_code == HTTPStatus.CREATED
    assert not await db_empty(get_test_session, Salary)
