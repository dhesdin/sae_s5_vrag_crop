from pathlib import Path
from unittest.mock import create_autospec

import pytest

from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaGenerateResult, OllamaWrapper
from v_crop_rag.ollama_client.vlm import OllamaVLM


@pytest.mark.asyncio
async def test_generate_returns_vlm_response():
    client = create_autospec(OllamaWrapper, instance=True)

    client.generate_with_image.return_value = OllamaGenerateResult(response="Description de l'image")  # dont contact Ollama & return this response

    vlm = OllamaVLM(client=client, model="qwen3-vl:instruct")

    image = Path("image.jpg")

    result = await vlm.generate(prompt="Décris cette image", image=image)

    assert result == "Description de l'image"
    client.generate_with_image.assert_awaited_once_with(model="qwen3-vl:instruct", prompt="Décris cette image", image=image)


def test_model_must_be_string():
    client = create_autospec(OllamaWrapper, instance=True)

    with pytest.raises(TypeError):
        OllamaVLM(client=client, model=123)


def test_model_must_not_be_empty():
    client = create_autospec(OllamaWrapper, instance=True)

    with pytest.raises(ValueError):
        OllamaVLM(client=client, model="   ")


@pytest.mark.asyncio
async def test_prompt_must_be_string():
    client = create_autospec(OllamaWrapper, instance=True)
    vlm = OllamaVLM(client=client, model="qwen3-vl:instruct")

    with pytest.raises(TypeError):
        await vlm.generate(prompt=123, image=Path("Image.jpg"))


@pytest.mark.asyncio
async def test_prompt_must_not_be_empty():
    client = create_autospec(OllamaWrapper, instance=True)
    vlm = OllamaVLM(client=client, model="qwen3-vl:instruct")

    with pytest.raises(ValueError):
        await vlm.generate(prompt="   ", image=Path("Image.jpg"))


@pytest.mark.asyncio
async def test_image_must_be_supported():
    client = create_autospec(OllamaWrapper, instance=True)
    vlm = OllamaVLM(client=client, model="qwen3-vl:instruct")

    with pytest.raises(TypeError):
        await vlm.generate(prompt="Décris cette image", image=123)
