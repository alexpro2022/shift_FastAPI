from fastapi import APIRouter

from app.config.app_config import app_conf
from app.config.db_config import async_session
from app.models.models import Salary
from app.repositories import crud

from .auth import auth_backend, fastapi_users
from .db import user_db
from .schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/users",
    tags=["users"],
    # dependencies=[Depends(current_superuser)],
    # response_model=list[schemas.PostResponse],
    # response_model_exclude_none=True,
    summary="Возвращает список всех пользователей.",
    description=app_conf.ADMIN_ONLY,
)
async def get_all_users(user_db: user_db):
    return await user_db.get_all()


@router.get(
    "/salaries",
    tags=["salaries"],
    # dependencies=[Depends(current_superuser)],
    # response_model=list[schemas.PostResponse],
    # response_model_exclude_none=True,
    summary="Возвращает список всех зарплат.",
    description=app_conf.ADMIN_ONLY,
)
async def get_all_salaries(session: async_session):
    return await crud.get_all(session, Salary)
