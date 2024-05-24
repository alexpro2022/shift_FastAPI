from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

USER_REGISTER_DATA = {
    "email": "user@example.com",
    "password": "userpw",
    "is_active": True,
    "is_superuser": False,
    "is_verified": False,
}

SALARY_UPDATE_DATA = {"value": 10.01, "inc_date": "2024-05-23"}

ALL_USERS: list = []
ALL_SALARIES: list = []

TITLE = "test_title"
DESCR = "test_descr"


class ModelTest(Base):
    title: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]

    def __repr__(self):
        return (
            f"{super().__repr__()}"
            f"\ntitle: {self.title}"
            f"\ndescription: {self.description}"
        )
