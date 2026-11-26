import time
from pathlib import Path

from v_crop_rag.config import ELEMENTS_PER_IMAGE, MAX_QUERY_LENGTH
from v_crop_rag.ollama_client.base import BaseEmbedding, BaseVLM
from v_crop_rag.service.parsing import VLMResponseParsingError, parse_vlm_response
from v_crop_rag.service.prompts import build_extraction_prompt
from v_crop_rag.service.utils import bbox_to_metadata, image_to_metadata, object_to_text
from v_crop_rag.storage.base import BaseVectorIndex


# helper for existing ids
def _main_entry_id(image_path: Path) -> str:
    """Return the id of the ":main" entry, written last: if it exists, the image is fully indexed."""
    return f"{image_path.stem}:main"


async def index_image(image_path: Path, vlm: BaseVLM, embedding: BaseEmbedding, index: BaseVectorIndex) -> int:
    """
    Describe one image with the VLM, then embed and index its background,
    each detected object, and finally its main subject.

    Asynchronous: awaits the VLM call and every embedding call, sequentially (no concurrency).

    Args:
        image_path (Path): Path to the image to be indexed.
        vlm (BaseVLM): Vision model used to describe the image.
        embedding (BaseEmbedding): Embedding model used to vectorize text.
        index (BaseVectorIndex): The vector index where embeddings will be stored.
    Returns:
        int: number of entries written to the index.
    Raises:
        ValueError: if the VLM returns an empty main_subject, since without it the ":main"
            completion marker entry cannot be created.
    """

    # checked before the VLM call: a wrong type would otherwise fail after seconds of wasted inference
    if not isinstance(image_path, Path):
        raise TypeError("image_path must be a Path")

    # ==== PROMPT && RESPONSE ==== #
    # ask the VLM to describe the image as structured JSON
    prompt = build_extraction_prompt()
    raw_response = await vlm.generate(prompt=prompt, image=image_path)

    # ==== PARSING RESPONSE ==== #
    # turn the raw JSON text into a typed ImageDescription (main_subject, background, detected_objects)
    parsed_response = parse_vlm_response(raw_response)

    # main_subject is required: without it, the ":main" completion marker entry cannot be created
    main_subject_text = parsed_response.main_subject.strip()
    if not main_subject_text:
        raise ValueError(f"empty main_subject for {image_path.name}, cannot index it")

    # ==== COMPUTE EVERYTHING FIRST ==== #
    # collect (id, vector, metadata) here; nothing is written to the index until every
    # embedding below succeeded, so one failing embed can't leave the image half-indexed
    entries: list[tuple[str, list[float], dict]] = []

    # background: its own entry/vector, one embedding per element as required
    background_text = parsed_response.background.strip()
    if background_text:
        metadata = {**image_to_metadata(image_path, "background"), "text": background_text}
        entries.append((f"{image_path.stem}:background", await embedding.embed(text=background_text), metadata))

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
        entries.append((object_id, await embedding.embed(text=object_text), metadata))

    # it ensure the main subject entry is only added after all detected objects have been processed
    metadata = {**image_to_metadata(image_path, "main_subject"), "text": main_subject_text}
    entries.append((_main_entry_id(image_path), await embedding.embed(text=main_subject_text), metadata))

    # ==== WRITE EVERYTHING ONCE ALL EMBEDDINGS SUCCEEDED ==== #
    # (a) if any embedding above failed, nothing has been written to the index yet.
    # (b) a failure here, mid-loop, can still leave partial entries; but since ":main" is appended
    # last, its absence is exactly how an interrupted image is detected.
    for entry_id, vector, metadata in entries:
        index.add(id=entry_id, vector=vector, metadata=metadata)

    return len(entries)


async def index_dataset(image_paths: list[Path], vlm: BaseVLM, embedding: BaseEmbedding, index: BaseVectorIndex) -> dict:
    """Index every image not already indexed, skip the ones the VLM answers badly, stop on any other error.
    Args:
    image_paths: list[Path]
        List of image file paths to index.
    vlm: BaseVLM
        The visual language model used to extract information from images.
    embedding: BaseEmbedding
        The embedding model used to generate vector representations of text.
    index: BaseVectorIndex
        The vector index where the embeddings will be stored.

    Raises:
        VLMResponseParsingError: If the VLM response cannot be parsed correctly.
        ValueError: If there is an issue with the input data or embedding process.
    Returns:
        dict: A dictionary containing two keys:
            "indexed": list of names of successfully indexed images.
            "skipped": list of names of images that were already indexed.
            "failed": list of tuples with the name and reason for each skipped image.
    """
    indexed = []  # names of the indexed images
    skipped = []  # names of the images already fully indexed
    failed = []  # (name, reason) of the skipped imagesges

    for image_path in image_paths:
        if index.exists(_main_entry_id(image_path)):
            skipped.append(image_path.name)
            print(image_path.name, "already indexed")
            continue
        start = time.perf_counter()
        try:
            await index_image(image_path=image_path, vlm=vlm, embedding=embedding, index=index)
            indexed.append(image_path.name)
            print(image_path.name, "indexed in", time.perf_counter() - start, "seconds")

        except (VLMResponseParsingError, ValueError) as e:
            e_truncate = str(e)[:200]
            failed.append((image_path.name, e_truncate))  # 200 for truncating long error messages
            print(image_path.name, "FAILED", e_truncate)
    return {"indexed": indexed, "skipped": skipped, "failed": failed}


# REQUEST BY USER
async def search_image(query: str, embedding: BaseEmbedding, index: BaseVectorIndex, k: int = 5) -> list[dict]:
    """Search the indexed images that best match a text query.

    The index stores one entry per element (background, main subject, objects), so
    more entries than k are requested, then grouped by image.

    Args:
        query: Text to search for. Truncated to MAX_QUERY_LENGTH characters.
        embedding: Embedding model used to vectorize the query.
        index: Vector index to search in.
        k: Maximum number of distinct images to return.

    Raises:
        TypeError: If query is not a string, or k is not an integer.
        ValueError: If query is empty or only whitespace, or k is lower than 1.

    Returns:
        list[dict]: At most k dicts sorted by ascending distance, one per image, with the keys
            "image" (file name), "distance" (of its closest element) and "matched" (text of that element).
    """
    # ==== GUARD CLAUSES ==== #
    if not isinstance(query, str):
        raise TypeError("query must be a string")

    query = query.strip()
    if not query:
        raise ValueError("query is required")
    # bool is a subclass of int so it would pass the check w/o it
    if not isinstance(k, int) or isinstance(k, bool):
        raise TypeError("k must be an integer")

    if k < 1:
        raise ValueError("k must be at least 1")

    # the UI limits the length too this keeps the embedding input short to avoid the long queries and the dissipation
    query = query[:MAX_QUERY_LENGTH]

    # SEARCH
    query_vector = await embedding.embed(text=query)
    results = index.query(vector=query_vector, k=k * ELEMENTS_PER_IMAGE)

    # GROUP BY IMAGE
    # results are sorted by ascending distance, so the first entry seen for an image is its best one
    best_by_image: dict[str, dict] = {}
    for result in results:
        image_name = result.metadata["image"]
        if image_name not in best_by_image:
            best_by_image[image_name] = {
                "image": image_name,
                "distance": result.distance,
                "matched": result.metadata["text"],
            }

    sorted_images = sorted(best_by_image.values(), key=lambda x: x["distance"])  # trash the first key by keeping only values and sorted by dist
    return sorted_images[:k]
