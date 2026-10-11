from abc import ABC, abstractmethod
from pathlib import Path


class BaseVLM(ABC):
    """Common interface for VLM"""

    @abstractmethod
    async def generate(self, prompt: str, image: str | Path | bytes) -> str:
        """Generate a textual response from a prompt and an image"""
        raise NotImplementedError


class BaseEmbedding(ABC):
    """common Interface for embedding models"""

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        """transform a text in vectors"""
        raise NotImplementedError
