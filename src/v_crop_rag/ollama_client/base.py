from typing import Any

import httpx


class BaseModelEndpoint:
    """Common base for clients communicating with Ollama models"""

    def __init__(self, base_url: str, model: str, timeout: float = 30.0) -> None:

        if not base_url.strip():
            raise ValueError("base_url must not be empty")

        if not model.strip():
            raise ValueError("model must not be empty")

        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    async def _post(self, endpoint: str, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # creation http client
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=payload)

        response.raise_for_status()

        return response.json()
