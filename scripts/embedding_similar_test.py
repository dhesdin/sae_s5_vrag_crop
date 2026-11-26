 # To test this script outside IUT, you should be have an instance of ollama on your computer and can test in comment off the client declaration
import asyncio

from v_crop_rag import config
from v_crop_rag.ollama_client.embedding import OllamaEmbedding
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper


async def main():

    client = OllamaWrapper(base_url=config.OLLAMA_URL)
   
    # client = OllamaWrapper(base_url="http://localhost:11434")

    embedding_model = OllamaEmbedding(
        client=client,
        model=config.EMBEDDING_MODEL,
    )

    vector = await embedding_model.embed(
        "Un vélo rouge est posé contre un mur."
    )

    print("Type :", type(vector))
    print("Dimension :", len(vector))
    print("Premières valeurs :", vector[:10])

    vector1 = await embedding_model.embed("Un vélo rouge")
    vector2 = await embedding_model.embed("Un vélo rouge   ")
    print("Premières valeurs vecteur 1 :", vector1[:10])
    print("Premières valeurs vecteur 2 :", vector2[:10])
    
    vectordiff = []
    for i in range(768):
        vectordiff.append(vector1[i] - vector2[i])
    
   
    
    print("diff v1 et v2:", sum([abs(vector1 - vector2) for vector1, vector2 in zip(vector1, vector2)])/768) 

    print(len(vector1))
    print(len(vector2))
    print(vector1 == vector2)


if __name__ == "__main__":
    asyncio.run(main())


# RESULTATS
# =========
# Une même requête non strip renvoie des vecteurs différents.


# vélo rouge avec vélo rouge + 1 espace
# --------------------------------------
# Premières valeurs vecteur 1 : [-0.17827435, 0.0037179247, 0.048887454, 0.03244495, -0.011943421, 0.037082113, -0.0073966566, -0.02627692, 0.050054517, -0.06944796]
# Premières valeurs vecteur 2 : [-0.1716521, 0.0011739486, 0.057674084, 0.034080993, 0.0015760218, 0.0467715, -0.010559825, -0.02651357, 0.044634428, -0.069622956]
# diff v1 et v2: 0.006044017258226563



# vélo rouge avec vélo rouge + 2 espaces
# --------------------------------------
# Premières valeurs vecteur 1 : [-0.17827435, 0.0037179247, 0.048887454, 0.03244495, -0.011943421, 0.037082113, -0.0073966566, -0.02627692, 0.050054517, -0.06944796]
# Premières valeurs vecteur 2 : [-0.15479165, -0.014739653, 0.042558767, 0.0048341225, -0.017037978, 0.027064588, -0.0034196752, -0.044710383, 0.022375291, -0.04873106]
# diff v1 et v2: 0.013083543982446615



# vélo rouge avec vélo rouge + 3 espaces
# --------------------------------------
# Premières valeurs vecteur 1 : [-0.17827435, 0.0037179247, 0.048887454, 0.03244495, -0.011943421, 0.037082113, -0.0073966566, -0.02627692, 0.050054517, -0.06944796]
# Premières valeurs vecteur 2 : [-0.16008495, -0.019659573, 0.042797156, 0.001271841, -0.017242491, 0.023405436, -0.011129742, -0.04607026, 0.02041166, -0.05163033]
# diff v1 et v2: 0.013662344331652344
