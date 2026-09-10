import pytest
from pydantic import ValidationError

from src.v_crop_rag.service.schemas import ImageDescription, DetectedObject


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


def test_detected_object_missing_label_raises():
    with pytest.raises(ValidationError):
        DetectedObject(color="rouge", position="quelque part") # w/o label


def test_image_description_empty_objects_allowed():
    desc = ImageDescription(
        main_subject="un mur blanc",
        background="texture unie",
        detected_objects=[],
    )
    assert desc.detected_objects == []
