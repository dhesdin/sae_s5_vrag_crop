import asyncio
import time
from pathlib import Path

from v_crop_rag.config import EMBEDDING_MODEL, OLLAMA_URL
from v_crop_rag.ollama_client.embedding import OllamaEmbedding
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper
from v_crop_rag.service.core import search_image
from v_crop_rag.storage.chroma import ChromaVectorIndex

# ==== CONSTANT ==== #
CHROMA_PATH = Path("data/chroma")
COLLECTION_NAME = "crop_embeddings"
K = 3
# (query, expected images), checked against dataset/ground_truth.json
QUERIES = [
    ("un ananas", ["kitchen_0.jpg", "market_0.jpg"]),
    ("un scooter", ["terace_2.jpg", "car_0.jpg"]),
    ("un réverbère", ["bicycle_2.jpg"]),
    ("un mètre ruban", ["workbench_2.jpg"]),
    ("une voiture de sport rouge", ["car_2.jpg"]),
    ("un vélo bleu", ["bicycle_1.jpg"]),
    ("un parasol multicolore", ["beach_1.jpg"]),
    ("un sous-bois d'automne", ["bench_1.jpg"]),
    ("des îlots rocheux dans une eau turquoise", ["beach_0.jpg"]),
    ("un mur rose", ["bicycle_0.jpg"]),
]

async def main() -> None:
    client = OllamaWrapper(base_url=OLLAMA_URL, timeout_s=300)

    if not await client.is_server_running():
        raise SystemExit("Ollama server is not running")

    # a missing folder would silently create an empty index
    if not CHROMA_PATH.exists():
        raise SystemExit(f"{CHROMA_PATH} not found, run scripts/manual_dataset_index.py first")

    embedding = OllamaEmbedding(client=client, model=EMBEDDING_MODEL)
    index = ChromaVectorIndex(path=CHROMA_PATH, collection_name=COLLECTION_NAME)

    hits = 0
    # loop for each query and its expected images
    for query, expected in QUERIES:
        start = time.perf_counter()
        found = await search_image(query, embedding, index, k=K)
        elapsed = time.perf_counter() - start

        images = []
        for row in found:
            images.append(row["image"])

        # rank of the first expected image (1 = best), None if absent from the top K
        rank = None
        for position, image in enumerate(images, start=1):
            if image in expected:
                rank = position
                break
        if rank is not None:
            hits += 1

        # how many of the expected images are in the top K
        expected_found = 0
        for image in expected:
            if image in images:
                expected_found += 1

        print("Query:", query)
        print("  expected:", expected)
        print("  rank of first expected:", rank)
        print("  expected found:", expected_found, "/", len(expected))
        print("  images returned:", len(found), "/", K)
        print("  time:", elapsed, "seconds")
        for row in found:
            print("   ", row["image"], row["distance"], row["matched"])

    print("Top", K, "hits:", hits, "/", len(QUERIES))
 
if __name__ == "__main__":
    asyncio.run(main())