#### Sprint 2 — Orchestration et pipeline complet V-CROP RAG

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



**Livrables / DoR & DoD**

| Livrable | Statut | Preuve |
|---|---|---|
| Stockage des métadonnées associées à chaque embedding | À faire | Vérification dans ChromaDB de la présence de l'identifiant ou chemin de l'image source, du type d'élément, de sa description et de sa bounding box lorsqu'elle existe |
| Association fiable entre un embedding et son élément visuel d'origine | À faire | Tests montrant qu'un résultat de recherche permet de retrouver l'image et l'élément visuel correspondants |
| Conservation des métadonnées après redémarrage de l'application | À faire | Vérification sur l'index ChromaDB persistant après arrêt puis relance |
| Détection d'une image déjà indexée | À faire | Test vérifiant qu'une image déjà présente dans l'index est reconnue lors d'une nouvelle exécution |
| Cache / anti-réindexation | À faire | Deux indexations successives du même jeu d'images sans nouvel appel inutile au VLM ni au modèle d'embedding |
| Compatibilité du cache avec la persistance ChromaDB | À faire | Vérification après redémarrage que les images déjà indexées ne sont pas retraitées |
| Gestion des timeouts lors des appels Ollama | À faire | Tests simulant un dépassement du temps d'attente avec erreur contrôlée |
| Gestion des erreurs HTTP Ollama | À faire | Tests avec réponses HTTP invalides ou erreurs serveur |
| Gestion de l'indisponibilité du serveur Ollama | À faire | Test avec serveur Ollama arrêté et message d'erreur explicite |
| Gestion d'un modèle Ollama indisponible ou inexistant | À faire | Test avec un nom de modèle invalide et gestion propre de l'erreur |
| Gestion des réponses invalides ou incomplètes produites par les modèles | À renforcer | Validation Pydantic / parsing défensif + tests sur réponses mal formées ou champs manquants |
| API de recherche exposée au frontend | À faire | Endpoint permettant de transmettre une requête utilisateur au moteur de recherche |
| Validation de la requête reçue par l'API | À faire | Modèle Pydantic + tests sur requêtes valides, invalides et champs manquants |
| Transmission de la requête API vers l'orchestrateur | À faire | Test d'intégration vérifiant que l'endpoint appelle correctement le moteur de recherche |
| Retour structuré des résultats de recherche | À faire | Réponse JSON contenant les informations nécessaires au frontend : image, élément, description, score et métadonnées disponibles |
| Gestion des erreurs du moteur dans l'API | À faire | Réponses HTTP adaptées en cas d'erreur Ollama, erreur de validation ou indisponibilité du moteur |
| Intégration frontend → API → moteur | À faire | Une requête saisie dans l'interface déclenche réellement une recherche et retourne les résultats |
| Tests d'intégration de l'API de recherche | À faire | Tests couvrant requête valide, absence de résultat, erreur moteur et données invalides |
| Non-régression des tests existants | À maintenir | Tous les tests déjà présents dans le projet doivent continuer à passer |
| Qualité du code | À maintenir | Ruff / lint et conventions du projet respectés |