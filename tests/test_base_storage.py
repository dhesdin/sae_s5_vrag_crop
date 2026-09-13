import pytest

from v_crop_rag.storage.base import BaseVectorIndex, VectoreSearchResult


def test_base_vector_index_cannot_be_instanciated():
    with pytest.raises(TypeError):
        BaseVectorIndex()


def test_vector_search_result_stores_values():
    result = VectoreSearchResult(id="object_123", score=0.51, metadata={"label": "test"})

    assert result.id == "object_123"
    assert result.score == 0.51
    assert result.metadata == {"label": "test"}
