from fastapi_users import schemas

from app.types import UUID_ID


class UserRead(schemas.BaseUser[UUID_ID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
