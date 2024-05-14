from typing import Any, Callable, TypeAlias

from deepdiff import DeepDiff
from fastapi import APIRouter

Json: TypeAlias = dict[str, Any]
callable: TypeAlias = Callable[[Json], str]


def reverse(router: APIRouter, view_name: str) -> str:
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
