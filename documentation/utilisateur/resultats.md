# Comprendre un résultat

Pour chaque image indexée, le VLM (modèle de vision) produit une description
structurée en JSON, conforme au schéma [`ImageDescription`](../technique/schema-donnees.md).
C'est ce même objet qui sert ensuite de base à la recherche.

## Exemple

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

## Lecture des champs

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

## Valeurs manquantes

`color`, `state` et `bounding_box` sont **optionnels** : lorsqu'une
information n'est pas déterminable pour un objet donné, le champ vaut `null`
plutôt que d'être omis ou deviné. `main_subject`, `background` et `label`
sont en revanche toujours renseignés - un résultat où l'un de ces champs
manquerait n'est pas un résultat valide au sens du schéma.

`bounding_box`, quand elle est présente, n'est garantie que sur sa borne
basse (`x >= 0`, `y >= 0`, `width`/`height` `> 0`) : le schéma ne peut pas à
lui seul vérifier qu'elle reste dans les limites de l'image.
