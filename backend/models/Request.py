from enum import Enum

from pydantic import BaseModel

class Response(BaseModel):
    id: int
    content: str
