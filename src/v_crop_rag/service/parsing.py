import json

from pydantic import ValidationError

from v_crop_rag.service.schemas import ImageDescription


class VLMResponseParsingError(Exception):
    """Raised when a VLM raw response cannot be turned into a valid ImageDescription."""

    def __init__(self, raw_response: str, reason: str) -> None:
        self.raw_response = raw_response
        self.reason = reason
        super().__init__(
            f"{reason} : {raw_response}"
        )  # Construct the except msg from the reason and raw response


def parse_vlm_response(raw: str) -> ImageDescription:

    if not raw or not raw.strip():
        raise VLMResponseParsingError(raw, "The raw response is empty or None")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise VLMResponseParsingError(
            raw, f"JSON is invalid : {e} please check the format"
        ) from e
    try:
        return ImageDescription.model_validate(
            data
        )  # not **data because we could have potentially lists, model_validate can receive any type of input
    except ValidationError as e:
        raise VLMResponseParsingError(raw, f"Validation error: {e}") from e
