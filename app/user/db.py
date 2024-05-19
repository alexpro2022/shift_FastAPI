from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import select

from app.config.db_config import async_session
from app.models.models import User


class CustomUserDatabase(SQLAlchemyUserDatabase):
    async def get_all(self):
        res = await self.session.scalars(select(self.user_table))
        return res.all()


async def get_user_db(session: async_session) -> AsyncGenerator[Any, Any]:
    yield CustomUserDatabase(session, User)


user_db = Annotated[CustomUserDatabase, Depends(get_user_db)]
