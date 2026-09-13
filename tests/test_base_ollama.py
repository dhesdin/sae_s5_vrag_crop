import pytest

from v_crop_rag.ollama_client.base import BaseEmbedding, BaseVLM


def test_base_vlm_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseVLM()


def test_base_embedding_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseEmbedding()
