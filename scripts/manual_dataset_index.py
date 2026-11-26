import asyncio
import time
from pathlib import Path

from v_crop_rag.config import EMBEDDING_MODEL, VLM_MODEL
from v_crop_rag.ollama_client.embedding import OllamaEmbedding
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper
from v_crop_rag.ollama_client.vlm import OllamaVLM
from v_crop_rag.service.core import index_dataset
from v_crop_rag.service.dataset_loader import list_dataset_images
from v_crop_rag.storage.chroma import ChromaVectorIndex

# ==== CONSTANT ==== #
CHROMA_PATH = Path("data/chroma")
COLLECTION_NAME = "crop_embeddings"


async def main() -> None:
    # setup
    client = OllamaWrapper(timeout_s=300)


    # guard clauses
    if not await client.is_server_running():
        raise SystemExit("Ollama server is not running")

    # a half-filled index from an earlier run would mix two VLM answers for the same image
    if CHROMA_PATH.exists():
        raise SystemExit(f"{CHROMA_PATH} already exists, delete it to start from an empty index")

    # images
    images = list_dataset_images(Path("dataset"))

    # call models
    vlm = OllamaVLM(client=client, model=VLM_MODEL)
    embedding = OllamaEmbedding(client=client, model=EMBEDDING_MODEL)
    index = ChromaVectorIndex(path=CHROMA_PATH, collection_name=COLLECTION_NAME)

    print("Models:", VLM_MODEL, EMBEDDING_MODEL)
    print("Images to index:", len(images))

    start = time.perf_counter()
    result = await index_dataset(images, vlm, embedding, index)
    total = time.perf_counter() - start

    print("Indexed:", len(result["indexed"]))
    print("Failed:", result["failed"])
    print("Total time:", total, "seconds")


if __name__ == "__main__":
    asyncio.run(main())