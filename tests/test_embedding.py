from unittest.mock import create_autospec

import pytest

from v_crop_rag.ollama_client.embedding import OllamaEmbedding
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper


@pytest.mark.asyncio
async def test_embed_returns_vector():
    client = create_autospec(OllamaWrapper, instance=True)

    expected_vector = [0.1, 0.2, -0.3]

    client.embed.return_value = expected_vector

    embedding = OllamaEmbedding(client=client, model="embeddinggemma")

    result = await embedding.embed("sentence of test")

    assert result == expected_vector
    client.embed.assert_awaited_once_with(model="embeddinggemma", text="sentence of test")


def test_model_must_be_string():
    client = create_autospec(OllamaWrapper, instance=True)

    with pytest.raises(TypeError):
        OllamaEmbedding(client=client, model=123)


def test_model_must_not_be_empty():
    client = create_autospec(OllamaWrapper, instance=True)

    with pytest.raises(ValueError):
        OllamaEmbedding(client=client, model="  ")


@pytest.mark.asyncio
async def test_text_must_be_string():
    client = create_autospec(OllamaWrapper, instance=True)
    embedding = OllamaEmbedding(client=client, model="embeddinggemma")

    with pytest.raises(TypeError):
        await embedding.embed(text=123)


@pytest.mark.asyncio
async def test_text_must_not_be_empty():
    client = create_autospec(OllamaWrapper, instance=True)
    embedding = OllamaEmbedding(client=client, model="embeddinggemma")

    with pytest.raises(ValueError):
        await embedding.embed(text="   ")
