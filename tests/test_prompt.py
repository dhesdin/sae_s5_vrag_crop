import json

from v_crop_rag.service.prompts import (
    _EXPECTED_JSON_SHAPE,
    _JSON_EXAMPLE,
    build_extraction_prompt,
)
from v_crop_rag.service.schemas import BoundingBox, DetectedObject, ImageDescription


def test_expected_json_shape_is_valid_json():
    # VErify that the expected JSON shape is valid JSON
    parsed = json.loads(_EXPECTED_JSON_SHAPE)
    assert "main_subject" in parsed
    assert "detected_objects" in parsed


def test_json_example_is_valid_json():
    parsed = json.loads(_JSON_EXAMPLE)
    assert "main_subject" in parsed
    assert isinstance(parsed["detected_objects"], list)
    assert len(parsed["detected_objects"]) > 0


def test_json_example_matches_schema_fields():
    # Verify that the concrete example uses the same keys as the schema
    example = json.loads(_JSON_EXAMPLE)
    first_object = example["detected_objects"][0]
    expected_keys = {"label", "color", "position", "state", "bounding_box"}
    assert expected_keys.issubset(first_object.keys())  # check if the whole elements of expected are in the parameters


def test_build_extraction_prompt_contains_expected_sections():
    prompt = build_extraction_prompt()
    assert "main_subject" in prompt
    assert "detected_objects" in prompt
    assert prompt.strip() != ""


def test_build_extraction_prompt_forbids_extra_text():
    # Verify that the strict anti-noise instruction is present
    prompt = build_extraction_prompt()
    assert "```" in prompt  # explicit mention of the prohibition of the Markdown block


def test_build_extraction_prompt_is_deterministic():
    # Two calls should produce exactly the same text (no hidden randomness)
    assert build_extraction_prompt() == build_extraction_prompt()


#  prompt/schema : the hand-written _JSON_EXAMPLE must always match 
#  the Pydantic schema exactly, recursively 


def test_json_example_matches_schema_recursively():
    example = json.loads(_JSON_EXAMPLE)

    assert set(example.keys()) == set(ImageDescription.model_fields.keys())

    detected_objects = example["detected_objects"]
    assert len(detected_objects) > 0
    checked_bounding_box = False
    for obj in detected_objects:
        assert set(obj.keys()) == set(DetectedObject.model_fields.keys())

        bounding_box = obj["bounding_box"]
        if bounding_box is not None:
            assert set(bounding_box.keys()) == set(BoundingBox.model_fields.keys())
            checked_bounding_box = True

    # Make sure at least one example object actually has a bounding_box
    assert checked_bounding_box
