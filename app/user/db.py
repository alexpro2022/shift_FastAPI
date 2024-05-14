from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase

from app.models.base import Base
from config.db_config import async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


async def get_user_db(session: async_session) -> AsyncGenerator[Any, Any]:
    yield SQLAlchemyUserDatabase(session, User)


user_db = Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]
