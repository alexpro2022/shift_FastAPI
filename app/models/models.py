from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Example(Base):
    title: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(2000), default="No description")

    def __repr__(self) -> str:
        return (
            f"{super().__repr__()}"
            f"\ntitle: {self.title}"
            f"\ndescription: {self.description}"
        )
