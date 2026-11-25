# Essais et mesures

Tous les chiffres de cette page viennent d'essais lancés sur le serveur Ollama
de l'IUT, avec `qwen3-vl:8b-instruct` et `embeddinggemma:latest`. Les sorties
brutes sont versionnées dans `docs/essais/` du dépôt : chaque chiffre peut
être vérifié.

## 1. Premier essai sur une image (10/11/2026)

Script : `scripts/manual_index_test.py`, image `market_0.jpg`.
Sorties : `essai-1-timeout-vlm.md`, `essai-index-image-2026-11-10.md`.

| Mesure | Valeur |
|---|---|
| Dimension des vecteurs | 768 |
| Norme d'un vecteur | 0,9999999 (donc normalisés) |
| Temps du VLM pour une image | 24 s |
| `index_image` complet | 11 entrées en 26 s |
| Relance sur la même image | 8 entrées : le VLM n'est pas déterministe |

Le premier passage a échoué : le timeout par défaut du wrapper (60 s) est
trop court pour le premier appel au VLM, le temps que le modèle se charge.
Les scripts suivants passent `timeout_s=300`.

## 2. Indexation des 30 images

Script : `scripts/manual_dataset_index.py`. Sortie : `essai-3-index-dataset.md`.

| Mesure | Valeur |
|---|---|
| Images indexées | 30 sur 30 |
| Échecs | 0 |
| Temps total | 1552,6 s (environ 26 min) |
| Moyenne par image | 51,8 s |
| Plus rapide / plus lente | 35,2 s (`bench_1`) / 73,1 s (`market_2`) |

Une image coûte en moyenne deux fois plus que sur `market_0.jpg` au premier
essai. L'estimation de départ (13 minutes pour le dataset, à partir des 24 s
du premier essai) était donc fausse. Les images les plus chargées (cuisines,
marchés, établis) sont les plus lentes, ce qui colle avec un VLM qui décrit
plus d'objets ; ce lien n'a pas été mesuré précisément.

## 3. Évaluation de la recherche sur 10 requêtes

Script : `scripts/manual_eval_search.py`. Sortie : `essai-4-evaluation.md`.

Les 10 requêtes ont été écrites à la main à partir de
`dataset/ground_truth.json`, qui décrit le contenu attendu de chaque image.
Pour chaque requête, on regarde si une image attendue apparaît dans les 3
premiers résultats (`k = 3`).

| Requête | Image attendue | Rang | Distance | Élément trouvé |
|---|---|---|---|---|
| un ananas | `kitchen_0`, `market_0` | 1 | 0,531 | ananas jaune dans un bac |
| un scooter | `terace_2`, `car_0` | 2 | 0,954 | moto gris stationnée |
| un réverbère | `bicycle_2` | absent | - | - |
| un mètre ruban | `workbench_2` | 1 | 0,855 | ruban à mesurer jaune |
| une voiture de sport rouge | `car_2` | 1 | 0,483 | une voiture rouge Dodge Challenger |
| un vélo bleu | `bicycle_1` | 1 | 0,459 | un vélo bleu appuyé contre un mur |
| un parasol multicolore | `beach_1` | 1 | 0,415 | un parasol coloré sur une plage de sable |
| un sous-bois d'automne | `bench_1` | 1 | 0,690 | un banc en bois dans une forêt d'automne |
| des îlots rocheux dans une eau turquoise | `beach_0` | 1 | 0,603 | mer turquoise, petites îles rocheuses à l'horizon |
| un mur rose | `bicycle_0` | 1 | 0,364 | mur rose pâle |

**Résultat : 9 requêtes sur 10 ont une image attendue dans le top 3**, dont 8
au rang 1.

Temps de réponse : environ 1,7 s pour la première requête (le modèle
d'embedding démarre), puis 0,12 à 0,28 s.

Ce qui marche bien : des détails qui ne sont pas le sujet de la photo sont
retrouvés (le mètre ruban sur un établi, l'ananas dans un marché), et les
requêtes de décor aussi (« un sous-bois d'automne », « des îlots rocheux »).

## 4. Diagnostics sur les échecs

Sorties : `essai-5-variantes-vocabulaire.md`, `essai-6-diagnostic-lampadaire.md`.

**« un scooter »** : problème de vocabulaire. Le VLM a écrit « moto » et
« motocycle ». Avec la requête « un motocycle », les deux images attendues
sortent aux rangs 1 et 2.

**« un réverbère »** : échec pas complètement expliqué.

| Requête | Rang de `bicycle_2` | Distance |
|---|---|---|
| un réverbère | absent | - |
| un lampadaire | absent (des lampes de bureau et de salon passent devant) | - |
| un lampadaire noir | 1 | 0,489 |
| lampadaire noir éteint (texte exact indexé) | 1 | 0,0 |

Le texte exact donne une distance nulle et le rang 1 : la chaîne
indexation, stockage, recherche est saine. L'hypothèse est que la couleur et
l'état font partie du texte indexé, et qu'une requête réduite au nom de
l'objet s'en éloigne trop. Elle repose sur deux cas seulement et n'a pas été
testée plus largement.

## Limites de ces mesures

- **Petit échantillon** : 10 requêtes, écrites par la même personne qui a
  conçu le système. Le 9 sur 10 donne une tendance, pas une performance
  garantie.
- **Faux positifs récurrents** : sur les 10 requêtes, `workbench_1` apparaît
  6 fois dans les résultats et `desktop_0` 4 fois. Ces images contiennent
  beaucoup de petits objets, donc souvent un élément vaguement proche.
- **Pas de seuil de distance** : les bonnes réponses vont de 0,36 à 0,95 et
  les mauvaises commencent vers 0,54. On ne peut pas filtrer les résultats
  non pertinents avec une valeur fixe.
- **Synonymes** : la recherche dépend des mots choisis par le VLM.
- **Facteur 10 non vérifié** : le nombre d'éléments demandés à ChromaDB
  (`k × 10`) n'a pas été confronté au nombre réel de doublons d'image.

## Pistes non testées

- Ajouter le préfixe de tâche recommandé pour `embeddinggemma` côté requête
  (à vérifier dans la fiche du modèle).
- Comparer des variantes du texte indexé, par exemple avec et sans l'état.
- Une reformulation de la requête par un LLM avant l'embedding, pour les
  synonymes (hors périmètre actuel).
