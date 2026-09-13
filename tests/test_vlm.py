from pathlib import Path
from unittest.mock import Mock

import pytest

from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaGenerateResult, OllamaWrapper
from v_crop_rag.ollama_client.vlm import OllamaVLM


def test_generate_returns_vlm_response():
    client = Mock(spec=OllamaWrapper)  # Create a mock of ollamaWrapper

    client.generate_with_image.return_value = OllamaGenerateResult(response="Description de l'image")  # dont contact Ollama & return this response

    vlm = OllamaVLM(client=client, model="qwen3-vl:instruct")

    image = Path("image.jpg")

    result = vlm.generate(prompt="Décris cette image", image=image)

    assert result == "Description de l'image"
    client.generate_with_image.assert_called_once_with(model="qwen3-vl:instruct", prompt="Décris cette image", image=image)


def test_model_must_be_string():
    client = Mock(spec=OllamaWrapper)

    with pytest.raises(TypeError):
        OllamaVLM(client=client, model=123)


def test_model_must_not_be_empty():
    client = Mock(spec=OllamaWrapper)

    with pytest.raises(ValueError):
        OllamaVLM(client=client, model="   ")


def test_prompt_must_be_string():
    client = Mock(spec=OllamaWrapper)
    vlm = OllamaVLM(client=client, model="qwen3-vl:instruct")

    with pytest.raises(TypeError):
        vlm.generate(prompt=123, image=Path("Image.jpg"))


def test_prompt_must_not_be_empty():
    client = Mock(spec=OllamaWrapper)
    vlm = OllamaVLM(client=client, model="qwen3-vl:instruct")

    with pytest.raises(ValueError):
        vlm.generate(prompt="   ", image=Path("Image.jpg"))


def test_image_must_be_supported():
    client = Mock(spec=OllamaWrapper)
    vlm = OllamaVLM(client=client, model="qwen3-vl:instruct")

    with pytest.raises(TypeError):
        vlm.generate(prompt="Décris cette image", image=123)
