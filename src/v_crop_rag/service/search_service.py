from functools import cache

from v_crop_rag.config import EMBEDDING_MODEL, ROOT_DIR
from v_crop_rag.ollama_client.embedding import OllamaEmbedding
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper
from v_crop_rag.service.core import search_image
from v_crop_rag.storage.chroma import ChromaVectorIndex

COLLECTION_NAME = "crop_embeddings"
CHROMA_PATH = ROOT_DIR / "data" / "chroma"


@cache
def _build_dependencies() -> tuple[OllamaEmbedding, ChromaVectorIndex]:
    """
    Build and return the necessary dependencies for the search service.
    The results is stored in the cache, build once then reused

    Raises:
        FileNotFoundError: If the Chroma index file (chroma.sqlite3) is missing in the expected path.

    Returns:
        tuple[OllamaEmbedding, ChromaVectorIndex]: The embedding model and the vector index.
    """
    if not (CHROMA_PATH / "chroma.sqlite3").exists():
        raise FileNotFoundError(f"No Chroma index in {CHROMA_PATH} (chroma.sqlite3 missing), run scripts/manual_dataset_index.py first")

    # build client (10 sec) bc w/o warmup we've got around ~2 secs for each request
    client = OllamaWrapper(timeout_s=10)

    embedding = OllamaEmbedding(client=client, model=EMBEDDING_MODEL)
    index = ChromaVectorIndex(path=CHROMA_PATH, collection_name=COLLECTION_NAME)

    return embedding, index


async def search_images(query: str, k: int = 5) -> list[dict]:
    """
    Search the indexed dataset for the images that best match a text query.

    The first call builds the embedding client and the vector index, later
    calls reuse them. Each image appears at most once, represented by its
    closest element.

    Args:
        query (str): The search text. Truncated to 100 characters.
        k (int, optional): The maximum number of images to return. Defaults to 5.

    Returns:
        list[dict]: At most k results, sorted by increasing distance. Each result
            has the keys "image" (file name, e.g. "market_0.jpg"), "distance"
            (float, smaller means closer), "similarity" (float, cosine similarity
            from -1 to 1, higher means closer) and "matched" (text of the closest
            element of the image).

    Raises:
        TypeError: If query is not a string, or k is not an integer (bool refused).
        ValueError: If query is blank or k is lower than 1.
        FileNotFoundError: If no Chroma index is found (chroma.sqlite3 missing).
        OllamaConnectionError: If the Ollama server cannot be reached.
    """

    embedding, index = _build_dependencies()
    return await search_image(query=query, embedding=embedding, index=index, k=k)
