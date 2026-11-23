#### Sprint 3 - Recherche, évaluation et intégration V-CROP RAG

**Objectif du sprint**

Semaine du 23/11/2026. L'objectif est de rendre la recherche utilisable et mesurée : fonction de recherche testée, dataset complet indexé sur le serveur de l'IUT, résultats évalués sur des requêtes réelles, et contrat de réponse défini pour l'API et le frontend.

**User Stories**

- US 3.1.1 (Bloc A - ValentinD) : En tant que développeur, je peux vérifier par des tests unitaires que la recherche renvoie une ligne par image, classée par distance, limitée à k, avec des gardes sur les entrées invalides.

- US 3.1.2 (Bloc A - ValentinD) : En tant que développeur, je peux indexer les 30 images du dataset en un seul appel sur le serveur de l'IUT et conserver une sortie versionnée de l'essai (images indexées, images en échec, durées).

- US 3.1.3 (Bloc A - ValentinD) : En tant qu'utilisateur, je peux interroger le dataset indexé avec 10 requêtes texte et mesurer si l'image attendue apparaît dans les 3 premiers résultats.
  Les images attendues viennent de `dataset/ground_truth.json`. L'évaluation compte aussi les doublons d'image parmi les `k * 10` éléments demandés à l'index, pour vérifier l'hypothèse du facteur 10. Rédaction des 10 requêtes : à confirmer avec MathysL.

- US 3.1.4 (Bloc A - ValentinD / Bloc C - MathysL) : En tant que développeur, je dispose d'un contrat de réponse de la recherche (liste de `{image, distance, matched}`) utilisable par l'API et le frontend.

- US 3.1.5 (Bloc B - FredericG) : à compléter par FredericG.
  Pistes issues des points de coordination, non confirmées : `exists(id)`, `upsert` ou suppression par image, métrique cosinus.

- US 3.1.6 (Bloc C - MathysL) : à compléter par MathysL.
  Pistes issues des points de coordination, non confirmées : branchement de l'API sur la recherche, tests de temps.

**Livrables / DoR & DoD**

_Mise à jour du 23/11/2026 (Bloc A). Le travail en cours est sur la branche `dhesdin/search-image`._

| Livrable                                                | Statut      | Preuve                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Fonction `search_image` (recherche regroupée par image) | En cours    | `service/core.py`, branche non mergée. Gardes, embedding de la requête, `index.query` avec `k * ELEMENTS_PER_IMAGE` éléments (constante dans `config.py`, ajoutée avec l'accord de FredericG), regroupement par image, tri par distance, coupe à k. `make format`, `make lint` et `make test` passent au 23/11 (127 tests, aucun test de `search_image` encore) |
| Tests unitaires de `search_image`                       | À faire     | `tests/test_core.py` avec faux embedding et faux index : une ligne par image, élément le plus proche conservé, coupe à k, `k * ELEMENTS_PER_IMAGE` demandé à l'index, gardes (type, requête vide, k invalide), troncature de la requête                                                                                                                         |
| Indexation des 30 images sur le serveur IUT             | À faire     | `index_dataset` lancé dans un dossier ignoré par git, sortie versionnée dans `docs/essais/` : images indexées, images en échec, durée par image et durée totale (estimation de départ : environ 13 minutes, non mesurée sur 30 images)                                                                                                                          |
| Évaluation sur 10 requêtes                              | À faire     | Pour chaque requête : l'image attendue est-elle dans le top 3, temps de réponse, nombre de doublons d'image parmi les `k * 10` éléments. Résultats versionnés dans `docs/essais/`                                                                                                                                                                               |
| Contrat de réponse de la recherche                      | À faire     | Format `{image, distance, matched}` défini avec MathysL et documenté, à relier aux branches `feat/MainRouter` et `feat/ResponsesRouter`                                                                                                                                                                                                                         |
| Lignes Bloc B (FredericG)                               | À compléter | à compléter par FredericG                                                                                                                                                                                                                                                                                                                                       |
| Lignes Bloc C (MathysL)                                 | À compléter | à compléter par MathysL                                                                                                                                                                                                                                                                                                                                         |
