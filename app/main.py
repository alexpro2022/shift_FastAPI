from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user.admin import create_admin

# from app.admin import admin
from app.api.routers import main_router
from app.models.base import Base
from config.app_config import app_conf
from config.db_config import engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    # The below context manager is for dev quick start without alembic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield await create_admin()


app = FastAPI(
    title=app_conf.app_title, description=app_conf.app_description, lifespan=lifespan
)

app.include_router(main_router)
# admin.mount_to(app)

origins = [
    "http://185.221.162.231",
    "http://185.221.162.231:81",
    "http://localhost",
    "http://localhost:81",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
