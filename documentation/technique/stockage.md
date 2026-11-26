# Stockage vectoriel

Les vecteurs sont stockés dans **ChromaDB**, en mode persistant sur disque.
Le code d'accès appartient au Bloc B (`src/v_crop_rag/storage/`) ; le contenu
des entrées est décidé par le Bloc A, qui les écrit.

## Interface

Le Bloc A ne voit ChromaDB qu'à travers `BaseVectorIndex`
(`storage/base.py`) :

```python
class BaseVectorIndex(ABC):
    def add(self, id: str, vector: list[float], metadata: dict) -> None: ...
    def query(self, vector: list[float], k: int = 5) -> list[VectoreSearchResult]: ...
```

`VectoreSearchResult` contient `id`, `distance` et `metadata`.

L'implémentation `ChromaVectorIndex` (`storage/chroma.py`) ouvre un
`PersistentClient` sur un dossier et crée la collection si elle n'existe
pas :

```python
index = ChromaVectorIndex(path="data/chroma", collection_name="crop_embeddings")
```

Elle vérifie les entrées avant chaque appel (id non vide, vecteur non vide de
nombres, `k` entier positif). Elle est couverte par 39 tests (`tests/test_chroma.py`), dont des tests
d'intégration avec un vrai ChromaDB qui vérifient la persistance.

## Où sont les données

- Dossier : `data/chroma`, ignoré par git (`data/` est dans `.gitignore`).
- Collection : `crop_embeddings`.

L'index n'est donc pas versionné : il faut le reconstruire avec
`scripts/manual_dataset_index.py` (environ 26 minutes, voir
[Indexer un dossier d'images](../utilisateur/indexation.md)).

## Ce que contient une entrée

Une image indexée produit une entrée pour son décor, une par objet détecté et
une pour son sujet principal. Exemple pour `market_0.jpg` (textes tirés des
essais, ils changent un peu à chaque passage du VLM) :

| id | `type` | `text` (ce qui a été embeddé) |
|---|---|---|
| `market_0:background` | `background` | « marché aux fruits et légumes intérieur, ... » |
| `market_0:0`, `market_0:1`, ... | `object` | « ananas jaune dans un bac », ... |
| `market_0:main` | `main_subject` | « un vendeur de fruits en train de manipuler un téléphone portable » |

Métadonnées présentes sur **toutes** les entrées : `image` (nom du fichier),
`type` et `text`. La recherche s'appuie sur `image` pour regrouper les
résultats et sur `text` pour expliquer un résultat.

Métadonnées en plus pour les objets : `label`, `position`, `has_bbox`, et
quand la boîte existe `bbox_x`, `bbox_y`, `bbox_width`, `bbox_height`.

Les vecteurs viennent d'`embeddinggemma` : 768 dimensions, norme 1 (mesuré :
0,9999999 sur l'essai du 10/11/2026).

## Distance

La collection est créée sans préciser de métrique, donc avec celle par
défaut de ChromaDB, la distance euclidienne au carré (L2²). Comme les
vecteurs sont de norme 1, elle classe les résultats exactement comme le
cosinus : L2² = 2 - 2 × cos. Une distance de 0,46 correspond donc à un
cosinus d'environ 0,77, et 0 à deux textes identiques.

## Limites connues

- **Pas de `exists(id)`** : on ne peut pas encore demander si une image est
  déjà indexée, donc le marqueur `nom:main` n'est pas exploité et il n'y a
  pas de reprise.
- **Pas de suppression ni d'`upsert`** : réindexer une image demande de
  repartir d'un index vide. Lors d'une relance sur un id déjà présent,
  ChromaDB a semblé ignorer le nouvel ajout (distances identiques), ce qui
  reste à confirmer en relisant le texte stocké.
- **Métrique cosinus non configurée** : sans conséquence sur le classement
  tant que les vecteurs sont normalisés, mais ce n'est pas explicite dans le
  code.

Ces trois points sont des pistes de travail pour le Bloc B, à confirmer avec
lui.

<!-- TODO (Frédéric) : compléter avec les choix de conception du stockage. -->
