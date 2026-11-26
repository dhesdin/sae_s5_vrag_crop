# V-CROP RAG

SAE V-CROP RAG - recherche d'images par éléments constitutifs.

## Comment ça fonctionne

Un utilisateur tape une requête comme « un mètre ruban » et récupère les
images du dataset qui contiennent cet élément - même s'il ne s'agit pas du
sujet principal de la photo.

Le problème : une recherche d'image classique capture surtout l'ambiance
globale d'une photo, via un unique embedding de l'image entière. Un parasol
rouge en arrière-plan d'une photo de plage passe inaperçu, noyé dans
l'embedding global de la scène.

La solution : décomposer chaque image en éléments constitutifs (sujet
principal, arrière-plan, objets détectés avec couleur, position, état) via
un VLM, puis vectoriser **chaque élément séparément** plutôt que l'image
dans son ensemble. Une recherche peut ainsi remonter une image sur la base
d'un détail précis, pas seulement de son thème général.

Exemple de décomposition produite par le VLM pour une photo de plage :

```json
{
  "main_subject": "une plage de sable",
  "background": "un ciel bleu avec quelques nuages",
  "detected_objects": [
    {
      "label": "chaise longue",
      "color": "blanc",
      "position": "premier plan gauche",
      "state": "pliée",
      "bounding_box": {"x": 120, "y": 340, "width": 180, "height": 220}
    },
    {
      "label": "parasol",
      "color": "rouge et blanc",
      "position": "centre",
      "state": null,
      "bounding_box": {"x": 400, "y": 100, "width": 150, "height": 400}
    }
  ]
}
```

## Pipeline

```text
Indexation (une fois par image)                        Recherche (à chaque requête)
┌───────────────────────────────────────────┐           ┌───────────────────────────┐
│  dataset/*.jpg                            │           │  requête texte            │
│       │                                   │           │       │                   │
│       ▼                                   │           │       ▼                   │
│  VLM (description JSON structurée)        │           │  embedding de la requête  │
│       │                                   │           │       │                   │
│       ▼                                   │           │       ▼                   │
│  parsing défensif -> ImageDescription     │           │  comparaison vectorielle  │
│       │                                   │           │  (ChromaDB)               │
│       ▼                                   │           │       │                   │
│  1 embedding par élément détecté          ├──────────►│       ▼                   │
│  (sujet principal / décor / objet)        │           │  images correspondantes,  │
│       │                                   │           │  classées par pertinence  │
│       ▼                                   │           │                           │
│  stockage dans ChromaDB                   │           │                           │
└───────────────────────────────────────────┘           └───────────────────────────┘
     qwen3-vl:8b-instruct                                   embeddinggemma:latest
     embeddinggemma:latest
```

1. Le VLM (`qwen3-vl:8b-instruct`) reçoit chaque image avec un prompt
   qui impose une sortie JSON stricte (`service/prompts.py`).
2. La réponse brute est validée par un parsing défensif
   (`service/parsing.py`) : JSON invalide, champs manquants ou réponse
   entourée de texte libre sont gérés sans faire planter le pipeline.
3. Le décor, chaque objet détecté (texte `label couleur état`) et le sujet
   principal sont vectorisés séparément par le modèle d'embedding
   (`embeddinggemma:latest`), pas l'image entière.
4. Les vecteurs sont stockés dans ChromaDB avec leurs métadonnées (image
   source, type d'élément, texte, position, bounding box).
5. À la recherche, la requête texte est vectorisée par le même modèle, sans
   repasser par le VLM. Les éléments les plus proches sont regroupés par
   image et les images sont renvoyées classées par distance.

Les trois fonctions sont dans `src/v_crop_rag/service/core.py` :
`index_image`, `index_dataset` et `search_image`.

## État du projet (25/11/2026)

| Étape | État |
|---|---|
| Schéma, prompt, parsing défensif | Fait, testé |
| Indexation d'une image et d'un dossier | Fait, testé, 30 images indexées sur le serveur IUT |
| Recherche regroupée par image | Fait, testé, évaluée sur 10 requêtes |
| Adaptateurs Ollama asynchrones, index ChromaDB | Fait, testé (Bloc B) |
| Interface web Vue, Docker | Sur la branche `dev`, pas encore sur `main` (Bloc C) |
| API FastAPI | Branches `feat/MainRouter` et `feat/ResponsesRouter`, réponses fixes, pas encore reliée à la recherche |
| Reprise d'une indexation interrompue | Pas fait |

Mesures réelles sur le serveur de l'IUT (sorties dans `docs/essais/`) :

- indexation des 30 images : 30 réussies, 0 échec, 1552,6 s au total, soit
  51,8 s par image en moyenne ;
- évaluation sur 10 requêtes écrites depuis `dataset/ground_truth.json` :
  l'image attendue est dans le top 3 pour 9 requêtes sur 10 ;
- temps d'une requête : environ 1,7 s pour la première, puis 0,12 à 0,28 s.

Limites connues : petit échantillon d'évaluation, sensibilité au
vocabulaire (« scooter » contre « moto »), quelques images qui reviennent
souvent en faux positif, pas de seuil de distance exploitable. Détail :
page *Essais et mesures* de la documentation en ligne.

## Équipe

| Membre | Bloc | Responsabilité |
|---|---|---|
| DHESDIN Valentin | A - Perception & Retrieval | Schéma JSON, prompt VLM, parsing, indexation, recherche, dataset, CI (`service/`, `dataset/`, `.github/workflows/`) |
| GOBFERT Frédéric | B - Infra & données | Adaptateurs Ollama VLM/embedding, stockage vectoriel ChromaDB (`ollama_client/`, `storage/`) |
| LEVITRE Mathys | C - Interface & livraison | Interface web, API, Docker, Docker Compose (`frontend/`, `docker/`, `docker-compose.yml`) |

Règle entre blocs : l'interface et l'API n'appellent que les fonctions de
service du Bloc A, et le Bloc A n'utilise le Bloc B qu'à travers ses
interfaces abstraites (`BaseVLM`, `BaseEmbedding`, `BaseVectorIndex`).

Répartition détaillée : `docs/COMMON_REPORT.md`.

## Stack

- **Cœur IA (Bloc A)** : Python 3.10+, Pydantic v2, asyncio, pytest, Ruff
- **Infrastructure & données (Bloc B)** : Ollama (VLM `qwen3-vl:8b-instruct`, embedding `embeddinggemma:latest`), httpx, ChromaDB
- **Interface & livraison (Bloc C)** : Vue 3, Vite, Pinia, FastAPI, Docker / Docker Compose
- **Documentation & CI** : MkDocs Material, GitHub Actions

Les modèles tournent sur le serveur Ollama de l'IUT (ou un Ollama local) : aucun service cloud.

## Structure du dépôt

```text
.
├── src/v_crop_rag/
│   ├── ollama_client/      # adaptateurs Ollama (VLM, embedding, wrapper IUT)
│   ├── storage/            # index vectoriel (interface + ChromaDB)
│   ├── service/            # schéma, prompt, parsing, loader, indexation et recherche (core.py)
│   └── config.py           # variables VCROP_* lues depuis .env, constantes de recherche
├── tests/                  # tests unitaires pytest (faux modèles, sans réseau)
├── dataset/                # 30 images de démonstration + ground_truth.json
├── scripts/                # essais manuels sur le vrai serveur (VLM, indexation, évaluation)
├── data/chroma/            # index ChromaDB créé par l'indexation (non versionné)
├── documentation/          # sources du site MkDocs
├── docs/                   # journaux de bord, suivi de sprint, sorties des essais (docs/essais/)
├── docker/                 # conteneurisation (Bloc C)
└── .github/workflows/      # CI (lint + tests) et déploiement de la doc
```

Flux : dataset → VLM (description JSON) → parsing → embedding par élément
→ ChromaDB → recherche texte → images. Détail : `documentation/technique/architecture.md`.

## Prérequis

- Python >= 3.10
- Pour les appels réels aux modèles : le réseau de l'IUT, ou un Ollama local
  avec `qwen3-vl:8b-instruct` et `embeddinggemma:latest`

## Installation

```bash
git clone https://github.com/dhesdin/sae_s5_vrag_crop.git
cd sae_s5_vrag_crop
```

Le `Makefile` gère l'environnement virtuel et les dépendances :

```bash
make setup
```

Cela crée `.venv/`, met à jour `pip` et installe le projet en mode éditable
avec les dépendances de développement (`pip install -e .[dev]`).

Activez ensuite le venv :

```bash
source .venv/bin/activate
```

## Dataset

`dataset/` contient 30 images récupérées manuellement sur un site de banque
d'images libres de droit, utilisées pour tester le pipeline d'extraction
sans dépendre de données propriétaires.

## Configuration pour l'appel réel à Ollama

La configuration est lue par `src/v_crop_rag/config.py`, depuis
l'environnement ou un fichier `.env` :

```bash
cp .env.example .env
```

| Variable | Valeur par défaut |
|---|---|
| `VCROP_OLLAMA_URL` | serveur Ollama de l'IUT (réseau IUT uniquement) |
| `VCROP_VLM_MODEL` | `qwen3-vl:8b-instruct` |
| `VCROP_EMBEDDING_MODEL` | `embeddinggemma:latest` |

Changer de modèle d'embedding oblige à tout réindexer : les vecteurs de deux
modèles ne sont pas comparables.

Vérification (depuis la racine du dépôt) :

```bash
python scripts/manual_vlm_test.py
```

`manual_dataset_index.py` et `manual_eval_search.py` ne lisent pas encore
`VCROP_OLLAMA_URL` : ils utilisent l'adresse par défaut du wrapper
(`ollama_wrapper_iut.py`, fichier fourni par l'IUT), donc le serveur de l'IUT.

## Utilisation

Indexer les 30 images du dataset (environ 26 minutes sur le serveur de
l'IUT, l'index est écrit dans `data/chroma`) :

```bash
python scripts/manual_dataset_index.py
```

Le script refuse de démarrer si `data/chroma` existe déjà : supprimer le
dossier pour réindexer.

Lancer les 10 requêtes d'évaluation sur cet index :

```bash
python scripts/manual_eval_search.py
```

Depuis Python, `search_image` renvoie une ligne par image, la plus proche en
premier :

```python
results = await search_image("un vélo bleu", embedding, index, k=3)
# [{"image": "bicycle_1.jpg", "distance": 0.459, "matched": "un vélo bleu appuyé contre un mur"}, ...]
```

`distance` est celle de l'élément le plus proche de l'image (plus petite =
plus proche) et `matched` son texte, ce qui explique pourquoi l'image est
remontée.

## Commandes du Makefile

| Commande | Description |
|---|---|
| `make help` | Liste les commandes disponibles |
| `make setup` | Crée le venv et installe les dépendances (`.[dev]`) |
| `make test` | Lance les tests unitaires (`pytest tests/ -q`) |
| `make lint` | Vérifie le code (`ruff check` + `ruff format --check`) |
| `make format` | Reformate le code (`ruff format`) |
| `make clean` | Supprime les `__pycache__` et les caches `.pytest_cache` / `.ruff_cache` |

`test`, `lint` et `format` nécessitent que `make setup` ait été exécuté au préalable.

## Tests

```bash
make test
```

136 tests au 25/11/2026. Ils n'appellent jamais le vrai serveur : le service
est testé avec de faux modèles et un faux index asynchrones.

## Conventions

- **Langue** : code, noms et commentaires en anglais ; contenu métier
  (prompts, valeurs extraites par le VLM, requêtes utilisateur) en français.
- **Python** : typage systématique, Pydantic pour toute donnée qui traverse
  une frontière de module (VLM → parsing → stockage).
- **Git** : une branche par tâche, `make format`, `make lint` et `make test` avant push,
  merge sur `main` après vérification, commits en anglais.
- **Tests** : chaque module a ses tests unitaires ; les scripts qui
  nécessitent le serveur Ollama réel (`scripts/manual_*.py`) restent
  séparés des tests `pytest`, et leurs sorties sont versionnées dans
  `docs/essais/`.

## Documentation

- Site MkDocs (GitHub Pages) : https://dhesdin.github.io/sae_s5_vrag_crop/
- Sources du site : `documentation/` (utilisateur + technique)
- Journaux de bord et suivi de sprint : `docs/`

Prévisualisation locale :

```bash
pip install -e .[docs]
mkdocs serve
```

## Liens utiles

- [gitingest](https://gitingest.com/dhesdin/sae_s5_vrag_crop) - résumé du repo condensé, utile pour donner du contexte à un LLM rapidement
- [gitdiagram](https://gitdiagram.com/dhesdin/sae_s5_vrag_crop) - diagramme d'architecture généré automatiquement à partir du code

Gitdiagram et gitingest sont des outils utiles pour visualiser rapidement l'architecture et le contenu du dépôt. Le contenu est généré automatiquement à partir du code, et non maintenu manuellement

Dépôts sources de ces outils :
- [gitdiagram](https://github.com/ahmedkhaleel2004/gitdiagram)
- [gitingest](https://github.com/coderamp-labs/gitingest)
