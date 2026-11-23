import asyncio
import time
from pathlib import Path

from v_crop_rag.config import EMBEDDING_MODEL
from v_crop_rag.ollama_client.embedding import OllamaEmbedding
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper
from v_crop_rag.service.core import search_image
from v_crop_rag.storage.chroma import ChromaVectorIndex

# ==== CONSTANT ==== #
CHROMA_PATH = Path("data/chroma")
COLLECTION_NAME = "crop_embeddings"
K = 3


async def main() -> None:
    client = OllamaWrapper(timeout_s=300)

    if not await client.is_server_running():
        raise SystemExit("Ollama server is not running")

    # a missing folder would silently create an empty index
    if not CHROMA_PATH.exists():
        raise SystemExit(f"{CHROMA_PATH} not found, run scripts/manual_dataset_index.py first")

    embedding = OllamaEmbedding(client=client, model=EMBEDDING_MODEL)
    index = ChromaVectorIndex(path=CHROMA_PATH, collection_name=COLLECTION_NAME)

    query = "un ananas"
    start = time.perf_counter()
    found = await search_image(query, embedding, index, k=K)
    elapsed = time.perf_counter() - start

    print("Query:", query)
    print("Images returned:", len(found))
    for row in found:
        print(" ", row["image"], row["distance"], row["matched"])
    print("Time:", elapsed, "seconds")


if __name__ == "__main__":
    asyncio.run(main())