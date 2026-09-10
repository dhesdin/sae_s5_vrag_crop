import json

from v_crop_rag.service.prompts import (
    _EXPECTED_JSON_SHAPE,
    _JSON_EXAMPLE,
    build_extraction_prompt,
)


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
