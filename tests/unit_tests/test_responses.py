from typing import Callable

from app.api.endpoints.responses import get_400, get_404

OBJ_NAME = "name"


def _test_response(
    method: Callable,
    key: int,
    message: str,
    description: str,
) -> None:
    response = method(OBJ_NAME)
    assert isinstance(response, dict)
    body = response[key]
    assert isinstance(body, dict)
    assert vars(body["model"])["model_fields"]["detail"].default == message
    assert body["description"] == description


def test_400() -> None:
    _test_response(
        get_400, 400, f"{OBJ_NAME} already exists", "The item already exists"
    )


def test_404() -> None:
    _test_response(get_404, 404, f"{OBJ_NAME} not found", "The item was not found")
