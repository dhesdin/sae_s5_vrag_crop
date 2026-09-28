# V-CROP RAG

SAE V-CROP RAG - recherche d'images par éléments constitutifs.

## Comment ça fonctionne

Un utilisateur tape une requête comme « parasol rouge » et récupère les
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
      "state": "pliee",
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
   contraignant une sortie JSON strict (`service/prompts.py`).
2. La réponse brute est validée par un parsing défensif
   (`service/parsing.py`) : JSON invalide, champs manquants ou réponse
   entourée de texte libre sont gérés sans faire planter le pipeline.
3. Chaque élément détecté est vectorisé individuellement par le modèle
   d'embedding (`embeddinggemma:latest`), pas l'image entière.
4. Les vecteurs sont stockés dans ChromaDB avec leurs métadonnées (image
   source, type d'élément, position).
5. À la recherche, la requête texte est vectorisée de la même façon et
   comparée aux vecteurs indexés ; les images correspondantes sont
   retournées classées par pertinence.

Le pipeline ci-dessus décrit l'architecture cible. L'orchestration
bout-en-bout (`service/core.py`) est en cours de développement - voir
`docs/monitoring/sprint-01.md` pour l'état d'avancement réel. Détail
technique complet : `documentation/technique/architecture.md`.

## Équipe

| Membre | Bloc | Responsabilité |
|---|---|---|
| DHESDIN Valentin | A - Perception & Retrieval | Schéma JSON, prompt VLM, parsing, pipeline d'indexation, recherche, dataset, CI (`service/`, `dataset/`, `.github/workflows/`) |
| GOBFERT Frédéric | B - Infra & données | Adaptateurs Ollama VLM/embedding, stockage vectoriel ChromaDB (`ollama_client/`, `storage/`) |
| LEVITRE Mathys | C - Interface & livraison | Interface web complète, Docker, Docker Compose (`frontend/`, `docker/`, `docker-compose.yml`) |

Répartition détaillée : `docs/COMMON_REPORT.md`.

## Stack

- **Cœur IA (Bloc A)** : Python 3.10+, Pydantic v2, pytest, Ruff
- **Infrastructure & données (Bloc B)** : Ollama (VLM `qwen3-vl:8b-instruct`, embedding `embeddinggemma:latest`), ChromaDB
- **Interface & livraison (Bloc C)** : Vue 3, Docker / Docker Compose
- **Documentation & CI** : MkDocs Material, GitHub Actions

Tout passe par Ollama en local, sur le serveur de l'IUT — aucun service cloud.

## Structure du dépôt

```text
.
├── src/v_crop_rag/
│   ├── ollama_client/      # adaptateurs Ollama (VLM, embedding, wrapper IUT)
│   ├── storage/            # index vectoriel (interface + ChromaDB)
│   └── service/            # schéma, prompt, parsing, loader, pipeline (core.py à venir)
├── tests/                  # tests unitaires pytest
├── dataset/                # 30 images de démonstration + ground_truth.json
├── scripts/                # scripts manuels (appel VLM réel, debug prompt)
├── documentation/          # sources du site MkDocs
├── docs/                   # journaux de bord + suivi de sprint
├── docker/                 # conteneurisation (Bloc C)
└── .github/workflows/      # CI (lint + tests) et déploiement de la doc
```

Flux prévu : dataset → VLM (description JSON) → parsing → embedding par élément
→ ChromaDB → recherche texte → images. Détail : `documentation/technique/architecture.md`.

## Prérequis

- Python >= 3.10

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

- **Serveur** : l'URL est codée en dur dans
  `src/v_crop_rag/ollama_client/ollama_wrapper_iut.py` (fichier fourni par l'IUT),
  accessible uniquement depuis le réseau de l'IUT.
- **Modèle VLM** : `qwen3-vl:8b-instruct`
- **Modèle d'embedding** : `embeddinggemma:latest`
- **Vérification** (depuis la racine du dépôt) :

```bash
python scripts/manual_vlm_test.py
```

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

## Conventions

- **Langue** : code, noms et commentaires en anglais ; contenu métier
  (prompts, valeurs extraites par le VLM, requêtes utilisateur) en français.
- **Python** : typage systématique, Pydantic pour toute donnée qui traverse
  une frontière de module (VLM → parsing → stockage).
- **Git** : une branche par tâche, `make lint && make test` avant merge,
  merge sur `main` après vérification, commits en anglais.
- **Tests** : chaque module a ses tests unitaires ; les scripts qui
  nécessitent le serveur Ollama réel (`scripts/manual_vlm_test.py`) restent
  séparés des tests `pytest`.

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
