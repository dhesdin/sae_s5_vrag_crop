 # To test this script outside IUT, you should be have an instance of ollama on your computer and can test in comment off the client declaration
import asyncio
from pathlib import Path

from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper
from v_crop_rag.ollama_client.vlm import OllamaVLM
from v_crop_rag.service.prompts import build_extraction_prompt


MODEL = "qwen3-vl:8b-instruct"
# Home model
#MODEL = "qwen3-vl:2b-instruct" 

IMAGE_PATH = Path("dataset/market_0.jpg")


async def main():

    # client initialization
    client = OllamaWrapper()
    
    # client = OllamaWrapper(base_url="http://localhost:11434")

    if not await client.is_server_running():
        raise SystemExit("The Ollama server is not running.")
    
    #  vlm call
    vlm = OllamaVLM(client=client, model=MODEL)

    prompt = build_extraction_prompt()


    # test 
    raw_response= await vlm.generate(prompt=prompt, image=IMAGE_PATH)

    print(f"Raw Response from VLM : {raw_response}")
    print(f"LENGTH characters from response VLM : {len(raw_response)}")


if __name__  == "__main__":
    asyncio.run(main())