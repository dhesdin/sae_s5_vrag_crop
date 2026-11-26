import pytest

from tests.test_core import FakeEmbedding, FakeIndex, make_result
from v_crop_rag.config import ELEMENTS_PER_IMAGE
from v_crop_rag.service import search_service


# Replace search_service._build_dependencies with a temporary function during tests
def _patch_dependencies(monkeypatch, embedding, index):
    monkeypatch.setattr(search_service, "_build_dependencies", lambda: (embedding, index))


# Tests for the search_service module
@pytest.mark.asyncio
async def test_search_images_returns_results_and_passes_k(monkeypatch):
    index = FakeIndex(
        [
            make_result("market_0.jpg:0", 0.5, "market_0.jpg"),
            make_result("kitchen_0.jpg:0", 0.6, "kitchen_0.jpg"),
        ]
    )
    _patch_dependencies(monkeypatch, FakeEmbedding(), index)

    results = await search_service.search_images("un ananas", k=3)

    assert len(results) == 2
    assert results[0]["image"] == "market_0.jpg"
    assert set(results[0].keys()) == {"image", "distance", "matched"}
    assert index.query_calls[0][1] == 3 * ELEMENTS_PER_IMAGE


# Test for search_images when the query is empty or whitespace
@pytest.mark.asyncio
async def test_search_images_does_not_catch_value_error(monkeypatch):
    _patch_dependencies(monkeypatch, FakeEmbedding(), FakeIndex())

    with pytest.raises(ValueError):
        await search_service.search_images("   ")


# Test for _build_dependencies when the index is missing
def test_build_dependencies_raises_when_index_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(search_service, "CHROMA_PATH", tmp_path / "missing")
    search_service._build_dependencies.cache_clear()  # Clear the cache to force rebuilding dependencies

    with pytest.raises(FileNotFoundError):
        search_service._build_dependencies()
