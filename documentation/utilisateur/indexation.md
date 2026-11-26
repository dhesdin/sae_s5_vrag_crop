# Indexer un dossier d'images

L'indexation se fait **une seule fois par image**. C'est l'étape lente : le
VLM doit regarder chaque photo et la décrire.

## Lancer l'indexation du dataset

Depuis la racine du dépôt, sur le réseau de l'IUT :

```bash
python scripts/manual_dataset_index.py
```

Le script liste les images de `dataset/`, les indexe une par une et écrit
l'index ChromaDB dans `data/chroma` (collection `crop_embeddings`). Il
affiche une ligne par image avec sa durée, puis un bilan :

```text
beach_0.jpg indexed in 49.4 seconds
...
Indexed: 30
Failed: []
Total time: 1552.6 seconds
```

!!! note "Compter environ 26 minutes"
    Sur le serveur de l'IUT, les 30 images ont pris 1552,6 s, soit 51,8 s
    par image en moyenne (entre 35 et 73 s). Sortie complète :
    `docs/essais/essai-3-index-dataset.md`.

!!! warning "Index existant"
    Si `data/chroma` existe déjà, le script s'arrête. C'est voulu : il n'y a
    pas encore de reprise ni de mise à jour, et mélanger deux passages du
    VLM sur la même image donnerait un index incohérent. Pour repartir de
    zéro, supprimez le dossier `data/chroma`.

## Ce qui se passe pour chaque image

C'est la fonction `index_image` (`src/v_crop_rag/service/core.py`) qui fait
le travail :

1. le VLM reçoit l'image et le prompt d'extraction, et répond en JSON ;
2. la réponse est vérifiée par le parsing défensif et convertie en
   [`ImageDescription`](../technique/schema-donnees.md) ;
3. un embedding est calculé pour le décor, pour chaque objet détecté et pour
   le sujet principal ;
4. une fois **tous** les embeddings calculés, les entrées sont écrites dans
   l'index, le sujet principal en dernier.

Une image donne en général une dizaine d'entrées (11 mesurées sur
`market_0.jpg`). Le détail de ce qui est stocké est sur la page
[Stockage vectoriel](../technique/stockage.md).

## Quand une image échoue

`index_dataset` parcourt la liste et applique une règle simple :

- **réponse du VLM inutilisable** (JSON invalide, champ manquant, sujet
  principal vide) : l'image est sautée, notée dans `failed` avec la raison,
  et la boucle continue ;
- **toute autre erreur** (serveur injoignable, timeout, erreur d'embedding) :
  l'indexation s'arrête, car le problème touchera aussi les images
  suivantes.

Sur l'essai complet, aucune image n'a été sautée.

## Utiliser les fonctions depuis Python

```python
from pathlib import Path

from v_crop_rag.service.core import index_dataset
from v_crop_rag.service.dataset_loader import list_dataset_images

images = list_dataset_images(Path("dataset"))   # .jpg, .jpeg, .png, triés
result = await index_dataset(images, vlm, embedding, index)
# {"indexed": ["beach_0.jpg", ...], "failed": [("nom.jpg", "raison"), ...]}
```

`vlm`, `embedding` et `index` sont les adaptateurs du Bloc B (`OllamaVLM`,
`OllamaEmbedding`, `ChromaVectorIndex`). Le script
`scripts/manual_dataset_index.py` montre comment les construire.
