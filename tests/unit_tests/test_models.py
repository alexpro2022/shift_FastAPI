from uuid import uuid4

import pytest

from app.models import Dish, Menu, Submenu
from tests.fixtures import data as d

# Test MULTIPLE model
COMMON_FIELDS = ("id", "title", "description")

parametrize = pytest.mark.parametrize(
    "model, data, attrs",
    (
        (Dish, d.DISH_POST_PAYLOAD, (*COMMON_FIELDS, "price")),
        (Menu, d.MENU_POST_PAYLOAD, (*COMMON_FIELDS,)),
        (Submenu, d.SUBMENU_POST_PAYLOAD, (*COMMON_FIELDS,)),
    ),
)


@parametrize
def test_model_attr(model, data: dict[str, str], attrs: str) -> None:
    for attr_name in attrs:
        assert hasattr(model, attr_name)


@parametrize
def test_model_repr(model, data: dict[str, str], attrs: str) -> None:
    representation = repr(model(**data))
    for attr_name in attrs:
        assert representation.find(attr_name) != -1


@parametrize
def test_asdict(model, data: dict[str, str], attrs: str) -> None:
    obj = model(**data)._asdict()
    assert isinstance(obj, dict)
    for key in data:
        assert obj[key] == data[key]


# Test SINGLE model
task_model_fields = pytest.mark.parametrize("field_name", ("id", "name", "description"))


@task_model_fields
def test_task_model_attr(field_name: str) -> None:
    assert hasattr(Task, field_name)


@task_model_fields
def test_task_model_repr(field_name: str) -> None:
    representation = repr(Task())
    assert representation.find(field_name) != -1


def test_task_model_asdict() -> None:
    data = {
        "id": uuid4(),
        "name": "test_as_dict_name",
        "description": "test_as_dict_description",
    }
    obj = Task(**data)
    assert isinstance(obj, Task)
    assert isinstance(obj._asdict(), dict)
    assert obj._asdict() == data
