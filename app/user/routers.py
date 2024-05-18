from fastapi import APIRouter

from .auth import auth_backend, fastapi_users, user_manager
from .schemas import UserCreate, UserRead, UserUpdate

# from sqlalchemy import select


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


@router.get("/users")
# for admins only
async def get_all_users(user_manager: user_manager):
    ...
    # session: async_session):
    # stmt = select(User)
    # return await user_manager.get_all_users()
