"""
The module is kept as code example.

"""

from http import HTTPStatus

import pytest
from httpx import AsyncClient

from app.api.routers import main_router
from tests.fixtures import data as d

from ..fixtures.load_csv_data import convert_to_int
from .utils import Json, check_response, reverse


@pytest.mark.parametrize(
    "view_name, expected_result",
    (
        ("get_all_cities", d.CITIES_EXPECTED),
        ("get_all_vacancies", d.VACANCY_NAMES_EXPECTED),
        ("get_all_categories", d.CATEGORIES_EXPECTED),
    ),
)
async def test_get_all(
    load_csv_data, async_client: AsyncClient, view_name: str, expected_result: Json
) -> None:
    url = reverse(main_router, view_name)
    response = await async_client.get(url)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json
    assert check_response(response_json, expected_result) == "DONE"


async def test_get_specialization(load_csv_data, async_client: AsyncClient) -> None:
    url = reverse(main_router, "get_spec").format(vacancy_name_id=2)
    response = await async_client.get(url)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json
    assert check_response(response_json, d.SPECIALIZATION_EXPECTED) == "DONE"


async def test_get_data(load_csv_data, async_client: AsyncClient) -> None:
    url = f"{reverse(main_router, 'get_data')}?vacancy_name_id=1&city_id=1"
    response = await async_client.get(url)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json
    assert check_response(response_json, d.DATA_EXPECTED) == "DONE"


async def test_post_vacancy(init_db, async_client: AsyncClient) -> None:
    url = reverse(main_router, "create_vacancy")
    response = await async_client.post(url, json=d.VACANCY_POST_PAYLOAD)
    assert response.status_code == HTTPStatus.CREATED
    response_json = response.json()
    assert response_json
    convert_to_int([response_json])
    response_json["show_info"] = bool(response_json["show_info"])
    assert (
        check_response(response_json, {**{"id": 1}, **d.VACANCY_POST_PAYLOAD}) == "DONE"
    )
