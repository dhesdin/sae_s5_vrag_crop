import json

from pydantic import ValidationError

from v_crop_rag.service.schemas import ImageDescription


class VLMResponseParsingError(Exception):
    """Raised when a VLM raw response cannot be turned into a valid ImageDescription."""

    def __init__(self, raw_response: str, reason: str) -> None:
        self.raw_response = raw_response
        self.reason = reason
        super().__init__(f"{reason} : {raw_response}")  # Construct the except msg from the reason and raw response


def parse_vlm_response(raw: str) -> ImageDescription:

    # None or empty
    if not raw or not raw.strip():
        raise VLMResponseParsingError(raw, "The raw response is empty or None")
    try:
        raw_json_data = _extract_json_candidate(raw=raw)
        data = json.loads(raw_json_data)
    # Invalid JSON
    except json.JSONDecodeError as e:
        raise VLMResponseParsingError(raw, f"JSON is invalid : {e} please check the format") from e
    try:
        return ImageDescription.model_validate(
            data
        )  # not **data because we could have potentially lists, model_validate can receive any type of input
    except ValidationError as e:
        raise VLMResponseParsingError(raw, f"Validation error: {e}") from e


def _extract_json_candidate(raw: str) -> str:
    stripped = raw.strip()
    first_brace = stripped.find("{")
    last_brace = stripped.rfind("}")
    if first_brace == -1 or last_brace == -1 or first_brace > last_brace:
        return stripped  # raw response
    return stripped[first_brace : last_brace + 1]  # characters from the first to the last brace
