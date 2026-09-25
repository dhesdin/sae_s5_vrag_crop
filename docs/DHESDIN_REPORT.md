# Eleve & Introduction

DHESDIN Valentin

**Ce rapport a un simple but : Un journal de bord qui retrace par session :**

- Le contexte du travail
- Ce qui a été fait
- Difficulté rencontrées
- Décisions technique

---

**Ma partie est la suivante:**

- Définition du schéma json, validation tests unitaires.
- Conception du prompt VLM, test et itération sur l'inférence VLM.
- Parsing défensif de la réponse VLM.
- Pipeline d'indexation (parcours du dossier dataset/ , appel VLM par image...)
- Gestion des embeddings par élément détecté.
- Fonction de recherche embedding.
- Orchestration (pipeline) complet d'exécution.

---

## Séances de 09/09/2026 && 10/09/2026

Durée: 7h30

### Contexte du travail

Attribution du sujet V-CROP RAG, mise en place du repo et répartition des rôles
en groupe de 3 (Bloc A - perception/retrieval, Bloc B - infra/données, Bloc C -
interface/livraison). Début de mon périmètre (Bloc A) : conception du schéma
d'extraction structurée.

### Ce qui a été fait

- Bootstrap du repo (structure src/, pyproject.toml, CI en stub, Makefile)
- Définition du schéma Pydantic (ImageDescription, DetectedObject, BoundingBox)
  à partir du sujet (plan principal / décor / objets+attributs) à ce stade c'est une première version
  il sera sûrement ajusté lors des premières inférences VLM.
- Écriture et enrichissement des tests unitaires du schéma (cas valides,
  champs obligatoires manquants, types invalides, champs optionnels)
- Conception du prompt d'extraction VLM (instructions + forme JSON + exemple
  concret), avec tests unitaires associés
- Ajout du loader de dataset (`loader.py`) : listing et tri des chemins
  d'images depuis dataset/, sans chargement du contenu en mémoire

### Difficultés rencontrées

- Confusion initiale entre héritage et composition dans la conception des
  classes Pydantic imbriquées (jamais utilisé Pydantic auparavant)
- Piège Python des valeurs par défaut mutables (liste vide comme
  défaut) - nécessité d'utiliser default_factory pour déclarer correctement une liste propre à un objet.

### Décisions techniques

- Gabarit JSON du prompt : écrit à la main plutôt que généré dynamiquement
  depuis le schéma Pydantic. Raison : automatiser
  aurait demandé une fonction récursive pour peu de gain
  vu la faible taille du schéma actuel. C'est un risque accepté de redondance entre schemas.py et prompt.py : divergence possible. Choisis d'attendre le VLM, d'itérer et d'ajuster à la main jusqu'à trouver une stabilité.
- Structure du schéma (ImageDescription, DetectedObject, BoundingBox) :
  hésitation initiale entre héritage (classes filles) et composition avant
  de trancher pour la composition. Raison : aucune des trois classes
  n'est une spécialisation d'une autre --> un DetectedObject n'est pas un
  BoundingBox, par contre il possède optionnellement une BoundingBox - la relation
  naturelle entre elles est "contient" pas "est un type de". Je pense que ça aurait pu fonctionner via héritage en python,
  mais ce n'est pas correct.
- Loader de dataset : pas d'utilisation de yield malgré la réflexion
  sur la scalabilité. Raison : la contrainte du projet consiste à une taille de dataset de taille minimale, le gain mémoire serait inutile dans ce contexte mais si un jour le dataset devenait très volumineux, il serait pertinent de repenser cette approche et d'utiliser un générateur avec `yield`. car yield permet de produire les éléments un par un, réduisant ainsi l'utilisation de la mémoire. (mais nécessitera de boucler sur le générateur pour l'accès aux élements).

---

## Séance du 14/09/2026

Durée: 1h

### Contexte du travail

Suite au rapport de suivi automatique du 13/09/2026, deux écarts relevés sur mon
périmètre (Bloc A) : le `BoundingBox` du schéma n'était pas borné (aucune contrainte
sur x/y/width/height), et le prompt (`service/prompts.py`) et le schéma
(`service/schemas.py`) sont dupliqués sans garde-fou vérifiant leur cohérence.

### Ce qui a été fait

- Ajout de contraintes sur `BoundingBox` (`service/schemas.py`) : `x`/`y` bornés à
  `>= 0`, `width`/`height` bornés à `> 0`. Le prompt (`_JSON_EXAMPLE` dans
  `prompts.py`) exprime le bounding box en pixels absolus (ex: `x=120, y=80`), pas en
  coordonnées normalisées
- Complément des tests dans `tests/test_schemas.py` : coordonnées négatives
  rejetées, largeur/hauteur nulles ou négatives rejetées, `x=0`/`y=0` acceptés.
- Ajout d'un test de cohérence prompt <-> schéma
  (`tests/test_prompt.py::test_json_example_matches_schema_recursively`) qui
  compare, récursivement, les clés de `_JSON_EXAMPLE` aux champs de
  `ImageDescription`, `DetectedObject` et `BoundingBox` via `model_fields.keys()`.

### Difficultés rencontrées

- Aucune difficulté technique notable : les deux ajouts sont triviaux

### Décisions techniques

- Je n'ai pas mis de limite haute sur x/y/width/height : le schéma BoundingBox n'a aucun moyen de savoir si les coordonnées dépassent l'image, puisqu'il ne connaît pas sa taille. Cette vérification devra être faite plus tard, dans le code métier, au moment où on aura à la fois l'image et son bounding box sous la main.
- Le choix, documenté dans la séance du 09-10/09/2026, d'écrire le gabarit JSON du
  prompt à la main plutôt que de le générer dynamiquement depuis `schemas.py` était
  un risque assumé de divergence entre les deux fichiers. Plutôt que de revenir sur
  ce choix (génération dynamique jugée disproportionnée pour la taille actuelle du
  schéma), j'ai ajouté un test de cohérence qui compare les clés de l'exemple du
  prompt à celles du schéma. Ce test transforme ce risque silencieux : ça à été relevé dans le rapport de suivi automatique du 13/09/2026 ("prompt et schéma dupliqués"). Donc un garde-fou vérifié en CI : dorénavant, toute modification du schéma sans mise à jour de l'exemple (ou inversement) fait échouer les tests.

---

## Séance du 22/09/2026

Durée: 3h

### Contexte du travail

Objectif de la séance : exécuter les tests réels du prompt d'extraction sur une
image via `OllamaVLM.generate()`, sur le serveur
Ollama hébergé sur le réseau de l'IUT. Séance entièrement consommée par un
problème de connexion au wifi étudiant, aucun avancement sur le code de mon
périmètre...

### Ce qui a été fait

- Diagnostic réseau sur les deux SSID IUT ("IUT - Etudiant" / "IUT - Etudiant -
  5GHz") : correction d'une config `nmcli` initiale erronée
- Vérification du mot de passe via le QR code officiel de l'établissement
  (`zbar-tools`) et confirmation par un test de connexion réussi sur téléphone
  avec les mêmes identifiants - élimine l'hypothèse mot de passe
- Tests successifs sans effet : power management wifi mis hors service
- Tentative de remplacement du driver in-kernel `rtw_8821ce` par le driver
  DKMS communautaire `tomaspinho/rtl8821ce` : snapshot Timeshift fait avant, 
  une connexion réussie de façon isolée puis rechute immédiate sur le même symptôme
- Restauration du système à l'état d'origine via le snapshot Timeshift, wifi
  personnel revérifié fonctionnel.

### Difficultés rencontrées

- `4WAY_HANDSHAKE_TIMEOUT` systématique sur les deux SSID, testé sur
  plusieurs bornes du mesh IUT (BSSID différents), en 2.4GHz comme en 5GHz :
  la carte s'authentifie et s'associe au point d'accès mais le handshake
  WPA2 échoue après ~3 secondes
- Blocage Secure Boot lors de l'installation du driver DKMS (résolu par
  enrôlement MOK), puis faute IOMMU au chargement du nouveau module (résolu
  par paramètre kernel), pour un résultat final non concluant

### Décisions techniques

- Arrêt du diagnostic matériel après la restauration Timeshift plutôt que de
  poursuivre le bricolage driver : Contact du service informatique de l'IUT prévu pour
  trouver une solution... En attendant cette résolution, contournement
  retenu pour ne pas bloquer mon travail : demander à Frédéric (partie B), déjà connecté au réseau
  IUT, d'exécuter le script de test manuel à ma place et de me transmettre les
  réponses brutes du VLM, afin de pouvoir avancer sur le parsing. Lors des
  prochaines séances, je pourrai continuer mon travail sans dépendre de la résolution du problème matériel.

## Séance du 24/09/2026

### Ce qui a été fait

- A4 : premier appel réel du VLM (`qwen3-vl:8b-instruct`) via
  `scripts/manual_vlm_test.py`, testé sur 5 images du dataset. Réponse
  systématiquement en JSON pur, sans bloc markdown ni texte autour,
  conforme au schéma `ImageDescription` sur les 5 essais (champs attendus
  présents, coordonnées bounding box valides).

### Décisions techniques

- Format de sortie stable sur les 5 échantillons testés : ça confirme
  empiriquement l'hypothèse du prompt (JSON pur attendu), mais le parsing
  défensif prévu pour A5 reste inchangé - il continue de gérer les cas non
  observés ici (JSON entouré de texte, bloc markdown), le VLM restant non
  déterministe et l'échantillon limité à 5 images sur un seul run.

  ## Séance du 25/09/2026

Durée: 3h

### Contexte du travail

Transformer la réponse brute (non fiable) du VLM en objet `ImageDescription`
validé, ou en exception explicite si la réponse est inexploitable.


### Ce qui a été fait

- `service/parsing.py` : exception custom `VLMResponseParsingError`, fonction `parse_vlm_response()` couvrant 4 cas
  d'échec (réponse vide/whitespace, JSON invalide, JSON valide mais champ
  requis manquant, JSON entouré de texte libre ou de balises markdown), et
  fonction interne `_extract_json_candidate()` pour isoler le JSON du bruit
  autour
- `tests/test_parsing.py` : Multiple tests couvrant les cas nominaux, plus `_extract_json_candidate()` testée en isolation afin de vérifier son comportement sur différents types de bruit autour du JSON.
- `make lint && make test` : 51/51 tests passants, lint clean
- Merge sur `main` (branche `dhesdin/parsing-vlm-answers` --> make lint et clean également puis supprimée après
  merge)

### Difficultés rencontrées

- Plusieurs bugs réels trouvés en construisant pas à pas : ordre de vérification incorrect (le contrôle "réponse vide"
  passait après le `try`/`json.loads` au lieu d'avant, donc l'entrée `None`
  passait après le `try`/`json.loads` au lieu d'avant, donc l'entrée `None`
  crashé de façon non contrôlée), cas "" couvert par premier contrôle mais je suis passé sur .strip() pour détecter les entrées ne contenant que des espaces.
 - Chaînage d'exception (`raise ... from e`) oublié au premier jet : du coup on perdait le contexte original de l'erreur, rendant le débogage plus difficile.

### Décisions techniques

- Extraction du JSON par position des accolades (premier `{`, dernier `}`)
  plutôt que par regex : couvre à la fois le cas "JSON entouré de balises
  markdown" et "JSON entouré de texte libre" avec un seul mécanisme, sans
  avoir à distinguer les deux cas explicitement. Plus simple et plus robuste
  qu'une regex dédiée aux balises markdown.
- `ImageDescription.model_validate(data)` préféré à `ImageDescription(**data)` :
  `model_validate()` lève systématiquement `pydantic.ValidationError` quel que
  soit le type de `data`, alors que `**data` lève un `TypeError` non catché si
  `data` n'est pas un dict (ex: un JSON valide mais qui est une liste). Ce
  deuxième cas aurait traversé le `except ValidationError` sans être
  intercepté, cassant la garantie défensive du module.
- `_extract_json_candidate()` ne lève jamais d'exception elle-même : en
  l'absence d'accolades, elle retourne le texte brut nettoyé (`stripped`)
  plutôt que de lever une erreur directement. Ça laisse `json.loads()` dans
  `parse_vlm_response()` gérer l'échec normalement (déjà catché par
  `except json.JSONDecodeError`), évite un chemin d'erreur dupliqué, et garde
  la fonction testable de façon isolée et pure.