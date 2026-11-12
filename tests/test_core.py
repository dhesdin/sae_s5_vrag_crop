from pathlib import Path

import pytest
from chromadb.api.types import validate_metadata

from v_crop_rag.ollama_client.base import BaseEmbedding, BaseVLM
from v_crop_rag.service.core import index_image
from v_crop_rag.service.parsing import VLMResponseParsingError
from v_crop_rag.service.schemas import BoundingBox, DetectedObject, ImageDescription
from v_crop_rag.storage.base import BaseVectorIndex
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaConnectionError
from v_crop_rag.service.core import index_dataset, index_image


class EmbeddingError(Exception):
    """Raised by FakeEmbedding to simulate a failure during embedding."""


def build_description_json(
    main_subject="un vélo rouge appuyé contre un mur",
    background="rue pavée en ville, façade d'immeuble en pierre, fin de journée",
    detected_objects=None,
):
    """Build a VLM JSON response from a real ImageDescription, never hand-written JSON."""
    if detected_objects is None:
        detected_objects = []

    description = ImageDescription(
        main_subject=main_subject,
        background=background,
        detected_objects=detected_objects,
    )
    return description.model_dump_json()


class FakeVLM(BaseVLM):
    """Fake VLM: always returns the same response, remembers each call."""

    def __init__(self, response):
        self.response = response
        self.calls = []

    async def generate(self, prompt, image):
        self.calls.append((prompt, image))
        return self.response


class FakeEmbedding(BaseEmbedding):
    """Fake embedding: always returns the same vector, remembers each text received."""

    def __init__(self, vector=None, fail_at=None):
        if vector is None:
            vector = [0.1, 0.2, 0.3]
        self.vector = vector
        self.fail_at = fail_at
        self.texts = []
        self.call_count = 0

    async def embed(self, text):
        self.call_count += 1
        self.texts.append(text)
        if self.fail_at is not None and self.call_count == self.fail_at:
            raise EmbeddingError("embedding failed")
        return self.vector


class FakeIndex(BaseVectorIndex):
    """Fake index: remembers every entry added; query is never used in these tests."""

    def __init__(self):
        self.added = []

    def add(self, id, vector, metadata):
        self.added.append((id, vector, metadata))

    def query(self, vector, k=5):
        return []


# background, then the detected objects, then the main subject last, in that exact order
@pytest.mark.asyncio
async def test_writes_background_objects_and_main_subject_in_order():
    objects = [
        DetectedObject(label="vélo", color="rouge", position="centre", state="à l'arrêt"),
        DetectedObject(label="panneau de signalisation", color="bleu", position="en haut à droite", state=None),
    ]
    vlm = FakeVLM(build_description_json(detected_objects=objects))
    embedding = FakeEmbedding()
    index = FakeIndex()

    await index_image(Path("photo"), vlm, embedding, index)

    ids_written = []
    for entry in index.added:
        ids_written.append(entry[0])

    assert ids_written == ["photo:background", "photo:0", "photo:1", "photo:main"]


# the returned count always matches how many entries were actually written
@pytest.mark.asyncio
async def test_return_value_equals_number_of_adds():
    objects = [DetectedObject(label="vélo", color="rouge", position="centre", state="à l'arrêt")]
    vlm = FakeVLM(build_description_json(detected_objects=objects))
    embedding = FakeEmbedding()
    index = FakeIndex()

    result = await index_image(Path("photo"), vlm, embedding, index)

    assert result == len(index.added)


# an object with nothing to embed is skipped, the next object keeps its original index
@pytest.mark.asyncio
async def test_object_with_empty_text_is_skipped():
    objects = [
        DetectedObject(label="vélo", color="rouge", position="centre", state="à l'arrêt"),
        DetectedObject(label="", color=None, position="quelque part", state=None),
        DetectedObject(label="panneau de signalisation", color="bleu", position="en haut à droite", state=None),
    ]
    vlm = FakeVLM(build_description_json(detected_objects=objects))
    embedding = FakeEmbedding()
    index = FakeIndex()

    await index_image(Path("photo"), vlm, embedding, index)

    ids_written = []
    for entry in index.added:
        ids_written.append(entry[0])

    assert "photo:0" in ids_written
    assert "photo:2" in ids_written
    assert "photo:1" not in ids_written


# if an embed call fails, the exception propagates and nothing is written to the index
@pytest.mark.asyncio
async def test_embed_failure_writes_nothing():
    objects = [DetectedObject(label="vélo", color="rouge", position="centre", state="à l'arrêt")]
    vlm = FakeVLM(build_description_json(detected_objects=objects))
    embedding = FakeEmbedding(fail_at=2)  # 1st call = background, 2nd call = the object
    index = FakeIndex()

    with pytest.raises(EmbeddingError):
        await index_image(Path("photo"), vlm, embedding, index)

    assert index.added == []


# a non-JSON VLM response fails parsing before any embedding or write happens
@pytest.mark.asyncio
async def test_non_json_response_raises_parsing_error():
    vlm = FakeVLM("ceci n'est pas du json du tout")
    embedding = FakeEmbedding()
    index = FakeIndex()

    with pytest.raises(VLMResponseParsingError):
        await index_image(Path("photo"), vlm, embedding, index)

    assert embedding.texts == []
    assert index.added == []


# an empty main_subject is rejected before any embedding or write happens
@pytest.mark.asyncio
async def test_empty_main_subject_raises_value_error():
    vlm = FakeVLM(build_description_json(main_subject=""))
    embedding = FakeEmbedding()
    index = FakeIndex()

    with pytest.raises(ValueError):
        await index_image(Path("photo"), vlm, embedding, index)

    assert embedding.texts == []
    assert index.added == []


# a whitespace-only main_subject is rejected the same way as an empty one
@pytest.mark.asyncio
async def test_blank_main_subject_raises_value_error():
    vlm = FakeVLM(build_description_json(main_subject="   "))
    embedding = FakeEmbedding()
    index = FakeIndex()

    with pytest.raises(ValueError):
        await index_image(Path("photo"), vlm, embedding, index)

    assert embedding.texts == []
    assert index.added == []


# a wrong image_path type is rejected before the VLM is ever called
@pytest.mark.asyncio
async def test_wrong_image_path_type_raises_before_vlm_call():
    vlm = FakeVLM(build_description_json())
    embedding = FakeEmbedding()
    index = FakeIndex()

    with pytest.raises(TypeError):
        await index_image("photo.jpg", vlm, embedding, index)

    assert vlm.calls == []


# the object's position never appears in the embedded text, only label/color/state do
@pytest.mark.asyncio
async def test_object_position_not_in_embedded_text():
    objects = [DetectedObject(label="vélo", color="rouge", position="en haut à gauche", state="à l'arrêt")]
    vlm = FakeVLM(build_description_json(detected_objects=objects))
    embedding = FakeEmbedding()
    index = FakeIndex()

    await index_image(Path("photo"), vlm, embedding, index)

    object_text = embedding.texts[1]  # 0 = background, 1 = object, 2 = main subject
    assert object_text == "vélo rouge à l'arrêt"
    assert "en haut à gauche" not in object_text


# bbox presence/absence is reflected exactly in has_bbox and the bbox_* metadata keys
@pytest.mark.asyncio
async def test_bbox_metadata_reflects_presence_or_absence():
    objects = [
        DetectedObject(label="vélo", color="rouge", position="centre", state="à l'arrêt", bounding_box=None),
        DetectedObject(
            label="panneau de signalisation",
            color="bleu",
            position="en haut à droite",
            state=None,
            bounding_box=BoundingBox(x=1, y=2, width=3, height=4),
        ),
    ]
    vlm = FakeVLM(build_description_json(detected_objects=objects))
    embedding = FakeEmbedding()
    index = FakeIndex()

    await index_image(Path("photo"), vlm, embedding, index)

    metadata_without_bbox = None
    metadata_with_bbox = None
    for entry_id, vector, metadata in index.added:
        if entry_id == "photo:0":
            metadata_without_bbox = metadata
        if entry_id == "photo:1":
            metadata_with_bbox = metadata

    assert metadata_without_bbox["has_bbox"] is False
    assert "bbox_x" not in metadata_without_bbox

    assert metadata_with_bbox["has_bbox"] is True
    assert "bbox_x" in metadata_with_bbox
    assert "bbox_y" in metadata_with_bbox
    assert "bbox_width" in metadata_with_bbox
    assert "bbox_height" in metadata_with_bbox


# every metadata dict written to the index is accepted by Chroma's own validator
@pytest.mark.asyncio
async def test_all_metadata_is_valid_for_chroma():
    objects = [
        DetectedObject(label="vélo", color="rouge", position="centre", state="à l'arrêt"),
        DetectedObject(
            label="panneau de signalisation",
            color=None,
            position="en haut à droite",
            state=None,
            bounding_box=BoundingBox(x=1, y=2, width=3, height=4),
        ),
    ]
    vlm = FakeVLM(build_description_json(detected_objects=objects))
    embedding = FakeEmbedding()
    index = FakeIndex()

    await index_image(Path("photo"), vlm, embedding, index)

    for entry_id, vector, metadata in index.added:
        validate_metadata(metadata)
        for value in metadata.values():
            assert value is not None
            assert not isinstance(value, dict)


# an empty background is skipped, but the objects and the main subject are still indexed
@pytest.mark.asyncio
async def test_empty_background_is_skipped():
    objects = [DetectedObject(label="vélo", color="rouge", position="centre", state="à l'arrêt")]
    vlm = FakeVLM(build_description_json(background="   ", detected_objects=objects))
    embedding = FakeEmbedding()
    index = FakeIndex()

    await index_image(Path("photo"), vlm, embedding, index)

    ids_written = []
    for entry in index.added:
        ids_written.append(entry[0])

    assert ids_written == ["photo:0", "photo:main"]

class DownVLM(BaseVLM):
    """Fake VLM: the Ollama server is down."""

    async def generate(self, prompt, image):
        raise OllamaConnectionError("server down")


# every image is indexed and listed, nothing fails
@pytest.mark.asyncio
async def test_index_dataset_indexes_every_image():
    vlm = FakeVLM(build_description_json())

    result = await index_dataset([Path("a.jpg"), Path("b.jpg")], vlm, FakeEmbedding(), FakeIndex())

    assert result == {"indexed": ["a.jpg", "b.jpg"], "failed": []}


# a bad VLM answer does not stop the run: both images are listed as failed
@pytest.mark.asyncio
async def test_index_dataset_continues_after_bad_answer():
    vlm = FakeVLM("not json at all")

    result = await index_dataset([Path("a.jpg"), Path("b.jpg")], vlm, FakeEmbedding(), FakeIndex())

    assert result["indexed"] == []
    assert [name for name, reason in result["failed"]] == ["a.jpg", "b.jpg"]


# a server error is not caught: it stops the whole run
@pytest.mark.asyncio
async def test_index_dataset_stops_on_connection_error():
    with pytest.raises(OllamaConnectionError):
        await index_dataset([Path("a.jpg")], DownVLM(), FakeEmbedding(), FakeIndex())