import uuid

import pytest
from fastapi import HTTPException

from app.repositories import crud
from tests.fixtures.data import ModelTest
from tests.utils import check_exception_info_not_found, compare_with_db

TITLE = "test_title"
DESCR = "test_descr"


@pytest.fixture
async def create_obj(get_test_session):
    return crud.insert_(get_test_session, ModelTest, title=TITLE, description=DESCR)


async def test_crud_insert(get_test_session, create_obj):
    created = await create_obj
    await compare_with_db(get_test_session, created, TITLE, DESCR)


async def test_crud_update(get_test_session, create_obj):
    UPDATE_TITLE = "update_title"
    UPDATE_DESCR = "update_descr"
    created = await create_obj
    await compare_with_db(get_test_session, created, TITLE, DESCR)
    updated = await crud.update_(
        get_test_session,
        ModelTest,
        created.id,
        title=UPDATE_TITLE,
        description=UPDATE_DESCR,
    )
    await compare_with_db(get_test_session, updated, UPDATE_TITLE, UPDATE_DESCR)


async def test_crud_get_or_404_raises_exc(get_test_session):
    with pytest.raises(HTTPException) as exc_info:
        await crud.get_or_404(get_test_session, ModelTest, uuid.uuid4())
    check_exception_info_not_found(exc_info, crud.MSG_OBJECT_NOT_FOUND)


async def test_crud_get_all(get_test_session, create_obj):
    created = await create_obj
    res = await crud.get_all(get_test_session, ModelTest)
    assert isinstance(res, list)
    assert created == res[0]
