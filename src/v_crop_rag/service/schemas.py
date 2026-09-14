from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """Schema representing a bounding box around a detected object.
    Coordinates in absolute pixels. The upper bound (staying within the image limits) cannot be verified here."""

    x: float = Field(..., ge=0, description="X coordinate of the bounding box")
    y: float = Field(..., ge=0, description="Y coordinate of the bounding box")
    width: float = Field(..., gt=0, description="Width of the bounding box")
    height: float = Field(..., gt=0, description="Height of the bounding box")


class DetectedObject(BaseModel):
    """Schema representing an object detected within an image."""

    label: str = Field(..., description="Label of the detected object")
    color: str | None = Field(None, description="Dominant color of the object, if relevant")
    position: str = Field(
        ...,
        description="Relative position in the image, in natural language. Ex: 'top left', 'center', 'bottom right'",
    )
    state: str | None = Field(
        None,
        description="Notable state of the object, if any. Ex: 'open', 'closed', 'damaged'",
    )
    bounding_box: BoundingBox | None = None


class ImageDescription(BaseModel):
    """Schema representing the overall description of an image, including its main subject, background, and detected objects."""

    main_subject: str = Field(..., description="Main subject of the image")
    background: str = Field(..., description="Background and general setting of the image")
    detected_objects: list[DetectedObject] = Field(default_factory=list, description="List of notable detected objects")
