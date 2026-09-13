import pytest
from pydantic import ValidationError

from src.v_crop_rag.service.schemas import BoundingBox, DetectedObject, ImageDescription


def test_image_description_valid():
    desc = ImageDescription(
        main_subject="une terrasse de café",
        background="place pavée européenne, journée ensoleillée",
        detected_objects=[
            DetectedObject(
                label="vélo",
                color="rouge",
                position="contre un réverbère, arrière-plan gauche",
            )
        ],
    )
    assert desc.main_subject == "une terrasse de café"
    assert len(desc.detected_objects) == 1
    assert desc.detected_objects[0].label == "vélo"


def test_image_description_empty_objects_allowed():
    desc = ImageDescription(
        main_subject="un mur blanc",
        background="texture unie",
        detected_objects=[],
    )
    assert desc.detected_objects == []


def test_image_description_multiple_objects():
    desc = ImageDescription(
        main_subject="une rue",
        background="ville",
        detected_objects=[
            DetectedObject(label="vélo", position="centre"),
            DetectedObject(label="poubelle", position="gauche"),
        ],
    )
    assert len(desc.detected_objects) == 2
    assert desc.detected_objects[1].label == "poubelle"


# --- ImageDescription : mandatory field missing ---


def test_image_description_missing_main_subject_raises():
    with pytest.raises(ValidationError):
        ImageDescription(background="texture unie", detected_objects=[])


def test_image_description_missing_background_raises():
    with pytest.raises(ValidationError):
        ImageDescription(main_subject="un mur", detected_objects=[])


# --- DetectedObject : mandatory field missing ---


def test_detected_object_missing_label_raises():
    with pytest.raises(ValidationError):
        DetectedObject(color="rouge", position="quelque part")  # w/o label


def test_detected_object_missing_position_raises():
    with pytest.raises(ValidationError):
        DetectedObject(label="vélo", color="rouge")  # w/o position


# --- DetectedObject : truly optional fields ---


def test_detected_object_minimal_fields_only():
    obj = DetectedObject(label="ombre", position="au sol")
    assert obj.color is None
    assert obj.state is None
    assert obj.bounding_box is None


# --- BoundingBox : valid and invalid cases ---


def test_bounding_box_valid():
    bbox = BoundingBox(x=10, y=20, width=100, height=50)
    assert bbox.width == 100


def test_bounding_box_missing_field_raises():
    with pytest.raises(ValidationError):
        BoundingBox(x=10, y=20, width=100)  # missing height


def test_detected_object_with_bounding_box():
    obj = DetectedObject(
        label="vélo",
        position="centre",
        bounding_box=BoundingBox(x=120, y=80, width=300, height=220),
    )
    assert obj.bounding_box.x == 120


# --- wrong data types ---


def test_bounding_box_wrong_type_raises():
    with pytest.raises(ValidationError):
        BoundingBox(x="dix", y=20, width=100, height=50)  # x should be a number
