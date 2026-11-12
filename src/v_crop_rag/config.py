"""Application configuration, read from environment variables (and from the .env file if present)."""

import os
from pathlib import Path

from dotenv import load_dotenv

# config.py is in src/v_crop_rag/ -> parents[0]=v_crop_rag, parents[1]=src, parents[2]=repository root
ROOT_DIR = Path(__file__).resolve().parents[2]

# Load .env into the environment. If the file doesn't exist, nothing happens (no error).
# A variable already defined in the real environment is NOT overwritten by .env.
load_dotenv(ROOT_DIR / ".env")

# Second argument = default value, used when the variable is defined nowhere (e.g. GitHub CI)
OLLAMA_URL = os.getenv("VCROP_OLLAMA_URL", "http://10.22.28.190:11434")
VLM_MODEL = os.getenv("VCROP_VLM_MODEL", "qwen3-vl:8b-instruct")
EMBEDDING_MODEL = os.getenv("VCROP_EMBEDDING_MODEL", "embeddinggemma:latest")
