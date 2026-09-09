from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x_min: int  # A MODIFIER SELON CONFIG VALENTIN (ici coord pixel mais possible aussi de coordonnées normalisées)
    y_min: int
    x_max: int
    y_max: int


class VisualElement(BaseModel):
    label: str
    description: str
    attributes: dict[str, str] = Field(default_factory=dict)
    bbox: BoundingBox | None = None
