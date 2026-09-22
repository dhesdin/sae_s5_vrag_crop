# Architecture

Le projet est découpé en trois blocs, avec un propriétaire par périmètre de
code (voir `docs/COMMON_REPORT.md` pour la répartition complète) :

- **Bloc A - Perception & Retrieval** (`service/`, schéma JSON, prompt VLM)
- **Bloc B - Infra & données** (`ollama_client/`, `storage/`)
- **Bloc C - Interface & livraison** (`Dockerfile`, `docker-compose.yml`,
  CI, `tests/`)

> Le dataset de démonstration (`dataset/`) a été repris par le Bloc A,
> Bloc C n'étant pas disponible sur ce point — voir le journal de bord
> du 09-10/09/2026.

Cette page rassemble la vue d'ensemble ; chaque section ci-dessous est
maintenue par le bloc concerné.

## Bloc A - Perception & Retrieval

Responsable : DHESDIN Valentin.

### Rôle

Extraire une description structurée de chaque image du dataset via un VLM,
puis permettre de retrouver une image à partir des éléments qu'elle contient.

### Ce que reçoit ce bloc

Du Bloc B : un client VLM et un client d'embedding utilisables via deux
interfaces abstraites (`src/v_crop_rag/ollama_client/base.py`) :

- `BaseVLM.generate(prompt, image) -> str`
- `BaseEmbedding.embed(text) -> list[float]`

Implémentées côté Bloc B par `OllamaVLM` et `OllamaEmbedding`
(`ollama_client/vlm.py`, `ollama_client/embedding.py`), sur la base du
wrapper `ollama_wrapper_iut.py`.

### Ce que livre ce bloc

Au Bloc C : le format de sortie JSON par image, défini par le schéma
[`ImageDescription`](schema-donnees.md) - voir aussi
[Comprendre un résultat](../utilisateur/resultats.md).

### Composants (état actuel)

| Composant                                                                 | Fichier                     | État                                                                          |
| ------------------------------------------------------------------------- | --------------------------- | ----------------------------------------------------------------------------- |
| Schéma d'extraction (`ImageDescription`, `DetectedObject`, `BoundingBox`) | `service/schemas.py`        | Implémenté, testé                                                             |
| Prompt d'extraction VLM                                                   | `service/prompts.py`        | Implémenté, testé, cohérence avec le schéma vérifiée en CI                    |
| Listing du dataset                                                        | `service/dataset_loader.py` | Implémenté, testé                                                             |
| Pipeline d'indexation (orchestration : listing + appel VLM par image)     | `service/core.py`           | Non implémenté                                                                |
| Parsing défensif de la réponse VLM                                        | `service/parsing.py`        | Non implémenté (code prêt, bloqué par A4 — validation sur réponse VLM réelle) |
| Gestion des embeddings par élément détecté                                | `service/utils.py`          | Non implémenté                                                                |
| Fonction de recherche par embedding                                       | `service/utils.py`          | Non implémenté                                                                |
| Orchestration complète du pipeline                                        | `service/core.py`           | Non implémenté                                                                |

Détail du flux prévu une fois le pipeline complet : voir
[Indexer un dossier d'images](../utilisateur/indexation.md) et
[Rechercher une image](../utilisateur/recherche.md). Les choix de conception
propres à ce bloc sont détaillés dans [Choix techniques](choix-techniques.md).

### Ce que ce bloc ne touche jamais

Le wrapper Ollama, la configuration Docker, le stockage bas niveau (ChromaDB
en direct) : ces éléments relèvent du Bloc B.

## Bloc B - Infra & données

<!-- TODO (Frédéric) : architecture des adaptateurs Ollama (VLM, LLM, embedding)
     et du stockage vectoriel (storage/). -->

## Bloc C - Interface & livraison

<!-- TODO (Mathys) : architecture de l'interface, conteneurisation Docker,
     CI/CD. -->
