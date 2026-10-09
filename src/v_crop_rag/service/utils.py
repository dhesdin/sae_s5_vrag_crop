from pathlib import Path

from v_crop_rag.service.schemas import BoundingBox, DetectedObject


def bbox_to_metadata(bbox: BoundingBox | None) -> dict[str, bool | float]:
    """Convert a bounding box into flat, prefixed metadata fields for ChromaDB.

    Chroma metadata values must be scalars (no nested objects or dicts). When bbox is None,
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


def _join_parts(parts: list[str | None]) -> str:
    """Strip each part, drop the empty/None ones, join what's left with a space."""
    result = []
    for part in parts:
        if part is None:
            continue

        cleaned = part.strip()
        if cleaned:
            result.append(cleaned)

    return " ".join(result)


def object_to_text(obj: DetectedObject) -> str:
    """Build the text embedded for a detected object (label, color, state).

    The position is deliberately excluded: it is relative to the image
    ("centre droit"), not query vocabulary. It is kept in the metadata instead.
    """
    if not isinstance(obj, DetectedObject):
        raise TypeError("obj must be a DetectedObject")

    # Fixed order: the same object always produces the same text
    return _join_parts([obj.label, obj.color, obj.state])


def image_to_metadata(image_path: Path, element_type: str) -> dict[str, str]:
    """Build the metadata for a whole-image entry (main_subject or background).

    Mirrors bbox_to_metadata, but there is no bbox for the image as a whole.
    element_type distinguishes a "main_subject" entry from a "background" one.
    """
    if not isinstance(image_path, Path):
        raise TypeError("image_path must be a Path")

    # wrong type first, then empty value: same two-step check as the adapters
    if not isinstance(element_type, str):
        raise TypeError("element_type must be a string")

    if not element_type.strip():
        raise ValueError("element_type is required")

    return {"image": image_path.name, "type": element_type}
