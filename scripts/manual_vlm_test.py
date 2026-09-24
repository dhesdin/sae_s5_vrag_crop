from pathlib import Path

from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper
from v_crop_rag.ollama_client.vlm import OllamaVLM
from v_crop_rag.service.prompts import build_extraction_prompt


MODEL = "qwen3-vl:8b"
IMAGE_PATH = Path("dataset/market_0.jpg")


def main():

    # client initialization
    client = OllamaWrapper()

    if not client.is_server_running():
        raise SystemExit("The Ollama server is not running.")
    
    #  vlm call
    vlm = OllamaVLM(client=client, model=MODEL)

    prompt = build_extraction_prompt()


    # test 
    raw_response= vlm.generate(prompt=prompt, image=IMAGE_PATH)

    print(f"Raw Response from VLM : {raw_response}")
    print(f"LENGTH characters from response VLM : {len(raw_response)}")


if __name__  == "__main__":
    main()