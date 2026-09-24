# Rechercher une image

!!! warning "État d'avancement"
    La fonction de recherche n'est pas encore implémentée
    (`service/core.py` et `service/utils.py` sont vides à ce stade). Cette
    page documente le fonctionnement prévu ; elle sera mise à jour avec
    l'usage réel dès que la recherche sera codée.

## Principe prévu

La recherche s'appuiera sur les embeddings calculés à l'étape
[d'indexation](indexation.md) : chaque objet détecté dans une image
(`DetectedObject`, voir le [schéma de données](../technique/schema-donnees.md))
aura son propre embedding, obtenu via `BaseEmbedding.embed` (Bloc B).

Le principe envisagé :

1. la requête de recherche (texte libre décrivant ce qui est cherché) est
   transformée en embedding avec le même modèle d'embedding que celui utilisé
   à l'indexation,
2. cet embedding est comparé aux embeddings stockés pour chaque objet
   détecté (similarité vectorielle, via le stockage du Bloc B),
3. les résultats sont remontés au niveau de l'image (et de l'objet détecté
   correspondant) plutôt qu'au niveau du vecteur brut, pour rester
   exploitables côté interface (Bloc C).

## Dépendances

Cette fonction dépend :

- du stockage vectoriel mis en place par le Bloc B (`storage/`),
- des embeddings produits à l'indexation, donc du pipeline décrit dans
  [Indexer un dossier d'images](indexation.md).

Elle ne peut donc pas être finalisée avant ces deux briques.
