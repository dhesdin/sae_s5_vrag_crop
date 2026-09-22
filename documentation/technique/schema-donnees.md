# Schéma de données

Le schéma décrit la sortie structurée attendue du VLM (modèle de vision) pour
une image : c'est le contrat entre l'extraction (Bloc A) et tout ce qui
consomme ce résultat ensuite (indexation, recherche, interface).

Il est défini avec [Pydantic](https://docs.pydantic.dev/) dans
`src/v_crop_rag/service/schemas.py`, sous la forme de trois modèles
imbriqués par **composition** (pas d'héritage) : un `DetectedObject`
*possède* optionnellement une `BoundingBox`, il n'*est pas* une `BoundingBox`.

## `ImageDescription`

Modèle racine, une instance par image traitée.

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `main_subject` | `str` | oui | Sujet principal de l'image |
| `background` | `str` | oui | Arrière-plan / contexte général |
| `detected_objects` | `list[DetectedObject]` | non (`[]` par défaut) | Liste des objets notables détectés |

La liste par défaut est déclarée avec `Field(default_factory=list)` et non
`= []` : une valeur mutable par défaut serait partagée entre toutes les
instances du modèle qui ne fournissent pas explicitement ce champ.

## `DetectedObject`

Un élément détecté dans l'image.

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `label` | `str` | oui | Nom de l'objet |
| `position` | `str` | oui | Position relative en langage naturel (ex. `"en haut à gauche"`, `"centre"`) |
| `color` | `str \| None` | non | Couleur dominante, si pertinent |
| `state` | `str \| None` | non | État notable (ex. `"ouvert"`, `"cassé"`) |
| `bounding_box` | `BoundingBox \| None` | non | Boîte englobante, si localisable |

## `BoundingBox`

Boîte englobante en **pixels absolus** (pas de coordonnées normalisées).

| Champ | Type | Contrainte |
|---|---|---|
| `x` | `float` | `>= 0` |
| `y` | `float` | `>= 0` |
| `width` | `float` | `> 0` |
| `height` | `float` | `> 0` |

Seule une borne basse est imposée : `BoundingBox` ne connaît pas la taille de
l'image dans laquelle elle s'inscrit, donc rien ne garantit ici que la boîte
reste à l'intérieur de l'image. Cette vérification (borne haute) est repoussée
au code métier, au moment où l'image et sa bounding box sont disponibles
ensemble.

## Cohérence avec le prompt VLM

Le prompt d'extraction (`service/prompts.py`) contient un exemple JSON
(`_JSON_EXAMPLE`) écrit à la main plutôt que généré depuis ce schéma, pour
éviter une fonction récursive de sérialisation disproportionnée par rapport à
la taille actuelle du schéma. Ce choix introduit un risque de divergence
entre le schéma et l'exemple donné au modèle.

Ce risque est couvert par un test dédié
(`tests/test_prompt.py::test_json_example_matches_schema_recursively`) qui
compare récursivement les clés de `_JSON_EXAMPLE` à celles de
`ImageDescription`, `DetectedObject` et `BoundingBox`
(via `model_fields.keys()`). Toute modification du schéma sans mise à jour de
l'exemple (ou inversement) fait échouer les tests.

## Validation

Le schéma est couvert par `tests/test_schemas.py` :

- instanciation valide avec 0, 1 ou plusieurs objets détectés,
- champs obligatoires manquants (`main_subject`, `background`, `label`,
  `position`) --> `ValidationError`,
- champs optionnels réellement optionnels (`color`, `state`,
  `bounding_box` à `None`),
- `BoundingBox` : coordonnées négatives, largeur/hauteur nulles ou négatives
  rejetées ; `x=0`/`y=0` acceptés.
