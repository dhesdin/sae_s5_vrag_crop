from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    USER = "user"
    IA = "ia"


class Response(BaseModel):
    id: int
    role: Role
    content: str
    img_url: str
