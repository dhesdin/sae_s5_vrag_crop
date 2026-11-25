#### Sprint 3 - Recherche, évaluation et intégration V-CROP RAG

**Objectif du sprint**

Semaine du 23/11/2026. L'objectif est de rendre la recherche utilisable et mesurée : fonction de recherche testée, dataset complet indexé sur le serveur de l'IUT, résultats évalués sur des requêtes réelles, et contrat de réponse défini pour l'API et le frontend.

**User Stories**

- US 3.1.1 (Bloc A - ValentinD) : En tant que développeur, je peux vérifier par des tests unitaires que la recherche renvoie une ligne par image, classée par distance, limitée à k, avec des gardes sur les entrées invalides.

- US 3.1.2 (Bloc A - ValentinD) : En tant que développeur, je peux indexer les 30 images du dataset en un seul appel sur le serveur de l'IUT et conserver une sortie versionnée de l'essai (images indexées, images en échec, durées).

- US 3.1.3 (Bloc A - ValentinD) : En tant qu'utilisateur, je peux interroger le dataset indexé avec 10 requêtes texte et mesurer si l'image attendue apparaît dans les 3 premiers résultats.
  Les 10 requêtes sont écrites depuis `dataset/ground_truth.json` (`scripts/manual_eval_search.py`). Le facteur 10 (`k * ELEMENTS_PER_IMAGE`) reste une hypothèse : le nombre de doublons d'image parmi les éléments renvoyés n'a pas été compté.

- US 3.1.4 (Bloc A - ValentinD / Bloc C - MathysL) : En tant que développeur, je dispose d'un contrat de réponse de la recherche (liste de `{image, distance, matched}`) utilisable par l'API et le frontend.

- US 3.1.5 (Bloc B - FredericG) : à compléter par FredericG.
  Pistes issues des points de coordination, non confirmées : `exists(id)`, `upsert` ou suppression par image, métrique cosinus.

- US 3.1.6 (Bloc C - MathysL) : à compléter par MathysL.
  Pistes issues des points de coordination, non confirmées : branchement de l'API sur la recherche, tests de temps.

**Livrables / DoR & DoD**

_Mise à jour du 25/11/2026 (Bloc A). `search_image` et ses tests sont mergés sur main._

| Livrable                                                | Statut      | Preuve |
| ------------------------------------------------------- | ----------- | ------ |
| Fonction `search_image` (recherche regroupée par image) | Fait        | `service/core.py`, mergée sur main, CI verte. Gardes, embedding de la requête, `index.query` avec `k * ELEMENTS_PER_IMAGE` éléments (constante dans `config.py`, ajoutée avec l'accord de Frederic), regroupement par image, tri par distance, coupe à k. |
| Tests unitaires de `search_image`                       | Fait        | `tests/test_core.py` : 9 tests avec faux embedding et faux index (une ligne par image, élément le plus proche conservé, coupe à k, `k * ELEMENTS_PER_IMAGE` demandé à l'index, gardes, troncature de la requête). 136 tests au total au `make test`. |
| Indexation des 30 images sur le serveur IUT             | Fait        | `scripts/manual_dataset_index.py`, sortie dans `docs/essais/essai-3-index-dataset.md` : 30 indexées, 0 échec, 1552,6 s au total (51,8 s par image en moyenne, min 35,2 s, max 73,1 s). L'estimation de départ de 13 minutes était fausse. |
| Évaluation sur 10 requêtes                              | Fait        | `scripts/manual_eval_search.py`, sorties dans `docs/essais/essai-4-evaluation.md` à `essai-6-diagnostic-lampadaire.md` : image attendue dans le top 3 pour 9 requêtes sur 10. Temps par requête : environ 1,7 s pour la première, 0,12 à 0,28 s ensuite. Limites : "un scooter" (vocabulaire, "un motocycle" retrouve 2 images sur 2) et "réverbère" (non expliqué, "un lampadaire noir" le retrouve au rang 1). |
| Contrat de réponse de la recherche                      | À faire     | Format `{image, distance, matched}` à définir avec MathysL et à documenter, puis à relier aux branches `feat/MainRouter` et `feat/ResponsesRouter`. |
| Lignes Bloc B (FredericG)                               | À compléter | à compléter par FredericG |
| Lignes Bloc C (MathysL)                                 | À compléter | à compléter par MathysL |