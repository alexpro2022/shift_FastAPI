from pydantic import BaseModel

from app.types import Response_4xx


def get_400(name: str) -> Response_4xx:
    class Message(BaseModel):
        detail: str = f"{name} already exists"

    return {400: {"model": Message, "description": "The item already exists"}}


def get_404(name: str) -> Response_4xx:
    class Message(BaseModel):
        detail: str = f"{name} not found"

    return {404: {"model": Message, "description": "The item was not found"}}
