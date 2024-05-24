from app.config.app_config import app_conf
from app.types import UUID_ID


async def notify_admin(user_id: UUID_ID) -> str:
    new_salary_url = app_conf.URL_PREFIX.format(f"salary/{user_id}")
    # TODO: notify admin by email
    return new_salary_url
