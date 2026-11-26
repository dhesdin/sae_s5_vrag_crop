# FAQ / erreurs courantes

Les problèmes ci-dessous ont tous été rencontrés pendant le projet.

## « Ollama server is not running » ou erreur de connexion

Le serveur Ollama de l'IUT n'est joignable que depuis le réseau de l'IUT.
Depuis chez soi, il faut un Ollama local (voir
[Installation](installation.md#configurer-lacces-a-ollama)).

!!! warning "Scripts d'indexation et d'évaluation"
    `scripts/manual_dataset_index.py` et `scripts/manual_eval_search.py`
    construisent le client sans lui passer `VCROP_OLLAMA_URL` : ils visent
    toujours l'adresse par défaut du wrapper, celle du serveur de l'IUT.
    Seuls `manual_vlm_test.py` et `manual_embedding_test.py` lisent la
    variable. Pour un Ollama local, il faut donc pour l'instant modifier
    ces deux scripts.

## `OllamaConnectionError` au premier appel du VLM, alors que le serveur répond

C'est un timeout. Le wrapper attend 60 s par défaut, et le premier appel au
VLM peut dépasser ce délai le temps que le modèle se charge (essai du
10/11/2026, `docs/essais/essai-1-timeout-vlm.md`). Les scripts d'indexation
passent `timeout_s=300`. Si vous écrivez votre propre script, faites pareil.

## « data/chroma already exists »

Le script d'indexation refuse de partir d'un index existant. Supprimez le
dossier `data/chroma` pour réindexer depuis zéro. Il n'y a pas encore de
reprise : une indexation coupée en route doit être relancée en entier.

## « data/chroma not found »

Le script d'évaluation a besoin d'un index. Lancez d'abord
`python scripts/manual_dataset_index.py`.

## Une image apparaît dans « failed »

Le VLM a renvoyé une réponse inutilisable : JSON cassé, champ obligatoire
absent, ou sujet principal vide. L'image est sautée et la raison est notée
(tronquée à 200 caractères). Relancer peut suffire, car le VLM ne répond pas
toujours la même chose d'un passage à l'autre.

## La recherche ne trouve pas une image qui contient pourtant l'objet

Deux causes vues sur les essais :

- **le mot n'est pas celui du VLM** : il a écrit « moto » ou « motocycle »
  là où la requête dit « scooter » ;
- **la requête est trop pauvre** : « un réverbère » ou « un lampadaire »
  échouent, « un lampadaire noir » marche, car le texte indexé était
  « lampadaire noir éteint ».

Ajouter la couleur ou essayer un synonyme aide souvent. Voir
[Rechercher une image](recherche.md#ecrire-une-bonne-requete).

## Les mêmes images reviennent sur des requêtes sans rapport

Oui, c'est une limite connue. Sur les 10 requêtes d'évaluation,
`workbench_1.jpg` apparaît 6 fois et `desktop_0.jpg` 4 fois : ces images
contiennent beaucoup de petits objets colorés, donc souvent un élément
« assez proche ». Il n'y a pas de seuil de distance pour les filtrer.

## Deux indexations de la même image ne donnent pas le même nombre d'entrées

Normal : le VLM n'est pas déterministe. `market_0.jpg` a donné 11 entrées
au premier passage et 8 au second.
