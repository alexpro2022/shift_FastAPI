from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from app.api.routers import main_router
from app.config.app_config import app_conf
from app.config.db_config import engine
from app.models.base import Base
from app.user.admin import create_admin


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    # The below context manager is for dev quick start without alembic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await create_admin()
    yield


app = FastAPI(
    title=app_conf.app_title, description=app_conf.app_description, lifespan=lifespan
)

app.include_router(main_router)
