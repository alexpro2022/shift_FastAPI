import uuid
from typing import Any

from sqlalchemy import UUID, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    """Base DB model."""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    def __repr__(self) -> str:
        return f"\nid: {self.id}"

    def _asdict(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
