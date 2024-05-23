import uuid

from fastapi import APIRouter

from app.config.app_config import app_conf
from app.config.db_config import async_session
from app.models.models import Salary
from app.repositories import crud
from app.schemas import schemas

from .responses import get_400, get_404

router = APIRouter(prefix=app_conf.URL_PREFIX.format("salary"), tags=["Salaries"])


@router.get(
    "/",
    # dependencies=[Depends(current_superuser)],
    # response_model=list[schemas.PostResponse],
    # response_model_exclude_none=True,
    summary="Возвращает список всех зарплат.",
    description=app_conf.ADMIN_ONLY,
)
async def get_all_salaries(session: async_session):
    return await crud.get_all(session, Salary)


@router.patch(
    "/{user_id}",
    # dependencies=[Depends(current_superuser)],
    # response_model=list[schemas.PostResponse],
    # response_model_exclude_none=True,
    summary="Редактирование зарплаты сотрудника.",
    description=app_conf.ADMIN_ONLY,
    responses={**get_400("Employee"), **get_404("Employee")},
)
async def patch_salary(
    session: async_session, user_id: uuid.UUID, payload: schemas.SalaryPatch
) -> None:
    salary = await crud.get(session, Salary, exception=True, user_id=user_id)
    salary_id = salary[0].id
    return await crud.update_(session, Salary, salary_id, **payload.model_dump())
