from v_crop_rag.ollama_client.embedding import OllamaEmbedding
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaWrapper


client = OllamaWrapper()

embedding_model = OllamaEmbedding(
    client=client,
    model="embeddinggemma",
)

vector = embedding_model.embed(
    "Un vélo rouge est posé contre un mur."
)

print("Type :", type(vector))
print("Dimension :", len(vector))
print("Premières valeurs :", vector[:10])

vector1 = embedding_model.embed("Un vélo rouge")
vector2 = embedding_model.embed("Un vélo noir")

print(len(vector1))
print(len(vector2))
print(vector1 == vector2)

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
