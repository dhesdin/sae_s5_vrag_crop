# Déploiement applicatif (Docker)

Le déploiement de l'application complète (interface, API, base vectorielle)
relève du Bloc C (LEVITRE Mathys).

## État actuel

Sur `main`, `docker/Dockerfile` et `docker-compose.yml` existent mais sont
vides. Une première version se trouve sur la branche `dev` (PR #14, fusionnée
dans `dev` le 08/10/2026) :

- **`docker/Dockerfile`** : image `node:lts-alpine` qui installe les
  dépendances du frontend, le construit (`npm run build`) et sert le
  résultat avec `http-server` sur le port **8080** ;
- **`docker-compose.yml`** : deux services, `frontend` (construit depuis le
  Dockerfile, port 8080) et `chromadb` (image officielle, port 8000, volume
  `chroma_data`).

Avec cette version, depuis la branche `dev` :

```bash
docker compose up --build
# interface sur http://localhost:8080
```

## Ce qui manque pour une application complète

- un service pour l'**API** FastAPI (branches `feat/MainRouter`,
  `feat/ResponsesRouter`), qui appellera `search_image` ;
- l'accès de l'API au serveur Ollama (réseau de l'IUT, ou Ollama local) pour
  embedder les requêtes ;
- le dossier `dataset/` monté dans le conteneur, pour afficher les images
  renvoyées par la recherche ;
- un choix sur ChromaDB : le moteur Python utilise aujourd'hui un ChromaDB
  **embarqué** (`PersistentClient` sur `data/chroma`), pas le service
  `chromadb` du compose.

Ce dernier point est à trancher entre les blocs B et C.

<!-- TODO (Mathys) : compléter avec la procédure réelle une fois le
     déploiement fusionné sur main. -->
