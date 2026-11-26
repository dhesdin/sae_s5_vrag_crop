from pydantic import BaseModel, Field


class Request(BaseModel):
    """Requête de recherche envoyée par le front."""

    query: str
    k: int = Field(default=5, ge=1)
