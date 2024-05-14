from typing import Annotated, Any, AsyncGenerator

from config.db_config import async_session
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from models.models import User


async def get_user_db(session: async_session) -> AsyncGenerator[Any, Any]:
    yield SQLAlchemyUserDatabase(session, User)


user_db = Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]
