from fastapi import APIRouter

from app.api.endpoints import example
from app.user import routers as u

main_router = APIRouter()


for router in (
    example.router,
    u.router,
    # add routers
):
    main_router.include_router(router)

# to remove above code into main.py
