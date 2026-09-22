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

un test dédié (`tests/test_prompt.py::test_json_example_matches_schema_recursively`)
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

## Bloc B - Infra & données

<!-- TODO (Frédéric) : choix techniques sur les adaptateurs Ollama et le
     stockage vectoriel. -->

## Bloc C - Interface & livraison

<!-- TODO (Mathys) : choix techniques sur l'interface, Docker, CI/CD. -->
