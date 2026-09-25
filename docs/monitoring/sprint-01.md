#### Sprint 1 : Pipeline d'Indexation & Recherche Vectorielle (V-CROP RAG)

**Objectif du sprint**

L'objectif de ce sprint est de passer du socle technique développé lors du Sprint 0 à une première chaîne fonctionnelle permettant d'analyser les images du dataset, de transformer les informations visuelles extraites en représentations vectorielles, de les stocker dans un index persistant et d'effectuer une première recherche à partir d'une requête utilisateur.

Le sprint doit également permettre de commencer l'intégration entre les différents blocs de l'application : extraction visuelle, infrastructure de stockage/recherche et interface utilisateur.

**User Stories**

* US 1.1.1 *(Bloc A / Bloc B - ValentinD / FredericG)* : En tant que développeur, je peux générer les embeddings correspondant aux éléments extraits d'une image en utilisant l'adaptateur Embedding/Ollama développé lors du Sprint 0.

  Le pipeline d'indexation ne doit pas dépendre directement de l'API HTTP d'Ollama mais uniquement de l'interface d'embedding fournie par le Bloc B.

* US 1.1.2 *(Bloc B - FredericG)* : En tant que développeur, je dispose d'une couche d'accès à **ChromaDB** permettant de créer et utiliser un index vectoriel persistant sans que les autres composants de l'application dépendent directement de l'implémentation de ChromaDB.

  Cette couche doit au minimum permettre :
  - l'ajout d'un vecteur accompagné de ses métadonnées ;
  - la recherche des `k` vecteurs les plus proches d'un vecteur donné ;
  - la persistance de l'index entre deux exécutions de l'application ;
  - l'identification de l'image et de l'élément visuel associés à chaque vecteur.

* US 1.1.3 *(Bloc A / Bloc B - ValentinD / FredericG)* : En tant que développeur, je peux indexer les éléments visuels extraits des images du dataset dans ChromaDB.

  Pour chaque élément indexé, les métadonnées nécessaires à son exploitation ultérieure doivent être conservées, notamment l'identifiant ou le chemin de l'image source, le type d'élément visuel et les informations nécessaires à sa localisation ou à son affichage.

* US 1.1.4 *(Bloc B - FredericG)* : En tant que développeur, je valide les adaptateurs Ollama développés lors du Sprint 0 avec le serveur réel de l'IUT.

  Un test d'intégration doit permettre de vérifier :
  - l'accès au serveur Ollama ;
  - l'utilisation réelle du modèle VLM ;
  - la production d'une réponse JSON exploitable ;
  - l'utilisation réelle du modèle d'embedding ;
  - la récupération d'un vecteur valide.

* US 1.1.5 

* US 1.1.6 

* US 1.1.7 

* US 1.1.8 

**Livrables / DoR & DoD**

| Livrable | Statut | Preuve |
|---|---|---|
| Appel réel du VLM via le serveur Ollama | À faire | Test d'intégration Ollama + réponse JSON valide |
| Appel réel du modèle d'embedding via Ollama | À faire | Test d'intégration + vérification du vecteur retourné |
| Interface générique de stockage vectoriel | À faire | Interface / abstraction du vector store + tests |
| Implémentation ChromaDB du stockage vectoriel | À faire | Adaptateur ChromaDB + tests |
| Persistance locale de l'index ChromaDB | À faire | Index conservé entre deux exécutions |
| Stockage des métadonnées associées aux embeddings | À faire | Vérification des documents et métadonnées dans ChromaDB |
| Recherche vectorielle `query(vector, k)` | À faire | Tests unitaires et test sur l'index réel |
| Première recherche texte → embedding → résultats | À faire | Requête de démonstration retournant les images correspondantes |
| Tests unitaires du Vector Store | À faire | Tests avec stockage isolé/temporaire |