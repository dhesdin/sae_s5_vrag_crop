 # To test this script outside IUT, you should be have an instance of ollama on your computer and can test in comment off the client declaration
import asyncio

from v_crop_rag.ollama_client.embedding import OllamaEmbedding
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper


async def main():

    client = OllamaWrapper()
   
    # client = OllamaWrapper(base_url="http://localhost:11434")

    embedding_model = OllamaEmbedding(
        client=client,
        model="embeddinggemma",
    )

    vector = await embedding_model.embed(
        "Un vélo rouge est posé contre un mur."
    )

    print("Type :", type(vector))
    print("Dimension :", len(vector))
    print("Premières valeurs :", vector[:10])

    vector1 = await embedding_model.embed("Un vélo rouge")
    vector2 = await embedding_model.embed("Un vélo noir")

    print(len(vector1))
    print(len(vector2))
    print(vector1 == vector2)


if __name__ == "__main__":
    asyncio.run(main())

# Test Ok pour la cohérence
# ==================================================
# Type : <class 'list'>
# Dimension : 768
# Premières valeurs : [-0.11639715, -0.029276002, 0.035711154, -0.003954126, 0.000330063, 0.028714223, 0.0007735396, -0.026074138, 0.046981074, -0.08361911]
# (.venv) kara@debianKaradoc:~/Documents/development/SAE_IA/sae_appli_ia/sae_s5_vrag_crop$ python scripts/manual_embedding_test.py 
# Type : <class 'list'>
# Dimension : 768
# Premières valeurs : [-0.11639715, -0.029276002, 0.035711154, -0.003954126, 0.000330063, 0.028714223, 0.0007735396, -0.026074138, 0.046981074, -0.08361911]
# 768
# 768
# False

# ================================================
# Avec :
# vector1 = embedding_model.embed("Un vélo rouge")
# vector2 = embedding_model.embed("Un vélo rouge")

# (.venv) kara@debianKaradoc:~/Documents/development/SAE_IA/sae_appli_ia/sae_s5_vrag_crop$ python scripts/manual_embedding_test.py 
# Type : <class 'list'>
# Dimension : 768
# Premières valeurs : [-0.11639715, -0.029276002, 0.035711154, -0.003954126, 0.000330063, 0.028714223, 0.0007735396, -0.026074138, 0.046981074, -0.08361911]
# 768
# 768
# True

# ==================================================
# Avec :
# vector1 = embedding_model.embed("Un vélo rouge")
# vector2 = embedding_model.embed("Un vélo ruge")

# (.venv) kara@debianKaradoc:~/Documents/development/SAE_IA/sae_appli_ia/sae_s5_vrag_crop$ python scripts/manual_embedding_test.py 
# Type : <class 'list'>
# Dimension : 768
# Premières valeurs : [-0.11639715, -0.029276002, 0.035711154, -0.003954126, 0.000330063, 0.028714223, 0.0007735396, -0.026074138, 0.046981074, -0.08361911]
# 768
# 768
# False
