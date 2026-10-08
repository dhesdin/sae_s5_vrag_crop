import pytest
from chromadb.api.types import validate_metadata

from v_crop_rag.service.schemas import BoundingBox, DetectedObject
from v_crop_rag.service.utils import bbox_to_metadata, object_to_text


# Ensure that bbox items are return with prefixed
def test_bbox_to_metadata_returns_prefixed_fields():
    bbox = BoundingBox(x=400, y=100, width=150, height=400)

    assert bbox_to_metadata(bbox) == {
        "has_bbox": True,
        "bbox_x": 400.0,
        "bbox_y": 100.0,
        "bbox_width": 150.0,
        "bbox_height": 400.0,
    }


# Ensure that None Bbox return false
def test_bbox_to_metadata_returns_has_bbox_false():
    assert bbox_to_metadata(None) == {"has_bbox": False}


# Ensure that every metadata value is a scalar (no nested dict, object, list or None)
def test_bbox_to_metadata_is_flat():
    bbox = BoundingBox(x=400, y=100, width=150, height=400)

    metadata = {"label": "parasol", **bbox_to_metadata(bbox)}

    assert all(isinstance(value, str | int | float | bool) for value in metadata.values())


# Ensure that a bbox at the origin (x=0, y=0) is not mistaken for a missing bbox
def test_bbox_to_metadata_keeps_zero_coordinates():
    bbox = BoundingBox(x=0, y=0, width=1, height=1)

    metadata = bbox_to_metadata(bbox)

    assert metadata["has_bbox"] is True
    assert metadata["bbox_x"] == 0.0
    assert metadata["bbox_y"] == 0.0


# param tests
@pytest.mark.parametrize(
    "invalid_bbox",  # param name
    [  # values list
        {"x": 1, "y": 2, "width": 3, "height": 4},
        [1, 2, 3, 4],
        "bbox",
        42,
    ],
)
def test_bbox_to_metadata_rejects_non_bbox(invalid_bbox):
    with pytest.raises(TypeError):
        bbox_to_metadata(invalid_bbox)


@pytest.mark.parametrize("bbox", [BoundingBox(x=0, y=0, width=1, height=1), None])
# data accepted by chromas
def test_bbox_to_metadata_is_accepted_by_chroma(bbox):
    metadata = {"label": "parasol", **bbox_to_metadata(bbox)}

    # method directly came from chromadb lib
    validate_metadata(metadata)


# Ensure that fields are joined in a fixed order: label, color, state
def test_object_to_text_joins_fields_in_order():
    obj = DetectedObject(label="vélo", color="rouge", state="garé", position="centre")

    assert object_to_text(obj) == "vélo rouge garé"


# Ensure that optional fields set to None are skipped
def test_object_to_text_skips_none_fields():
    obj = DetectedObject(label="vélo", color=None, state=None, position="centre")

    assert object_to_text(obj) == "vélo"


# Ensure that surrounding spaces are removed and whitespace-only fields are skipped
def test_object_to_text_strips_and_skips_blank_fields():
    obj = DetectedObject(label="  vélo  ", color="   ", state="", position="centre")

    assert object_to_text(obj) == "vélo"


# Ensure that a blank label gives an empty text, even if position is filled
def test_object_to_text_blank_label_returns_empty_string():
    obj = DetectedObject(label=" ", color=None, state=None, position="centre")

    assert object_to_text(obj) == ""


# Ensure that position is not part of the embedded text
def test_object_to_text_ignores_position():
    a = DetectedObject(label="vélo", color="rouge", state="garé", position="centre droit")
    b = DetectedObject(label="vélo", color="rouge", state="garé", position="au fond")

    assert object_to_text(a) == object_to_text(b) == "vélo rouge garé"


# Ensure that the bounding box is not part of the embedded text
def test_object_to_text_ignores_bounding_box():
    bbox = BoundingBox(x=1, y=2, width=3, height=4)
    with_bbox = DetectedObject(label="vélo", position="centre", bounding_box=bbox)
    without_bbox = DetectedObject(label="vélo", position="centre")

    assert object_to_text(with_bbox) == object_to_text(without_bbox) == "vélo"


@pytest.mark.parametrize(
    "invalid_obj",
    [
        {"label": "vélo", "position": "centre"},
        "vélo",
        None,
        BoundingBox(x=0, y=0, width=1, height=1),
    ],
)
def test_object_to_text_rejects_non_detected_object(invalid_obj):
    with pytest.raises(TypeError):
        object_to_text(invalid_obj)
