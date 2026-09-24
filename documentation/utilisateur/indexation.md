# Indexer un dossier d'images

!!! warning "État d'avancement"
    Le pipeline d'indexation complet n'est pas encore implémenté. Cette page
    documente ce qui existe réellement aujourd'hui, et ce qui reste à faire.

## Ce qui existe aujourd'hui

Le point de départ de l'indexation est le listing du dossier `dataset/` par
`list_dataset_images()` (`src/v_crop_rag/service/dataset_loader.py`) :

- parcourt un dossier (par défaut `dataset/` à la racine du projet),
- ne garde que les fichiers dont l'extension est `.jpg`, `.jpeg` ou `.png`,
- retourne la liste triée des chemins, **sans charger le contenu des images
  en mémoire** - seul le chemin est manipulé à ce stade.

```python
from v_crop_rag.service.dataset_loader import list_dataset_images

images = list_dataset_images("dataset")
# [PosixPath('dataset/a.png'), PosixPath('dataset/b.jpg'), ...]
```

Le prompt d'extraction VLM ([conçu et testé](../technique/choix-techniques.md))
existe également (`build_extraction_prompt()` dans `service/prompts.py`) mais
n'est pas encore branché sur un appel réel image par image dans un pipeline.

## Ce qu'il reste à faire

L'orchestration complète de l'indexation n'est pas encore codée
(`service/core.py` est vide à ce stade). Elle est prévue pour, pour chaque
image listée par `list_dataset_images()` :

1. appeler le VLM (`BaseVLM.generate`, fourni par le Bloc B via
   `OllamaVLM`) avec le prompt d'extraction et l'image,
2. parser et valider la réponse JSON du VLM contre le schéma
   [`ImageDescription`](../technique/schema-donnees.md) (avec parsing
   défensif : réponse non JSON, champs inattendus, etc.),
3. calculer un embedding par élément détecté (`BaseEmbedding.embed`, fourni
   par le Bloc B via `OllamaEmbedding`),
4. stocker le résultat (description + embeddings) dans le stockage vectoriel
   (Bloc B).

Cette page sera mise à jour avec la commande / fonction réelle d'indexation
dès que ce pipeline sera implémenté.
