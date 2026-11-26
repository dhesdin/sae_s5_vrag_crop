# Installation & lancement

## Prérequis

- Python 3.10 ou plus récent (la CI tourne en 3.12).
- `make` et `git`.
- Pour les appels réels aux modèles : être sur le **réseau de l'IUT**, où
  tourne le serveur Ollama. Hors IUT, un Ollama local fonctionne aussi à
  condition d'avoir téléchargé les deux modèles.

Les tests unitaires n'ont besoin ni du réseau ni d'Ollama : ils utilisent de
faux modèles.

## Installer

```bash
git clone https://github.com/dhesdin/sae_s5_vrag_crop.git
cd sae_s5_vrag_crop
make setup
source .venv/bin/activate
```

`make setup` crée `.venv/` et installe le projet en mode éditable avec les
dépendances de développement (`pip install -e .[dev]`).

## Configurer l'accès à Ollama

La configuration est lue dans `src/v_crop_rag/config.py`, depuis des
variables d'environnement ou un fichier `.env` à la racine :

```bash
cp .env.example .env
```

| Variable | Rôle | Valeur par défaut |
|---|---|---|
| `VCROP_OLLAMA_URL` | Adresse du serveur Ollama | serveur de l'IUT |
| `VCROP_VLM_MODEL` | Modèle de vision | `qwen3-vl:8b-instruct` |
| `VCROP_EMBEDDING_MODEL` | Modèle d'embedding | `embeddinggemma:latest` |

!!! warning "Changer de modèle d'embedding"
    Les vecteurs de deux modèles différents ne sont pas comparables. Si
    `VCROP_EMBEDDING_MODEL` change, il faut supprimer l'index et tout
    réindexer.

Pour un Ollama local :

```bash
ollama pull qwen3-vl:8b-instruct
ollama pull embeddinggemma:latest
# puis dans .env : VCROP_OLLAMA_URL=http://localhost:11434
```

## Vérifier que tout marche

```bash
make test                        # 136 tests, sans réseau
python scripts/manual_vlm_test.py   # un appel réel au VLM (réseau IUT)
```

## Commandes utiles

| Commande | Effet |
|---|---|
| `make test` | Tests unitaires (`pytest tests/ -q`) |
| `make lint` | `ruff check` puis `ruff format --check` |
| `make format` | Reformate le code avec Ruff |
| `make clean` | Supprime les caches Python, pytest et Ruff |

Pour la suite : [indexer le dataset](indexation.md), puis
[lancer une recherche](recherche.md).
