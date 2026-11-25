# Génération et déploiement

Cette page décrit l'automatisation du dépôt : l'intégration continue du code
et la publication de cette documentation. Les deux workflows sont dans
`.github/workflows/`.

## Intégration continue (`ci.yml`)

Lancée à chaque push sur `main` et à chaque pull request vers `main`.

1. installation de Python 3.12 et du projet (`pip install -e .[dev]`) ;
2. `ruff check .` puis `ruff format --check .` ;
3. `pytest tests/ -q`.

Une PR dont la CI est rouge n'est pas fusionnée. Les mêmes vérifications se
lancent en local avant de pousser :

```bash
make format
make lint
make test
```

Les tests n'appellent jamais le vrai serveur Ollama : les adaptateurs sont
testés avec des mocks et le service avec de faux modèles. Les essais réels
passent par les scripts de `scripts/`, à lancer à la main sur le réseau de
l'IUT, et leurs sorties sont versionnées dans `docs/essais/`.

La CI ne teste que Python 3.12, alors que le projet annonce Python 3.10 et
plus (`pyproject.toml`).

## Documentation en ligne (`docs.yml`)

Le site est construit avec **MkDocs Material**.

- Sources : `documentation/` (configuration dans `mkdocs.yml`).
- Déploiement : à chaque push sur `main` qui touche `documentation/` ou
  `mkdocs.yml`, le workflow lance `mkdocs gh-deploy`, qui construit le site
  et le pousse sur la branche `gh-pages`.
- Adresse : <https://dhesdin.github.io/sae_s5_vrag_crop/>

Prévisualiser en local avant de pousser :

```bash
pip install -e .[docs]
mkdocs serve        # http://127.0.0.1:8000
```

`mkdocs build --strict` permet de vérifier qu'aucun lien interne n'est cassé.

## Ce qui n'est pas sur le site

Le site sert à utiliser et comprendre le projet. Le suivi du travail reste
dans `docs/` : sprints (`docs/monitoring/`), journaux de bord de chaque
membre (`*_REPORT.md`) et sorties brutes des essais (`docs/essais/`).
