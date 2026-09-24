# V-CROP RAG

SAE V-CROP RAG - recherche d'images par éléments constitutifs.

## Prérequis

- Python >= 3.10

## Liens utiles

- [gitingest](https://gitingest.com/dhesdin/sae_s5_vrag_crop) - résumé du repo condensé, utile pour donner du contexte à un LLM rapidement
- [gitdiagram](https://gitdiagram.com/dhesdin/sae_s5_vrag_crop) - diagramme d'architecture généré automatiquement à partir du code

Gitdiagram et gitingest sont des outils utiles pour visualiser rapidement l'architecture et le contenu du dépôt. Le contenu est généré automatiquement à partir du code, et non maintenu manuellement

Dépôts sources de ces outils :
- [gitdiagram](https://github.com/ahmedkhaleel2004/gitdiagram)
- [gitingest](https://github.com/coderamp-labs/gitingest)

## Installation

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
