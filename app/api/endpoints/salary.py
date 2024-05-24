import uuid

from fastapi import APIRouter

from app.config.app_config import app_conf
from app.config.db_config import async_session
from app.models.models import Salary
from app.repositories import crud
from app.schemas import schemas
from app.user.auth import admin, authorized

from .responses import get_404

router = APIRouter(prefix=app_conf.URL_PREFIX.format("salary"), tags=["Salaries"])


@router.get(
    "/",
    response_model=list[schemas.SalaryOut],
    summary="Возвращает список всех зарплат.",
    description=app_conf.ADMIN_ONLY,
    dependencies=[admin],
)
async def get_all_salaries(session: async_session):
    return await crud.get_all(session, Salary)


@router.patch(
    "/{user_id}",
    response_model=schemas.SalaryOut,
    summary="Редактирование зарплаты сотрудника админом работодателя.",
    description=app_conf.ADMIN_ONLY,
    dependencies=[admin],
    responses=get_404("Employee"),
)
async def update_salary(
    session: async_session, user_id: uuid.UUID, payload: schemas.SalaryPatch
) -> None:
    salary = await crud.get(
        session, Salary, exception=True, fetch_one=True, user_id=user_id
    )
    return await crud.update_(session, Salary, salary.id, **payload.model_dump())


@router.get(
    "/my_salary",
    summary="Просмотр зарплаты сотрудником.",
    description=app_conf.AUTH_ONLY,
    responses=get_404("Salary"),
)
async def get_my_salary(session: async_session, user: authorized):
    return await crud.get(
        session,
        Salary,
        exception=True,
        fetch_one=True,
        user_id=user.id,
        msg="У админов нет записей в БД зарплат.",
    )