from fastapi import APIRouter

from app.config.app_config import app_conf

SUM_ALL_ITEMS = "ALL_ITEMS"

router = APIRouter(prefix=f"{app_conf.URL_PREFIX}items", tags=["Items"])


"""
@router.get(
    "/",
    response_model=list[schemas.VacancyOut],
    responses={**get_400("Item"), **get_404("Item")},
    summary=SUM_ALL_ITEMS,
    description=(f"{app_conf.ALL_USERS} {SUM_ALL_ITEMS}"),
)
async def get_all_vacancies(session: async_session) -> list:
    from sqlalchemy import select

    stmt = select(Vacancy)
    return await session.scalars(stmt)
"""
