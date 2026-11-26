import pytest
from fastapi.testclient import TestClient

from backend.app import App
from backend.routers import requestsRouter
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaConnectionError

RESULTS = [
    {"image": "market_0.jpg", "distance": 0.531, "similarity": 0.734, "matched": "ananas jaune dans un bac"},
    {"image": "kitchen_0.jpg", "distance": 0.602, "similarity": 0.699, "matched": "ananas sur une table"},
]


@pytest.fixture
def client() -> TestClient:
    return TestClient(App())


# Replace the real search_images (Ollama + Chroma) with a fake one
def _patch_search(monkeypatch, fake) -> None:
    monkeypatch.setattr(requestsRouter, "search_images", fake)


def _raising(error: Exception):
    async def fake(query: str, k: int = 5) -> list[dict]:
        raise error

    return fake


def test_search_returns_results_with_rank(monkeypatch, client):
    calls = []

    async def fake(query: str, k: int = 5) -> list[dict]:
        calls.append((query, k))
        return RESULTS

    _patch_search(monkeypatch, fake)

    response = client.post("/requests/", json={"query": "un ananas", "k": 3})

    assert response.status_code == 200
    assert calls == [("un ananas", 3)]
    body = response.json()
    assert [r["rank"] for r in body] == [1, 2]
    assert body[0] == {"rank": 1, **RESULTS[0]}


def test_search_k_defaults_to_5(monkeypatch, client):
    calls = []

    async def fake(query: str, k: int = 5) -> list[dict]:
        calls.append(k)
        return []

    _patch_search(monkeypatch, fake)

    response = client.post("/requests/", json={"query": "un ananas"})

    assert response.status_code == 200
    assert response.json() == []
    assert calls == [5]


@pytest.mark.parametrize(
    ("error", "status"),
    [
        (ValueError("query is blank"), 422),
        (OllamaConnectionError("unreachable"), 503),
        (FileNotFoundError("data/chroma not found"), 500),
    ],
)
def test_search_converts_service_errors(monkeypatch, client, error, status):
    _patch_search(monkeypatch, _raising(error))

    response = client.post("/requests/", json={"query": "un ananas"})

    assert response.status_code == status


@pytest.mark.parametrize("payload", [{"query": "un ananas", "k": 0}, {"k": 3}, {"query": "un ananas", "k": "abc"}])
def test_search_rejects_invalid_body(monkeypatch, client, payload):
    _patch_search(monkeypatch, _raising(AssertionError("search_images should not be called")))

    response = client.post("/requests/", json=payload)

    assert response.status_code == 422
