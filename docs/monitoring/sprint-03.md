#### Sprint 3 - Recherche, évaluation et intégration V-CROP RAG

**Objectif du sprint**

Semaine du 23/11/2026. L'objectif est de rendre la recherche utilisable et mesurée : fonction de recherche testée, dataset complet indexé sur le serveur de l'IUT, résultats évalués sur des requêtes réelles, et contrat de réponse défini pour l'API et le frontend.

**User Stories**

- US 3.1.1 (Bloc A - ValentinD) : En tant que développeur, je peux vérifier par des tests unitaires que la recherche renvoie une ligne par image, classée par distance, limitée à k, avec des gardes sur les entrées invalides.

- US 3.1.2 (Bloc A - ValentinD) : En tant que développeur, je peux indexer les 30 images du dataset en un seul appel sur le serveur de l'IUT et conserver une sortie versionnée de l'essai (images indexées, images en échec, durées).

- US 3.1.3 (Bloc A - ValentinD) : En tant qu'utilisateur, je peux interroger le dataset indexé avec 10 requêtes texte et mesurer si l'image attendue apparaît dans les 3 premiers résultats.
  Les 10 requêtes sont écrites depuis `dataset/ground_truth.json` (`scripts/manual_eval_search.py`). Le facteur 10 (`k * ELEMENTS_PER_IMAGE`) reste une hypothèse : le nombre de doublons d'image parmi les éléments renvoyés n'a pas été compté.

- US 3.1.4 (Bloc A - ValentinD / Bloc C - MathysL) : En tant que développeur, je dispose d'un contrat de réponse de la recherche (liste de `{image, distance, matched}`) utilisable par l'API et le frontend.

- US 3.1.5 (Bloc B - FredericG) : En tant que développeur, je peux relancer l'indexation sans retraiter les images déjà indexées et sans conserver d'entrées obsolètes.
  `exists(id)` dans `BaseVectorIndex` et `ChromaVectorIndex` (détection du marqueur `{image}:main`), et `add` passe en `upsert` : réécrire un id remplace l'entrée au lieu d'être ignoré silencieusement (constat de l'essai IUT du 10/11).

- US 3.1.6 (Bloc C - MathysL) : à compléter par MathysL.
  Pistes issues des points de coordination, non confirmées : branchement de l'API sur la recherche, tests de temps.

- US 3.1.7 (Bloc B - FredericG) : En tant que développeur, je compare les éléments indexés avec une métrique adaptée aux embeddings de texte.
  Vérifier si les vecteurs d'`embeddinggemma` sont normalisés, configurer la collection ChromaDB en `cosine`, normaliser le texte avant embedding, et mesurer l'effet sur l'évaluation des 10 requêtes (US 3.1.3). À livrer avant l'indexation des 30 images (US 3.1.2) pour éviter une réindexation.

- US 3.1.8 (Bloc B - FredericG) : En tant que développeur, je distingue les erreurs Ollama (serveur injoignable, délai dépassé, erreur HTTP, modèle introuvable) afin que le pipeline puisse décider de sauter une image ou de s'arrêter.
  Reprise de l'US 2.1.3, non terminée au sprint 2.

**Livrables / DoR & DoD**

_Mise à jour du 26/11/2026 (Bloc A). `search_image`, `search_images` et la reprise de l'indexation sont mergés sur main (151 tests au `make test`)._

| Livrable | Statut | Preuve |
| -------- | ------ | ------ |
| Fonction `search_image` (recherche regroupée par image) | Fait | `service/core.py`, mergée sur main, CI verte. Gardes, embedding de la requête, `index.query` avec `k * ELEMENTS_PER_IMAGE` éléments (constante dans `config.py`, ajoutée avec l'accord de FredericG), regroupement par image, tri par distance, coupe à k. |
| Tests unitaires de `search_image` | Fait | `tests/test_core.py` : 9 tests avec faux embedding et faux index (une ligne par image, élément le plus proche conservé, coupe à k, `k * ELEMENTS_PER_IMAGE` demandé à l'index, gardes, troncature de la requête). |
| Fonction de service `search_images` | Fait | `service/search_service.py`, mergée (PR #24 et #25). Construit l'embedder et l'index une seule fois au premier appel, chemin de l'index depuis `ROOT_DIR`, `FileNotFoundError` si l'index est absent. 3 tests dans `tests/test_search_service.py`. Vrai appel sur le serveur IUT : « un ananas » donne market_0 et kitchen_0 aux rangs 1 et 2, `k = 30` renvoie les 30 images. |
| Indexation des 30 images sur le serveur IUT | Fait | `scripts/manual_dataset_index.py`, sortie dans `docs/essais/essai-3-index-dataset.md` : 30 indexées, 0 échec, 1552,6 s au total (51,8 s par image en moyenne, min 35,2 s, max 73,1 s). L'estimation de départ de 13 minutes était fausse. |
| Reprise de l'indexation (côté Bloc A) | Fait | `index_dataset` saute les images dont l'entrée `:main` existe (clé `skipped`), grâce à `exists` du Bloc B. Relance sur l'index complet : 30 images sautées en 0,14 s, `docs/essais/essai-7-reprise-indexation.md`. Limite : une image interrompue en cours de route est réindexée par-dessus ses anciens ids, des entrées de l'ancienne description peuvent rester (pas de suppression par image). |
| Évaluation sur 10 requêtes | Fait | `scripts/manual_eval_search.py`, sorties dans `docs/essais/essai-4-evaluation.md` à `essai-6-diagnostic-lampadaire.md` : image attendue dans le top 3 pour 9 requêtes sur 10. Temps par requête : environ 1,7 s pour la première, 0,12 à 0,28 s ensuite. Limites : « un scooter » (vocabulaire, « un motocycle » retrouve 2 images sur 2) et « un réverbère » (non expliqué, « un lampadaire noir » le retrouve au rang 1). |
| Contrat de réponse de la recherche | Défini, branchement à faire | Format {image, distance, matched}. D'après MathysL (26/11) : POST /requests/ avec {"query", "k"} (k à 5 par défaut), réponse en liste de {rank, image, distance, matched} (rang 1 = meilleure image), erreurs en 422 (requête vide ou k invalide), 503 (Ollama injoignable) et 500 (index absent). Branche mlevitre/RequestRouter, non mergée à ce stade. Vraie recherche non testée côté API. |
| (Bloc B) `exists(id)` dans l'interface et l'implémentation ChromaDB | Fait (branche `feature/storage-exists-upsert`) | `storage/base.py`, `storage/chroma.py`. Tests unitaires (id trouvé / absent, types et valeurs invalides) et d'intégration (avant / après `add`, après redémarrage). `FakeIndex` de `tests/test_core.py` adapté avec l'accord de ValentinD. 137 tests passent au 23/11 |
| (Bloc B) `add` en `upsert` | Fait | Test d'intégration : deux `add` sur le même id donnent une seule entrée, avec les dernières métadonnées. |
| (Bloc B) Normalisation des vecteurs `embeddinggemma` | À vérifier | `scripts/embedding_similar_test.py` : norme de chaque vecteur (≈ 1 si normalisé) et similarité cosinus entre textes proches |
| (Bloc B) Collection ChromaDB en métrique cosinus | À faire | Test d'intégration : deux vecteurs de même direction et de normes différentes sont à distance 0. Une collection existante garde sa métrique |
| (Bloc B) Comparaison L2 / cosinus sur les 10 requêtes | À faire (avec Bloc A) | Top 3 de l'évaluation US 3.1.3 avec les deux métriques |
| (Bloc B) Normalisation du texte avant embedding | À faire | Constat du 23/11 : « Un vélo rouge » et « Un vélo rouge » suivi d'espaces donnent des vecteurs différents (écart moyen par composante : 0,006 avec 1 espace, 0,013 avec 2). `OllamaEmbedding.embed` normalise les espaces ; test unitaire |
| (Bloc B) Délai d'attente Ollama configurable | À faire | Constat IUT du 10/11 : premier appel VLM > 60 s (`httpx.ReadTimeout`), même appel en 24,4 s avec un délai augmenté |
| (Bloc B) Exceptions Ollama distinctes | À faire | Délai dépassé, serveur injoignable, erreur HTTP, modèle introuvable. |
| (Bloc B / Bloc A) Politique d'erreurs | À définir | Avec les nouvelles exceptions : par exemple sauter l'image si le délai est dépassé, arrêter si le serveur est injoignable ou le modèle introuvable |
| Lignes Bloc C (MathysL) | À compléter | à compléter par MathysL |