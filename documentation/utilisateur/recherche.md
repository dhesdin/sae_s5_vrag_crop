# Rechercher une image

Une fois le dataset [indexé](indexation.md), on peut interroger l'index avec
une phrase courte en français : « un vélo bleu », « un mur rose »,
« des îlots rocheux dans une eau turquoise ».

## Comment ça marche

La recherche n'appelle **pas** le VLM. Le texte de la requête est
simplement transformé en vecteur par le même modèle d'embedding que celui de
l'indexation (`embeddinggemma`), puis comparé aux vecteurs stockés. C'est ce
qui la rend rapide : de l'ordre de 0,1 à 0,3 s par requête, contre presque
une minute par image à l'indexation.

Les étapes, dans `search_image` (`src/v_crop_rag/service/core.py`) :

1. la requête est nettoyée et coupée à 100 caractères ;
2. elle est transformée en vecteur ;
3. ChromaDB renvoie les `k × 10` éléments les plus proches (une image
   produit une dizaine d'entrées, plusieurs peuvent ressembler à la
   requête) ;
4. les éléments sont regroupés par image, en gardant pour chacune son
   élément le plus proche ;
5. les images sont triées par distance croissante et on en garde au plus
   `k`.

## Lancer une recherche

Le plus simple est le script d'évaluation, qui enchaîne 10 requêtes sur
l'index de `data/chroma` :

```bash
python scripts/manual_eval_search.py
```

Depuis Python :

```python
from v_crop_rag.service.core import search_image

results = await search_image("un vélo bleu", embedding, index, k=3)
```

Ce que renvoie la fonction est décrit dans
[Comprendre un résultat](resultats.md#resultat-dune-recherche).

## Écrire une bonne requête

Les éléments indexés sont des textes courts, du type
« ananas jaune dans un bac » ou « mur rose pâle ». Les requêtes qui marchent
le mieux leur ressemblent :

- **nommer l'objet et sa couleur** : « un lampadaire » échoue, alors que
  « un lampadaire noir » retrouve la bonne image au rang 1 ;
- **utiliser le mot que le VLM aurait choisi** : « un scooter » ne retrouve
  qu'une des deux images attendues, « un motocycle » retrouve les deux ;
- **rester court** : au-delà de 100 caractères, la requête est coupée sans
  prévenir.

Ces constats viennent de très peu de cas (voir
[Essais et mesures](../technique/essais.md)), ce sont des pistes plutôt que
des règles.

## Erreurs possibles

| Situation | Erreur |
|---|---|
| `query` n'est pas une chaîne | `TypeError` |
| requête vide ou faite d'espaces | `ValueError` |
| `k` n'est pas un entier (un booléen est refusé) | `TypeError` |
| `k` inférieur à 1 | `ValueError` |
