import uuid
from datetime import date
from decimal import Decimal

from config.app_config import app_conf
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    salary: Mapped["Salary"] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return (
            f"{super().__repr__()}"
            f"\nsalary: {self.salary.value if self.salary else None}"
        )


class Salary(Base):
    value: Mapped[Decimal] = mapped_column(
        Numeric(precision=app_conf.salary_precision, scale=app_conf.salary_scale)
    )
    inc_date: Mapped[date]
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="salary")

    __table_args__ = (UniqueConstraint("user_id"),)

    def __repr__(self) -> str:
        return (
            f"{super().__repr__()}"
            f"\nvalue: {self.value}"
            f"\ninc_date: {self.inc_date}"
            f"\nuser_id: {self.user_id}"
            f"\nuser: {self.user.email if self.user else None}"
        )
