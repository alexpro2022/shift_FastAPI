from fastapi import APIRouter, HTTPException, status

from app.config.app_config import app_conf

from .auth import auth_backend, fastapi_users
from .db import user_db
from .schemas import UserCreate, UserRead, UserUpdate

TAG_AUTH = "Auth"
TAG_USERS = "Users"

router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=app_conf.URL_PREFIX.format("auth/jwt"),
    tags=[TAG_AUTH],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=app_conf.URL_PREFIX.format("auth"),
    tags=[TAG_AUTH],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=app_conf.URL_PREFIX.format("user"),
    tags=[TAG_USERS],
)


@router.get(
    app_conf.URL_PREFIX.format("user"),
    tags=[TAG_USERS],
    # dependencies=[Depends(current_superuser)],
    # response_model=list[schemas.PostResponse],
    # response_model_exclude_none=True,
    summary="Возвращает список всех пользователей.",
    description=app_conf.ADMIN_ONLY,
)
async def get_all_users(user_db: user_db):
    return await user_db.get_all()


@router.delete(
    app_conf.URL_PREFIX.format("user/{id}"),
    tags=[TAG_USERS],
    deprecated=True,
)
def delete_user(id: str):
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail="Удаление пользователей запрещено!",
    )
