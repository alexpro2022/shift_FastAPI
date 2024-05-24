from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.config.app_config import app_conf
from app.types import UUID_ID

DECIMAL_VALUE = 10.01


class SalaryPatch(BaseModel):
    value: Decimal = Field(
        None,
        gt=0,
        examples=[DECIMAL_VALUE],
        decimal_places=app_conf.salary_scale,
        max_digits=app_conf.salary_precision,
    )
    inc_date: date | None


class SalaryOut(SalaryPatch):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
    id: UUID_ID
    user_id: UUID_ID
