from pydantic import BaseModel, Field

from v_crop_rag.ollama_client import vlm


class BoundingBox(BaseModel):
    x: float = Field(..., description="X coordinate of the bounding box")
    y: float = Field(..., description="Y coordinate of the bounding box")
    width: float = Field(..., description="Width of the bounding box")
    height: float = Field(..., description="Height of the bounding box")


class DetectedObject(BaseModel):
    label: str = Field(..., description="Label of the detected object")
    color: str | None = Field(
        None, description="Dominant color of the object, if relevant"
    )
    position: str = Field(
        ..., description="Relative position in the image, in natural language. Ex: 'top left', 'center', 'bottom right'"
    )
    state: str | None = Field(None, description="Notable state of the object, if any. Ex: 'open', 'closed', 'damaged'")
    bounding_box: BoundingBox | None = None


class ImageDescription(BaseModel):
    main_subject: str = Field(..., description="Main subject of the image")
    background: str = Field(
        ..., description="Background and general setting of the image"
    )
    detected_objects: list[DetectedObject] = Field(
        default_factory=list, description="List of notable detected objects"
    )
