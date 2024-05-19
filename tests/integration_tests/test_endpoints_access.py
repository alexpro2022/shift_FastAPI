"""
The module is kept as code example.

"""

from http import HTTPStatus

import pytest
from httpx import AsyncClient

from app.main import app

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
