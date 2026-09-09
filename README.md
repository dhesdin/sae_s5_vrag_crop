# V-CROP RAG

SAE V-CROP RAG - recherche d'images par éléments constitutifs.

## Prérequis

- Python >= 3.10

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
