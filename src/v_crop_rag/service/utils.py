from v_crop_rag.service.schemas import BoundingBox, DetectedObject


def bbox_to_metadata(bbox: BoundingBox | None) -> dict[str, bool | float]:
    """Convert a bounding box into flat, prefixed metadata fields for ChromaDB.

    Chroma metadata values must be scalars (no nested objects or dicts), When bbox is None,
    only has_bbox=False is returned,
    so objects without a bbox can be filtered with where={"has_bbox": False}.

    Args:
        bbox (BoundingBox | None): The bounding box to convert, or None if absent.

    Returns:
        dict[str, bool | float]: has_bbox, plus bbox_x, bbox_y, bbox_width and bbox_height when bbox is set.
    """

    if bbox is None:
        return {"has_bbox": False}

    if not isinstance(bbox, BoundingBox):
        raise TypeError("bbox must be a BoundingBox or None")

    return {
        "has_bbox": True,
        "bbox_x": bbox.x,
        "bbox_y": bbox.y,
        "bbox_width": bbox.width,
        "bbox_height": bbox.height,
    }


def object_to_text(obj: DetectedObject) -> str:
    """Build the text embedded for a detected object (label, color, state, position).
    """
    if not isinstance(obj, DetectedObject):
        raise TypeError("obj must be a DetectedObject")

    parts = [obj.label, obj.color, obj.state, obj.position]
    return " ".join(part.strip() for part in parts if part and part.strip())    