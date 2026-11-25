# Choix techniques

Cette page regroupe les décisions techniques argumentées par bloc, extraites
du journal de bord de chacun.

## Bloc A - Perception & Retrieval

Responsable : DHESDIN Valentin.

### Schéma : composition plutôt qu'héritage

`ImageDescription`, `DetectedObject` et `BoundingBox` sont reliés par
**composition**, pas par héritage : aucune des trois classes n'est une
spécialisation d'une autre. Un `DetectedObject` n'*est pas* une
`BoundingBox`, il en *possède* optionnellement une. La relation naturelle
entre ces objets est « contient », pas « est un type de ». Un héritage aurait
pu fonctionner techniquement en Python, mais n'aurait pas reflété
correctement le domaine.

### Liste par défaut via `default_factory`

`ImageDescription.detected_objects` utilise
`Field(default_factory=list)` plutôt que `= []`. En Python, une valeur par
défaut mutable est évaluée une seule fois et partagée entre toutes les
instances qui ne fournissent pas explicitement ce champ ; `default_factory`
garantit qu'une nouvelle liste est créée à chaque instanciation.

### Contraintes de `BoundingBox`

`x`/`y` sont bornés à `>= 0`, `width`/`height` à `> 0`. Aucune borne haute
n'est posée : le schéma `BoundingBox` n'a aucun moyen de savoir si les
coordonnées dépassent l'image, puisqu'il ne connaît pas sa taille. Cette
vérification est repoussée au code métier, au moment où l'image et sa
bounding box seront disponibles ensemble (voir
[Schéma de données](schema-donnees.md)).

### Exemple JSON du prompt écrit à la main

Le gabarit JSON du prompt d'extraction (`_JSON_EXAMPLE` dans
`service/prompts.py`) est écrit à la main plutôt que généré dynamiquement à
partir du schéma Pydantic. Générer cet exemple automatiquement demanderait
une fonction récursive de sérialisation, pour un gain jugé faible au vu de la
taille actuelle du schéma. C'est un risque assumé de redondance entre
`schemas.py` et `prompts.py` : les deux peuvent diverger si l'un est modifié
sans l'autre.

Un test dédié (`tests/test_prompt.py::test_json_example_matches_schema_recursively`)
compare récursivement les clés de l'exemple du prompt à celles du schéma
(`model_fields.keys()`). Toute divergence entre les deux fait désormais
échouer les tests en CI, au lieu de rester un écart implicite entre deux
fichiers.

### Pas de `yield` dans le loader de dataset

`list_dataset_images()` (`service/dataset_loader.py`) retourne une liste
matérialisée plutôt qu'un générateur, malgré le gain mémoire potentiel d'un
`yield` sur un dataset volumineux. Le dataset du projet reste de taille
réduite, ce qui rend ce gain inutile dans ce contexte. Si le dataset devenait
un jour très volumineux, repasser à un générateur serait pertinent - au prix
de devoir boucler dessus pour accéder aux éléments, au lieu d'indexer
librement une liste.

### Parsing défensif de la réponse du VLM

Le VLM ne renvoie pas toujours du JSON propre : il peut l'entourer de texte
ou de balises Markdown. `parse_vlm_response` garde ce qui va de la première
accolade `{` à la dernière `}`, le charge, puis le valide avec Pydantic.
Tout échec (réponse vide, JSON invalide, schéma non respecté) lève une seule
exception, `VLMResponseParsingError`, qui garde la réponse brute pour le
diagnostic. Il n'y a pas de nouvelle tentative auprès du VLM : l'image est
simplement sautée.

### Un embedding par élément, pas par image

C'est le cœur du projet. Une image donne une entrée pour son décor, une par
objet détecté et une pour son sujet principal. Un détail secondaire a ainsi
son propre vecteur au lieu d'être dilué dans un vecteur global de la scène.

### Texte d'un objet : label, couleur, état

Le texte embeddé pour un objet est `label couleur état` dans cet ordre fixe
(`object_to_text`), par exemple « ananas jaune dans un bac ». La position
(« centre droit ») et la bounding box restent hors du texte : ce ne sont pas
des mots qu'un utilisateur tape dans une requête. Elles sont gardées en
métadonnées. C'est une hypothèse, elle n'a pas été mesurée.

### Bounding box aplatie

ChromaDB n'accepte que des métadonnées scalaires. La boîte est donc
découpée en `bbox_x`, `bbox_y`, `bbox_width`, `bbox_height`, avec un
booléen `has_bbox` (`bbox_to_metadata`).

### Identifiants et marqueur de fin

Les ids suivent le nom de l'image : `nom:0`, `nom:1`... pour les objets,
`nom:background` pour le décor, `nom:main` pour le sujet principal. Le
séparateur `:` évite la confusion avec les noms du dataset, qui contiennent
déjà `_numéro`.

L'entrée `main` est écrite **en dernier** : si elle est présente, l'image a
été indexée en entier. Ce marqueur n'est pas encore lu (il faudrait une
méthode `exists` côté stockage), c'est la base prévue pour la reprise.

### Tout calculer avant d'écrire

`index_image` calcule tous les embeddings d'une image avant le premier
`add`. Si un embedding échoue, rien n'est écrit pour cette image. Une panne
pendant l'écriture peut encore laisser des entrées partielles, mais
l'absence de `main` permet de la repérer.

### Sujet principal vide refusé

Sans sujet principal, pas d'entrée `main`, donc pas de marqueur. Le cas lève
une `ValueError` et l'image est sautée par `index_dataset`. Solution
provisoire : la validation pourrait se faire directement dans le schéma.

### Quelles erreurs sauter pendant l'indexation d'un dossier

`index_dataset` saute les images dont la réponse VLM est inutilisable
(`VLMResponseParsingError`, `ValueError`) et laisse remonter tout le reste
(réseau, timeout). Une réponse ratée ne concerne qu'une image, une panne du
serveur les concernera toutes : inutile de continuer.

### Pas de VLM à la recherche

La requête est embeddée directement par `embeddinggemma`, le même modèle que
pour l'indexation. Pas de reformulation ni de re-classement par le VLM :
une requête coûte environ 0,2 s au lieu de plusieurs dizaines de secondes.
C'est une extension possible, hors du périmètre actuel.

### Résultats regroupés par image

L'index stocke des éléments, mais l'utilisateur cherche des images.
`search_image` renvoie donc une ligne par image `{image, distance,
matched}`, où `distance` et `matched` sont ceux de l'élément le plus proche.
Pour avoir assez d'images différentes après regroupement, ChromaDB est
interrogé avec `k × ELEMENTS_PER_IMAGE` éléments (10, constante dans
`config.py` ajoutée avec l'accord du Bloc B). Le 10 vient des 11 entrées
mesurées sur `market_0.jpg` ; il reste à vérifier en comptant les doublons
sur les requêtes d'évaluation.

Le regroupement garde le premier élément vu pour chaque image, ce qui
suppose que ChromaDB renvoie les résultats par distance croissante. Le
regroupement lit `metadata["image"]`, présent sur toutes les entrées, au
lieu de découper l'id.

### Requête limitée à 100 caractères

Les éléments indexés sont des textes courts. Une requête longue mélange
plusieurs idées dans un seul vecteur et ressemble moins à chacun d'eux. La
requête est donc coupée à 100 caractères (`MAX_QUERY_LENGTH`), sans erreur ;
l'interface est censée limiter la saisie de son côté.

## Bloc B - Infra & données

Responsable : GOBFERT Frédéric. Choix constatés dans le code et dans
`docs/FRED_REPORT.md`.

### Interfaces abstraites devant Ollama et ChromaDB

`BaseVLM`, `BaseEmbedding` et `BaseVectorIndex` isolent le reste du code des
outils concrets. `ChromaVectorIndex` hérite de `BaseVectorIndex` pour pouvoir
changer de base vectorielle sans toucher au Bloc A. Les tests du Bloc A en
profitent : ils remplacent ces classes par des faux.

### Adaptateurs asynchrones

Les adaptateurs et le wrapper sont passés en asynchrone (httpx) en octobre.
Le Bloc A a suivi : `index_image`, `index_dataset` et `search_image` sont des
fonctions `async`.

### Validation des entrées dans les adaptateurs

Chaque adaptateur vérifie d'abord le type, puis la valeur (chaîne vide,
vecteur vide, `k <= 0`) avant d'appeler Ollama ou ChromaDB. Le Bloc A a
repris la même convention en deux temps dans ses propres fonctions.

### Configuration par variables d'environnement

L'URL du serveur et les noms des modèles sont lus depuis `.env`
(`VCROP_*`, PR #18), avec des valeurs par défaut pour la CI.

<!-- TODO (Frédéric) : compléter ou corriger. -->

## Bloc C - Interface & livraison

Responsable : LEVITRE Mathys. Choix constatés sur les branches `dev` et
`feat/ResponsesRouter`, pas encore sur main.

### Interface en conversation

L'interface (Vue 3, Vite, Pinia pour l'état) est pensée comme une
messagerie : l'utilisateur tape sa recherche et les résultats arrivent comme
une réponse dans le fil.

### API FastAPI

L'API est écrite avec FastAPI, organisée en routeurs (`ResponsesRouter`), avec
un modèle Pydantic `Response` (`id`, `role`, `content`, `img_url`).

### Conteneurisation

Le Dockerfile construit le frontend avec Node puis le sert en statique sur le
port 8080. `docker-compose.yml` ajoute un service ChromaDB.

<!-- TODO (Mathys) : compléter ou corriger. -->
