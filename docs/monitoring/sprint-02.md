#### Sprint 2 - Orchestration et pipeline complet V-CROP RAG

**Objectif du sprint**

L’objectif principal est d'assembler les briques déjà développées afin d'obtenir un pipeline fonctionnel complet : image → VLM → parsing → embeddings → ChromaDB → recherche → résultat exploitable.

**User Stories**
* US 2.1.1 (Bloc B - FredericG) : En tant que développeur, je peux conserver avec chaque embedding les métadonnées permettant d'identifier et d'exploiter le résultat lors d'une recherche.
Les métadonnées doivent notamment permettre de retrouver :
- l'identifiant ou le chemin de l'image source ;
- le type d'élément indexé ;
- son libellé ou sa description ;
- sa bounding box lorsqu'elle existe ;
- toute information nécessaire à l'affichage ou à la justification du résultat.

* US 2.1.2 (Bloc B - FredericG) : En tant que développeur, je peux éviter de retraiter inutilement une image déjà présente dans l'index.
Lors d'une nouvelle exécution du pipeline, le système doit pouvoir déterminer qu'une image a déjà été indexée et éviter de relancer inutilement le VLM et la génération des embeddings.
Le mécanisme choisi doit rester compatible avec la persistance locale de ChromaDB.

* US 2.1.3 (Bloc B - FredericG) : En tant que développeur, je rends les échanges avec Ollama plus robustes et adaptés à l'intégration applicative.
Les adaptateurs doivent notamment gérer :
- les timeouts ;
- les erreurs HTTP ;
- l'indisponibilité du serveur Ollama ;
- l'indisponibilité d'un modèle ;
- les réponses invalides ou incomplètes.

* US 2.1.4 (Bloc B - FredericG / Bloc C - MathysL) : En tant qu'utilisateur, je peux envoyer une requête depuis l'application web et recevoir les résultats produits par le moteur de recherche vectorielle.

Une API doit assurer la liaison entre l'interface utilisateur et le pipeline de recherche.

L'API doit :
- recevoir la requête utilisateur ;
- transmettre cette requête à l'orchestrateur ;
- récupérer les résultats du moteur ;
- retourner une réponse structurée exploitable par le frontend.

* US 2.1.5 (Bloc A - ValentinD) : En tant que développeur, je peux indexer un dossier d'images en un seul appel, avec une politique d'erreurs explicite.
Le pipeline parcourt le dataset, saute les images déjà indexées (grâce à l'index fourni par le Bloc B), décide quoi faire d'une image en échec (sauter ou arrêter), et permet de détecter une image restée à moitié indexée.

* US 2.1.6 (Bloc A - ValentinD) : En tant qu'utilisateur, je peux obtenir, pour une requête texte, une liste d'images classées avec l'élément qui justifie chaque résultat.
La requête est transformée en embedding avec le même modèle qu'à l'indexation, comparée aux éléments indexés, puis les résultats sont regroupés par image (image, élément, description, score, bounding box lorsqu'elle existe).

*US 2.1.5 et 2.1.6 ajoutées par le Bloc A : l'orchestration et la recherche du moteur n'étaient pas couvertes par la répartition initiale du sprint.*


**Livrables / DoR & DoD**

*Mise à jour du 10/11/2026 (Bloc A). Le travail en cours est sur la branche `dhesdin/index-single-image`.*

| Livrable | Statut | Preuve |
|---|---|---|
| Stockage des métadonnées associées à chaque embedding | En cours | Vérification dans ChromaDB de la présence de l'identifiant ou chemin de l'image source, du type d'élément, de sa description et de sa bounding box lorsqu'elle existe. **Bloc A** : `index_image` (`service/core.py`, branche non mergée) construit pour chaque entrée l'image source (`image`), le type (`type` : object / background / main_subject), le texte embeddé (`text`), le libellé (`label`, objets) et la position, et la bounding box (`has_bbox` + `bbox_*` via `bbox_to_metadata`). `tests/test_core.py` vérifie que chaque métadonnée est acceptée par `validate_metadata` de ChromaDB. Essai réel du 10/11 : les 11 entrées d'une image sont bien présentes dans l'index (ids retournés par `query`). Vérification du contenu des métadonnées dans la base réelle : à faire |
| Association fiable entre un embedding et son élément visuel d'origine | En cours | Tests montrant qu'un résultat de recherche permet de retrouver l'image et l'élément visuel correspondants. **Bloc A** : ids déterministes `{image}:{i}` (objets), `{image}:background`, `{image}:main`, associés aux métadonnées `image` et `type`. `tests/test_core.py` vérifie les ids, l'ordre d'écriture et le saut d'un objet vide sans décaler les ids suivants. Essai réel du 10/11 : `market_0:0` à `market_0:8`, `market_0:background` et `market_0:main` sont retournés par `query`. Liaison id vers libellé vérifiée sur la base réelle : à faire. Le test de bout en bout dépend de la fonction de recherche (à faire) |
| Conservation des métadonnées après redémarrage de l'application | À faire | Vérification sur l'index ChromaDB persistant après arrêt puis relance |
| Détection d'une image déjà indexée | À faire | Test vérifiant qu'une image déjà présente dans l'index est reconnue lors d'une nouvelle exécution. **Bloc A** : `index_image` écrit l'entrée `{image}:main` en dernier, comme marqueur d'image complète (`tests/test_core.py` : le dernier `add` est `:main`, aucun `add` si un embedding échoue). La détection elle-même dépend de `exists(id)` côté Bloc B, absent de `storage/base.py` et de `storage/chroma.py` dans l'état consulté. Constat de l'essai du 10/11 : relancer `index_image` sur la même image semble ne pas remplacer les entrées existantes (voir la ligne « Essais réels »), ce qui rend nécessaire une suppression par image ou un `upsert` côté Bloc B |
| Cache / anti-réindexation | À faire | Deux indexations successives du même jeu d'images sans nouvel appel inutile au VLM ni au modèle d'embedding. **Bloc A** : la boucle sur le dataset qui saute les images dont `{image}:main` existe n'est pas écrite |
| Compatibilité du cache avec la persistance ChromaDB | À faire | Vérification après redémarrage que les images déjà indexées ne sont pas retraitées |
| Gestion des timeouts lors des appels Ollama | À faire | Tests simulant un dépassement du temps d'attente avec erreur contrôlée. **Constat Bloc A (essai du 10/11)** : le premier appel au VLM a dépassé le délai par défaut de 60 s du wrapper (`httpx.ReadTimeout`) et a été remonté comme `OllamaConnectionError` « Impossible de joindre Ollama », alors que le serveur répondait. Avec un délai augmenté, le même appel a pris 24,4 s |
| Gestion des erreurs HTTP Ollama | À faire | Tests avec réponses HTTP invalides ou erreurs serveur |
| Gestion de l'indisponibilité du serveur Ollama | À faire | Test avec serveur Ollama arrêté et message d'erreur explicite |
| Gestion d'un modèle Ollama indisponible ou inexistant | À faire | Test avec un nom de modèle invalide et gestion propre de l'erreur |
| Gestion des réponses invalides ou incomplètes produites par les modèles | À renforcer | Validation Pydantic / parsing défensif + tests sur réponses mal formées ou champs manquants. **Bloc A** : `parse_vlm_response` (`VLMResponseParsingError`, 11 tests, mergé sur main). `index_image` refuse un `main_subject` vide ou blanc par un `ValueError` (branche, choix provisoire, couvert par 2 tests de `tests/test_core.py`) et propage `VLMResponseParsingError` sans écrire dans l'index (test). Reste : valider `main_subject` non vide dans le schéma, et définir la politique d'erreurs de la boucle d'indexation |
| API de recherche exposée au frontend | À faire | Endpoint permettant de transmettre une requête utilisateur au moteur de recherche |
| Validation de la requête reçue par l'API | À faire | Modèle Pydantic + tests sur requêtes valides, invalides et champs manquants |
| Transmission de la requête API vers l'orchestrateur | À faire | Test d'intégration vérifiant que l'endpoint appelle correctement le moteur de recherche. **Dépendance Bloc A** : la fonction de recherche appelée par l'API (service) n'est pas commencée |
| Retour structuré des résultats de recherche | À faire | Réponse JSON contenant les informations nécessaires au frontend : image, élément, description, score et métadonnées disponibles. **Dépendance Bloc A** : ce contenu est produit par la fonction de recherche et de ranking (non commencée) |
| Gestion des erreurs du moteur dans l'API | À faire | Réponses HTTP adaptées en cas d'erreur Ollama, erreur de validation ou indisponibilité du moteur |
| Intégration frontend → API → moteur | À faire | Une requête saisie dans l'interface déclenche réellement une recherche et retourne les résultats |
| Tests d'intégration de l'API de recherche | À faire | Tests couvrant requête valide, absence de résultat, erreur moteur et données invalides |
| (Bloc A) Indexation d'une image : `index_image` | Fait (fusion en cours) | `service/core.py`, branche `dhesdin/index-single-image` : prompt → VLM → parsing → un embedding par objet, par décor et par sujet principal → écriture, marqueur `{image}:main` en dernier. Asynchrone (`async def`, `await`), compatible avec les interfaces de `main` (fusion de `main` dans la branche). `tests/test_core.py` : 12 tests avec faux VLM / faux embedder / faux index (ordre d'écriture, valeur retournée, objet vide sauté, échec d'embedding sans écriture, réponse non JSON, `main_subject` vide, type de `image_path`, position exclue du texte, métadonnées de bbox, validité Chroma, décor vide). Essai réel sur le serveur IUT le 10/11 : une image indexée (11 entrées). Reste : pull request vers `main`, CI |
| (Bloc A) Boucle d'indexation du dataset + politique d'erreurs | À faire | Parcours de `list_dataset_images()`, saut des images déjà indexées, décision sauter/arrêter par type d'erreur, compte rendu du run. Dépend de `exists(id)` (Bloc B). Estimation : environ 25 s par image, soit 13 à 14 minutes pour 30 images (une seule image mesurée) |
| (Bloc A) Fonction de recherche et ranking | À faire | Embedding de la requête avec le modèle d'indexation, `query(vector, k)`, regroupement des résultats par image, score agrégé, retour structuré. Non commencée. Un `query` brut a été exécuté sur l'index réel dans le script d'essai (ids et distances), sans regroupement par image ni évaluation de la pertinence |
| (Bloc A) Essais réels sur le serveur IUT | En cours | Essai du 10/11/2026 (`scripts/manual_index_test.py`, sortie dans `docs/essais/essai-2.md`). Embedding (`embeddinggemma:latest`) : dimension 768, norme 0,9999999. Appel direct du VLM (`qwen3-vl:8b-instruct`) : 24,4 s, JSON conforme au schéma. `index_image` : 11 entrées en 26,4 s (9 objets, décor, sujet principal). Relance sur la même image : 8 entrées en 28,2 s (le VLM n'est pas déterministe) ; les distances des ids déjà présents sont inchangées, donc Chroma semble ignorer les `add` sur un id existant (hypothèse à confirmer car j'ai fait qu'un seul essai). Bounding boxes : 1 objet sur 9 en possède une, Après analyse de l'image et des positions je pense fortement que l'unité est en pixel. Reste : une seule image testée, indexation des 30 images, évaluation de la recherche |
| Non-régression des tests existants | À maintenir | Tous les tests déjà présents dans le projet doivent continuer à passer. 124 tests passent sur la branche `dhesdin/index-single-image` (commit `1782d14`, `main` intégré par fusion). CI de la pull request : à vérifier |
| Qualité du code | À maintenir | Ruff / lint et conventions du projet respectés. Lint propre sur la branche au même commit |
| Tests des scripts dans l'environnement IUT (suite au passage en asynchrone) | En cours | Tests passent. **Bloc A** : `scripts/manual_index_test.py` est asynchrone et a été exécuté sur le serveur IUT le 10/11 (sortie versionnée dans `docs/essais/`) |