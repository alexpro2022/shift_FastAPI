import uuid

from app.config.app_config import app_conf


async def notify_admin(user_id: uuid.UUID) -> str:
    new_salary_url = app_conf.URL_PREFIX.format(f"salary/{user_id}")
    # TODO: notify admin by email
    return new_salary_url
