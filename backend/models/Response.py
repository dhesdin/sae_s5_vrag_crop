from pydantic import BaseModel


class Response(BaseModel):
    id: int
    content: str
    img_url: str
