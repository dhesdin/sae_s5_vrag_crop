import pytest
from chromadb.api.types import validate_metadata

from v_crop_rag.service.schemas import BoundingBox
from v_crop_rag.service.utils import bbox_to_metadata


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
