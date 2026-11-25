# Comprendre un résultat

Il y a deux sortes de résultats dans le projet : ce que renvoie une
**recherche** (une liste d'images classées), et ce que le VLM produit pour
chaque image à l'**indexation** (une description structurée).

## Résultat d'une recherche

`search_image` renvoie une liste d'images, la plus proche en premier, avec
au plus `k` lignes. Exemple réel pour « un vélo bleu » avec `k = 3`
(`docs/essais/essai-4-evaluation.md`) :

```python
[
    {"image": "bicycle_1.jpg", "distance": 0.459, "matched": "un vélo bleu appuyé contre un mur"},
    {"image": "workbench_1.jpg", "distance": 0.544, "matched": "moules bleu"},
    {"image": "terace_1.jpg", "distance": 0.595, "matched": "vélo bleu, blanc à l'arrêt, avec panier"},
]
```

- **`image`** : le nom du fichier dans `dataset/`. Pour afficher l'image,
  on reconstruit le chemin à partir du dossier du dataset (pas de
  vignette stockée).
- **`distance`** : la distance entre la requête et l'élément le plus proche
  de cette image. **Plus elle est petite, plus c'est proche.** 0 veut dire
  texte identique.
- **`matched`** : le texte de cet élément le plus proche. C'est ce qui
  explique pourquoi l'image est remontée : ici, la 2e image n'a pas de vélo,
  elle remonte à cause de « moules bleu ».

!!! note "Lire les distances"
    Sur les essais, une bonne réponse se situe souvent entre 0,36 et 0,7, et
    les résultats hors sujet vers 0,8 à 1,05. Mais les deux zones se
    chevauchent : aucun seuil fiable n'a été trouvé pour dire « en dessous
    de telle valeur, c'est pertinent ». Le classement compte plus que la
    valeur brute.

Ce format n'est pas encore figé avec l'API et l'interface : il peut encore
bouger quand le Bloc C branchera la recherche.

## Description d'une image par le VLM

Pour chaque image indexée, le VLM produit une description structurée en
JSON, conforme au schéma [`ImageDescription`](../technique/schema-donnees.md).
Ses champs deviennent ensuite les entrées de l'index.

### Exemple

```json
{
  "main_subject": "un vélo rouge appuyé contre un mur",
  "background": "rue pavée en ville, façade d'immeuble en pierre, fin de journée",
  "detected_objects": [
    {
      "label": "vélo",
      "color": "rouge",
      "position": "centre",
      "state": "à l'arrêt",
      "bounding_box": { "x": 120, "y": 80, "width": 300, "height": 220 }
    },
    {
      "label": "panneau de signalisation",
      "color": "bleu",
      "position": "en haut à droite",
      "state": null,
      "bounding_box": null
    }
  ]
}
```

### Lecture des champs

- **`main_subject`** - le sujet principal de l'image, en une phrase courte.
- **`background`** - l'arrière-plan et le contexte général de la scène.
- **`detected_objects`** - la liste des éléments notables repérés dans
  l'image, potentiellement vide si aucun élément distinct n'a été identifié.

Pour chaque objet détecté :

- **`label`** - le nom de l'objet.
- **`position`** - sa position relative dans l'image, exprimée en langage
  naturel (ex. `"centre"`, `"en haut à gauche"`), et non en coordonnées.
- **`color`** - la couleur dominante de l'objet, quand elle est pertinente.
- **`state`** - un état notable de l'objet (ex. `"ouvert"`, `"cassé"`),
  quand il y en a un.
- **`bounding_box`** - la zone rectangulaire de l'objet dans l'image, en
  pixels absolus (`x`, `y`, `width`, `height`), quand elle a pu être
  localisée précisément.

### Valeurs manquantes

`color`, `state` et `bounding_box` sont **optionnels** : lorsqu'une
information n'est pas déterminable pour un objet donné, le champ vaut `null`
plutôt que d'être omis ou deviné. `main_subject`, `background` et `label`
sont en revanche toujours renseignés - un résultat où l'un de ces champs
manquerait n'est pas un résultat valide au sens du schéma.

`bounding_box`, quand elle est présente, n'est garantie que sur sa borne
basse (`x >= 0`, `y >= 0`, `width`/`height` `> 0`) : le schéma ne peut pas à
lui seul vérifier qu'elle reste dans les limites de l'image.

En pratique, le VLM renseigne rarement la boîte : sur `market_0.jpg`, un
seul objet sur neuf en avait une. L'unité en pixels est celle demandée par
le schéma, elle a été vérifiée à l'œil sur une seule boîte. La boîte n'entre
pas dans la recherche, elle est seulement conservée en métadonnées.
