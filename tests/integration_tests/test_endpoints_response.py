import uuid
from http import HTTPStatus

import pytest
from httpx import AsyncClient

from app.models.models import Salary
from app.repositories import crud
from tests.fixtures import data as d
from tests.integration_tests.authorization import register_user
from tests.integration_tests.utils import Json, check_response, request
from tests.utils import db_empty


@pytest.mark.parametrize(
    "view_name, expected_result",
    (
        ("get_all_users", d.ALL_USERS),
        ("get_all_salaries", d.ALL_SALARIES),
    ),
)
async def test_get_all_responses(
    init_db,
    async_client: AsyncClient,
    admin_user,
    view_name: str,
    expected_result: Json,
) -> None:
    response = await request(async_client, view_name)
    assert response.status_code == HTTPStatus.OK
    assert check_response(response.json(), expected_result) == "DONE"


async def test_admin_has_no_salary_records(
    init_db, admin_user, async_client: AsyncClient
) -> None:
    response = await request(async_client, "get_my_salary")
    assert response.status_code == HTTPStatus.NOT_FOUND
    expected_result = {"detail": "У админов нет записей в БД зарплат."}
    assert check_response(response.json(), expected_result) == "DONE"


async def test_on_register_creates_salary_record(
    async_client: AsyncClient,
    get_test_session,
    mock_async_session,
) -> None:
    assert await db_empty(get_test_session, Salary)
    user_id = await register_user(async_client, get_test_session)
    assert not await db_empty(get_test_session, Salary)
    salaries = await crud.get_all(get_test_session, Salary)
    assert len(salaries) == 1
    salary: Salary = salaries[0]
    assert salary.inc_date is None
    assert salary.value is None
    assert isinstance(salary.id, uuid.UUID)
    assert isinstance(salary.user_id, uuid.UUID)
    assert str(salary.user_id) == user_id


async def test_update_salary(
    async_client: AsyncClient, get_test_session, mock_async_session, admin_user
):
    user_id = await register_user(async_client, get_test_session)
    response = await request(async_client, "update_salary", user_id)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    salary: Salary = await crud.get(
        get_test_session, Salary, fetch_one=True, user_id=user_id
    )
    assert str(salary.inc_date) == str(d.SALARY_UPDATE_DATA["inc_date"])
    assert str(salary.value) == str(d.SALARY_UPDATE_DATA["value"])
    assert response_json.keys() == salary._asdict().keys()
    assert set(response_json.values()) == set(map(str, salary._asdict().values()))
