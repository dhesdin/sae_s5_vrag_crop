# Groupe
DHESDIN Valentin
LEVITRE Mathys
GOBFERT Frédéric

# Sujet
V-CROP RAG - Recherche fine d'images

# Séances du 09/09/26
Durée: 3h00

- Appropriation du sujet
- Etude des documents fournis
- Mise en commun des techniques pour Python
    - toml
    - makefile
- Initialisation du dépôt Git
- Recherches documentaires
- Répartition des rôles :
    - Valentin : Perception + Retrieval
    - Frédéric : Infra & données
    - Mathys : Interface et livraison
- Mis en place d'un Kanban - https://trello.com/invite/b/6aa19eef67d49a9b73af1b6d/ATTIc2fb1fd53a4a7a2d7778fc7794d761a2695EAE08/kanbanvcroprag

# Répartition des rôles

| | **Bloc A - Core IA** | **Bloc B - Infra & données** | **Bloc C - Interface & livraison** |
|---|---|---|---|
| **Fichiers/dossiers possédés** | `service/{core.py,utils.py, *.py}` , prompts VLM, schéma JSON | `ollama_client/`{base.py, vlm.py, llm.py, embedding.py}, `storage/` | `Dockerfile`, `docker-compose.yml`, `.github/workflows/`, `dataset/`, `tests/` |
| **Ce qu'il reçoit de qui** | De **Bloc B** : le client VLM/embedding utilisable (`vlm  --> texte`, `embedding --> vecteur`) | Rien en amont | De **Bloc A** : les fonctions de recherches d'images pour le JSON |
| **Ce qu'il livre à qui** | À **Bloc C** : le format de sortie JSON | À **Bloc A** : les interfaces (classe abstraite) des modèles avec fonction && signatures des méthodes | Rien en aval - bout de chaîne |
| **Ne touche jamais** | Le code du wrapper Ollama, la config Docker, le storage bas niveau (ChromaDB direct) | Le contenu du schéma JSON, le prompt VLM, la logique de ranking/filtrage | La logique d'extraction VLM, le contenu du wrapper Ollama |

