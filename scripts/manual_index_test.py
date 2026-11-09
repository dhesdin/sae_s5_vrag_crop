from pathlib import Path

from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper
from v_crop_rag.service.core import index_image
# from v_crop_rag.storage.chroma import ChromaVectorIndex

# ==== CONSTANT ==== #
IMAGE_PATH = Path("dataset/market_0.jpg")
CHROMA_PATH = Path("data/chroma")
COLLECTION_NAME = "images"


def main() -> None:
    # one Ollama client reused for both the VLM call and the embedding call
    client = OllamaWrapper()

    # guard clauses
    if not client.is_server_running():
        raise SystemExit("Ollama server is not running")

    if not IMAGE_PATH.exists():
        raise SystemExit(f"Image not found at {IMAGE_PATH}")

    

    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO


if __name__ == "__main__":
    main()
