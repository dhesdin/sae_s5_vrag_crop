import pytest

from v_crop_rag.service.parsing import (
    VLMResponseParsingError,
    _extract_json_candidate,
    parse_vlm_response,
)
from v_crop_rag.service.schemas import ImageDescription

_VALID_PAYLOAD = """
{
    "main_subject": "un vélo rouge",
    "background": "une rue pavée",
    "detected_objects": []
}
"""


# Clean, well-formed JSON should parse and validate without any extraction needed.
def test_parse_clean_json():
    result = parse_vlm_response(_VALID_PAYLOAD)
    assert isinstance(result, ImageDescription)
    assert result.main_subject == "un vélo rouge"


# JSON surrounded by free text (VLM adding commentary) should still be extracted and parsed.
def test_parse_json_surrounded_by_free_text():
    raw = f"Voici le résultat :\n{_VALID_PAYLOAD}\nJ'espère que ça aide !"
    result = parse_vlm_response(raw)
    assert result.main_subject == "un vélo rouge"


# JSON wrapped in a markdown code fence (forbidden by the prompt, but VLMs don't always comply).
def test_parse_json_in_markdown_code_fence():
    raw = f"```json\n{_VALID_PAYLOAD}\n```"
    result = parse_vlm_response(raw)
    assert result.main_subject == "un vélo rouge"


# An empty string must raise our custom exception, not crash further downstream.
def test_parse_empty_response_raises():
    with pytest.raises(VLMResponseParsingError) as exc_info:
        parse_vlm_response("")
    assert exc_info.value.reason == "The raw response is empty or None"
    assert exc_info.value.raw_response == ""


# A response made only of whitespace must be treated as empty, same as an empty string.
def test_parse_whitespace_only_response_raises():
    with pytest.raises(VLMResponseParsingError) as exc_info:
        parse_vlm_response("   \n\t  ")
    assert exc_info.value.reason == "The raw response is empty or None"


# Truncated/malformed JSON must raise our exception and keep the original raw response for debugging.
def test_parse_invalid_json_raises():
    raw = '{"main_subject": "vélo", "background": '  # truncated, missing closing brace
    with pytest.raises(VLMResponseParsingError) as exc_info:
        parse_vlm_response(raw)
    assert exc_info.value.raw_response == raw
    assert "JSON is invalid" in exc_info.value.reason


# Valid JSON missing a required schema field must fail at the Pydantic validation step.
def test_parse_valid_json_missing_required_field_raises():
    raw = '{"main_subject": "un vélo"}'  # "background" missing
    with pytest.raises(VLMResponseParsingError) as exc_info:
        parse_vlm_response(raw)
    assert "Validation error" in exc_info.value.reason


# Already-clean JSON should be returned unchanged.
def test_extract_json_candidate_with_clean_json():
    assert _extract_json_candidate('{"a": 1}') == '{"a": 1}'


# A markdown code fence around the JSON should be stripped away.
def test_extract_json_candidate_with_markdown_fence():
    raw = '```json\n{"a": 1}\n```'
    assert _extract_json_candidate(raw) == '{"a": 1}'


# Free text before/after the JSON object should be stripped away.
def test_extract_json_candidate_with_surrounding_text():
    raw = 'Voici : {"a": 1} merci'
    assert _extract_json_candidate(raw) == '{"a": 1}'


# With no braces at all, the function should fall back to returning the stripped input as-is.
def test_extract_json_candidate_with_no_braces_returns_stripped_input():
    raw = "  pas de json ici  "
    assert _extract_json_candidate(raw) == "pas de json ici"
