from http import HTTPStatus
from typing import Any, Callable, TypeAlias

from deepdiff import DeepDiff
from fastapi import APIRouter, FastAPI
from httpx import AsyncClient
from httpx._types import HeaderTypes

from app.main import app
from app.types import UUID_DEFAULT, UUID_ID
from tests.fixtures import data as d

Json: TypeAlias = dict[str, Any]
callable: TypeAlias = Callable[[Json], str]


def reverse(router: APIRouter | FastAPI, view_name: str) -> str:
    if isinstance(router, FastAPI):
        router = vars(router)["router"]
    for route in vars(router)["routes"]:
        if route.name == view_name:
            return route.path
    raise NotImplementedError(
        f"Path operation function `{view_name}` hasn't been implemented yet."
    )


def check_response(
    response_json: Json | list[Json], expected_result: Json | list[Json]
) -> str:
    diff = DeepDiff(response_json, expected_result, ignore_order=True)
    assert not diff, diff
    return "DONE"


async def request(
    async_client: AsyncClient,
    view_name: str,
    user_id: UUID_ID = UUID_DEFAULT(),
    headers: HeaderTypes | None = None,
):
    if view_name == "update_salary":
        url = reverse(app, view_name).format(user_id=user_id)
        response = await async_client.patch(
            url, json=d.SALARY_UPDATE_DATA, headers=headers
        )
    else:
        url = reverse(app, view_name)
        response = await async_client.get(url, headers=headers)
    return response


def has_access(response):
    return response.status_code == HTTPStatus.OK or response.status_code not in (
        HTTPStatus.FORBIDDEN,
        HTTPStatus.UNAUTHORIZED,
    )
