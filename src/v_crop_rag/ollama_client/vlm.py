from pathlib import Path

from v_crop_rag.ollama_client.base import BaseVLM
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper


class OllamaVLM(BaseVLM):
    """Implement a VLM using Ollama"""

    def __init__(self, client: OllamaWrapper, model: str) -> None:
        if not isinstance(model, str):
            raise TypeError("model must be a string")

        if model.strip() == "":
            raise ValueError("model is required")

        self._client = client
        self._model = model

    def generate(self, prompt: str, image: str | Path | bytes) -> str:
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")

        if prompt.strip() == "":
            raise ValueError("prompt is required")

        if not isinstance(image, str | Path | bytes):
            raise TypeError("image must be a string or a path or bytes")

        result = self._client.generate_with_image(model=self._model, prompt=prompt, image=image)
        return result.response
