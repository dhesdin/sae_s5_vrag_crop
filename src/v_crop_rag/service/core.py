from pathlib import Path

from v_crop_rag.ollama_client.base import BaseEmbedding, BaseVLM
from v_crop_rag.service.parsing import parse_vlm_response
from v_crop_rag.service.prompts import build_extraction_prompt
from v_crop_rag.service.utils import bbox_to_metadata, image_to_metadata, object_to_text
from v_crop_rag.storage.chroma import ChromaVectorIndex


def index_image(image_path: Path, vlm: BaseVLM, embedding: BaseEmbedding, index: ChromaVectorIndex) -> int:
    """
    Describe one image with the VLM, then embed and index its background,
    each detected object, and finally its main subject.

    Args:
        image_path (Path): Path to the image to be indexed.
        vlm (BaseVLM): Vision model used to describe the image.
        embedding (BaseEmbedding): Embedding model used to vectorize text.
        index (ChromaVectorIndex): The vector index where embeddings will be stored.
    Returns:
        int: number of entries written to the index.
    """

    # ==== PROMPT && RESPONSE ==== #
    # ask the VLM to describe the image as structured JSON
    prompt = build_extraction_prompt()
    raw_response = vlm.generate(prompt=prompt, image=image_path)

    # ==== PARSING RESPONSE ==== #
    # turn the raw JSON text into a typed ImageDescription (main_subject, background, detected_objects)
    parsed_response = parse_vlm_response(raw_response)

    # ==== COMPUTE EVERYTHING FIRST ==== #
    # collect (id, vector, metadata) here; nothing is written to the index until every
    # embedding below succeeded, so one failing embed can't leave the image half-indexed
    entries: list[tuple[str, list[float], dict]] = []

    # background: its own entry/vector, one embedding per element as required
    background_text = parsed_response.background.strip()
    if background_text:
        metadata = {**image_to_metadata(image_path, "background"), "text": background_text}
        entries.append((f"{image_path.stem}:background", embedding.embed(text=background_text), metadata))

    # one entry per detected object
    for i, obj in enumerate(parsed_response.detected_objects):
        # text to embed: label/color/state only (position stays out, it's not search vocabulary)
        object_text = object_to_text(obj=obj)

        # skip objects with nothing usable to embed (e.g. empty label and no color/state)
        if not object_text:
            continue

        # bbox flattened into scalars, plus label/position/source image so results are readable
        metadata = {
            **bbox_to_metadata(bbox=obj.bounding_box),
            "image": image_path.name,
            "label": obj.label,
            "position": obj.position,
            "type": "object",
            "text": object_text,
        }
        # separator : because the dataset filenames already contain "_{number}"
        object_id = f"{image_path.stem}:{i}"
        entries.append((object_id, embedding.embed(text=object_text), metadata))

    # it ensure the main subject entry is only added after all detected objects have been processed
    main_subject_text = parsed_response.main_subject.strip()
    if main_subject_text:
        metadata = {**image_to_metadata(image_path, "main_subject"), "text": main_subject_text}
        entries.append((f"{image_path.stem}:main", embedding.embed(text=main_subject_text), metadata))

    # ==== WRITE EVERYTHING ONCE ALL EMBEDDINGS SUCCEEDED ==== #
    for entry_id, vector, metadata in entries:
        index.add(id=entry_id, vector=vector, metadata=metadata)

    return len(entries)
