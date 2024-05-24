import uuid
from typing import Any, AsyncGenerator, TypeAlias

from sqlalchemy.ext.asyncio import AsyncSession

UUID_ID = uuid.UUID
UUID_DEFAULT = uuid.uuid4

Response_4xx: TypeAlias = dict[int, dict[str, Any]]
AsyncGenAsyncSession: TypeAlias = AsyncGenerator[AsyncSession, None]
