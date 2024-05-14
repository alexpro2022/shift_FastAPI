from fastapi import APIRouter

from app.core.config import settings
from app.core.dependencies import async_session
from app.models.models import Vacancy
from app.schemas import schemas

from .responses import get_400, get_404

SUM_ALL_ITEMS = "ALL_ITEMS"

router = APIRouter(prefix=f"{settings.URL_PREFIX}items", tags=["Items"])


@router.get(
    "/",
    response_model=list[schemas.VacancyOut],
    responses={**get_400("Item"), **get_404("Item")},
    summary=SUM_ALL_ITEMS,
    description=(f"{settings.ALL_USERS} {SUM_ALL_ITEMS}"),
)
async def get_all_vacancies(session: async_session) -> list:
    from sqlalchemy import select

    stmt = select(Vacancy)
    return await session.scalars(stmt)
