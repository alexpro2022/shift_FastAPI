import uuid

from app.config.app_config import app_conf
from app.services.admin import notify_admin


async def test_notify_admin():
    USER_ID = uuid.uuid4()
    actual = await notify_admin(USER_ID)
    expected = app_conf.URL_PREFIX.format(f"salary/{USER_ID}")
    assert actual == expected
