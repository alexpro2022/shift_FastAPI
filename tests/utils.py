import uuid

from fastapi import status

# from deepdiff import DeepDiff
from app.config.app_config import app_conf
from app.repositories import crud
from app.user.db import User
from tests.fixtures.data import ModelTest

USER_CREDS = (app_conf.admin_email, app_conf.admin_password)


def check_user(user: User, is_superuser: bool = False) -> None:
    assert user.email == app_conf.admin_email
    assert user.hashed_password
    assert user.is_superuser == is_superuser


def compare(left, right) -> None:
    def clean(item) -> dict:
        wanted = "_sa_instance_state"
        d = vars(item).copy()
        if wanted in d:
            d.pop(wanted)
        return d

    assert clean(left) == clean(right)
    # diff = DeepDiff(clean(left), clean(right), ignore_order=True)
    # assert not diff, diff


def compare_lists(left: list, right: list) -> None:
    assert left and isinstance(left, list)
    assert right and isinstance(right, list)
    assert len(left) == len(right)
    for l_item, r_item in zip(left, right):
        compare(l_item, r_item)


def check_exception_info(
    exc_info, expected_msg: str, expected_error_code: int | None = None
) -> None:
    assert expected_msg in exc_info.value.args
    # assert expected_msg == str(exc_info)
    if expected_error_code is not None:
        assert expected_error_code in exc_info.value.args


def check_exception_info_not_found(exc_info, msg_not_found: str) -> None:
    check_exception_info(exc_info, msg_not_found, status.HTTP_404_NOT_FOUND)


async def compare_with_db(
    session, obj: ModelTest, expected_title, expected_description
):
    retrieved = await crud.get_or_404(session, ModelTest, obj.id)
    assert isinstance(retrieved, ModelTest)
    assert isinstance(retrieved.id, uuid.UUID)
    assert retrieved.title == expected_title
    assert retrieved.description == expected_description
    assert obj == retrieved


async def db_empty(session, model):
    return await crud.get_all(session, model) == []
