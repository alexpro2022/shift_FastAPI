from api.endpoints import example
from fastapi import APIRouter
from user import routers as u

main_router = APIRouter()


for router in (
    example.router,
    u.router,
    # add routers
):
    main_router.include_router(router)
