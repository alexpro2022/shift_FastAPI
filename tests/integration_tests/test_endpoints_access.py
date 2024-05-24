from http import HTTPStatus

import pytest
from httpx import AsyncClient

from tests.integration_tests.authorization import get_auth_user_token, get_headers
from tests.integration_tests.utils import has_access, request

ADMIN_ENDPOINTS_VIEWS = ("get_all_users", "get_all_salaries", "update_salary")
AUTH_USER_ENDPOINT_VIEW = "get_my_salary"
ALL_ENDPOINTS_VIEWS = (*ADMIN_ENDPOINTS_VIEWS, AUTH_USER_ENDPOINT_VIEW)


# ANON USER - No access to all endpoints
@pytest.mark.parametrize("view_name", ALL_ENDPOINTS_VIEWS)
async def test_anon_has_no_access(init_db, async_client: AsyncClient, view_name: str):
    response = await request(async_client, view_name)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


# ADMIN USER - Full access to all endpoints
@pytest.mark.parametrize("view_name", ALL_ENDPOINTS_VIEWS)
async def test_admin_has_full_access(
    init_db, admin_user, async_client: AsyncClient, view_name: str
) -> None:
    response = await request(async_client, view_name)
    assert has_access(response)


# AUTHORIZED USER - Only access to my_salary endpoint
@pytest.mark.parametrize("view_name", ADMIN_ENDPOINTS_VIEWS)
async def test_auth_has_no_access(
    init_db, mock_async_session, async_client: AsyncClient, view_name: str
) -> None:
    headers = get_headers(await get_auth_user_token(async_client))
    response = await request(async_client, view_name, headers=headers)
    assert response.status_code == HTTPStatus.FORBIDDEN


async def test_auth_has_access_salary_records(
    init_db,
    mock_async_session,
    async_client: AsyncClient,
) -> None:
    headers = get_headers(await get_auth_user_token(async_client))
    response = await request(async_client, AUTH_USER_ENDPOINT_VIEW, headers=headers)
    assert has_access(response)
