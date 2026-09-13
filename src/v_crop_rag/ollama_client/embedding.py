from v_crop_rag.ollama_client.base import BaseEmbedding
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper


class OllamaEmbedding(BaseEmbedding):
    """Implement a Embedging using Ollama"""

    def __init__(self, client: OllamaWrapper, model: str) -> None:
        if not isinstance(model, str):
            raise TypeError("model must be a string")

        if model.strip() == "":
            raise ValueError("model is required")

        self._client = client
        self._model = model

    def embed(self, text: str) -> list[float]:
        if not isinstance(text, str):
            raise TypeError("text must be a string")

        if text.strip() == "":
            raise ValueError("text is required")

        return self._client.embed(model=self._model, text=text)
