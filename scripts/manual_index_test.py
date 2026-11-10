import asyncio
from math import sqrt
import tempfile
import time
from pathlib import Path

from v_crop_rag.ollama_client.embedding import OllamaEmbedding
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper
from v_crop_rag.ollama_client.vlm import OllamaVLM
from v_crop_rag.service.core import index_image
from v_crop_rag.service.prompts import build_extraction_prompt
from v_crop_rag.storage.chroma import ChromaVectorIndex

# ==== CONSTANT ==== #
IMAGE_PATH = Path("dataset/market_0.jpg")
# temp folder to avoid persisting the chroma index permanently
CHROMA_PATH_TEMP = Path(tempfile.mkdtemp())
COLLECTION_NAME = "crop_embeddings"
EMBEDDING_MODEL = "embeddinggemma:latest"
VLM_MODEL = "qwen3-vl:8b-instruct"
SHORT_TEXT = "Des pastèques verte et mûre"


async def main() -> None:
    # setup
    client = OllamaWrapper(timeout_s=300) # try with 300 s bc 60 TO

    # guard clauses
    if not await client.is_server_running():
        raise SystemExit("Ollama server is not running")

    if not IMAGE_PATH.exists():
        raise SystemExit(f"Image not found at {IMAGE_PATH}")

    # call models
    vlm = OllamaVLM(client=client, model=VLM_MODEL)
    embedding = OllamaEmbedding(client=client, model=EMBEDDING_MODEL)
    index = ChromaVectorIndex(path=CHROMA_PATH_TEMP, collection_name=COLLECTION_NAME)

    print("Models:", VLM_MODEL, EMBEDDING_MODEL)
    print("Image:", IMAGE_PATH)

    # embedding: dimension and norm of a real vector
    vector = await embedding.embed(text=SHORT_TEXT)
    norm = sqrt(sum(x * x for x in vector)) # normalize 
    print("Vector dimension:", len(vector))
    print("Vector norm:", norm)

    # VLM alone: time and raw answer
    start = time.perf_counter()
    raw_response = await vlm.generate(prompt=build_extraction_prompt(), image=IMAGE_PATH)
    print("VLM time:", time.perf_counter() - start, "seconds")
    print(raw_response)

    # index the same image twice
    for iteration in (1, 2):
        start = time.perf_counter()
        count = await index_image(image_path=IMAGE_PATH, vlm=vlm, embedding=embedding, index=index)
        print("Iteration", iteration, ":", count, "entries in", time.perf_counter() - start, "seconds")

        # what the index contains after this pass
        for result in index.query(vector, k=count):
            print("  ", result.id, result.distance)


if __name__ == "__main__":
    asyncio.run(main())