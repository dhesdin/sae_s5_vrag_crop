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
- Ajout du loader de dataset (`service/dataset_loader.py`) : listing et tri des chemins
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

---

## Séance du 24/09/2026

Durée: 2h

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

---

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


  ---

## Séances du 06/10/2026 au 09/10/2026

Durée: 3h

### Contexte du travail

Début de A6/A7 : orchestration de l'indexation d'une image (`service/core.py`),
c'est le seul blocage identifié par l'audit du 28/09 (`core.py` vide). Travail sur
la branche `dhesdin/index-single-image`, non mergée à ce stade car il manque tests unitaire et les essais réels.

### Ce qui a été fait

- `service/utils.py` : `bbox_to_metadata()` (aplatit la bounding box en métadonnées
  scalaires préfixées `bbox_*` + `has_bbox`), `object_to_text()` (texte embeddé d'un
  objet), `image_to_metadata()` (métadonnées du sujet principal et du décor), et
  `_join_parts()` partagée.
- `tests/test_utils.py` : tests de `bbox_to_metadata` (dont un contrôle depuis directement la librairie
  `chromadb.api.types.validate_metadata`) et de `object_to_text`.
- `service/core.py` : `index_image()` : prompt, appel VLM, parsing, puis un embedding
  par objet, un pour le décor, un pour le sujet principal. Commitée sur la branche.
- `scripts/manual_index_test.py` : squelette seulement, câblage à faire (tests unitaire aussi à prévoir pour core.py et utils.py(nouvelles fonctions))

### Difficultés rencontrées

- Format des métadonnées attendu par ChromaDB : j'ai d'abord pensé envoyer la
  bounding box telle quelle, donc un dict (ou un objet) imbriqué dans le dict de
  métadonnées. Chroma attend des métadonnées plates, avec des valeurs scalaires
  (str, int, float, bool). D'où `bbox_to_metadata()`, qui aplatit la bounding box
  en champs préfixés `bbox_*` + `has_bbox`.
- Structuration de `core.py` : c'est le fichier qui m'a demandé le plus
  d'itérations.
  - un embedding distinct par objet, par décor et par sujet principal ;
  - des métadonnées exploitables (image source, type, texte embeddé, label,
    position) ;
  - tous les embeddings calculés avant le premier `add` ;
  - l'entrée `:main` écrite en dernier, comme marqueur de complétion.
- Première version de `bbox_to_metadata` : le contrôle de type passait avant le
  test `None`, donc le cas courant (objet sans bbox) levait une erreur, et
  `has_bbox` était écrasé. Trouvé en relecture.

### Décisions techniques

- Texte embeddé d'un objet : `label`, `color`, `state`. La position n'y est pas : elle
  est relative à l'image (" centre droit "), ce n'est pas du vocabulaire de requête.
  Elle reste en métadonnée pour l'affichage. Hypothèse non encore mesurée : à valider
  sur des requêtes de test.
- Un embedding distinct par élément, conformément à la fiche : sujet principal et décor
  ne sont pas fusionnés.
- Ids : `{image}:{i}` pour les objets (index = position dans `detected_objects`),
  `{image}:background`, `{image}:main`. Séparateur `:` car les noms du dataset
  contiennent déjà `_0`, `_1`...
- Marqueur de complétion : `:main` est écrit en dernier. Tous les embeddings sont
  calculés avant le premier `add`.
- `index_image` dépend des types de base (`BaseVLM`, `BaseEmbedding`, `BaseVectorIndex`),
  pas des classes concrètes, et n'attrape aucune exception : c'est la boucle sur le
  répertoire qui décidera de sauter une image ou d'arrêter. Pour moi c'est l'appelant qui décidé quoi en faire de son application
  Par exemple sauter une image, s'arrêter à la première erreur, continuer malgré les erreurs...
- `main_subject` vide : `ValueError` avant tout calcul (choix provisoire).

### Points ouverts

- À fournir par FredericG : `exists(id)` et une suppression par image (cache et
  réindexation).
- À vérifier : métrique de distance de la collection Chroma (cosinus exigé par la
  fiche) ; comportement de Chroma sur un `add` avec id déjà présent ; préfixe de tâche
  d'embeddinggemma (model card) ; unité des coordonnées de bbox sur une sortie réelle.

### À faire

- Tests de `image_to_metadata` et `tests/test_core.py` (faux VLM, faux embedder, faux
  index).
- Câblage de `scripts/manual_index_test.py` et essais réels (latence, dimension du
  vecteur, relance sur la même image).
- Boucle sur le dataset et cache, puis recherche et ranking (A8).


---

## Séances du 20/10/2026 au 12/11/2026

Durée: 15H

### Contexte du travail

Suite de A6/A7 : `index_image` doit passer en asynchrone (les adaptateurs de Frédéric
sont asynchrones depuis le 11/10), être testé avec de faux modèles, essayé sur le
vrai serveur de l'IUT, puis étendu à tout un dossier (`index_dataset`). Entre-temps :
retour de la prof (30/10) et audit automatique (01/11).

### Ce qui a été fait

- 20/10 : `index_image` passé en asynchrone. `tests/test_core.py` avec faux VLM, faux
  embedder et faux index asynchrones (12 tests).
- 09/11 : branche `dhesdin/index-single-image` poussée, 124 tests au
  `make test`.
- 10/11 : premier essai réel sur le serveur IUT. `scripts/manual_index_test.py`
  réécrit en asynchrone, sortie versionnée dans `docs/essais/`.
- 12/11 : `index_image` fusionné sur main (PR #19). `index_dataset` écrit : boucle sur
  les images, une ligne par image avec sa durée, retourne `{"indexed": [...],
  "failed": [(nom, raison)]}`. 3 tests (15 tests dans `test_core.py`.

### Mesures réelles (serveur IUT, 10/11/2026, une seule image : market_0.jpg)

- embeddinggemma : dimension 768, norme 0,9999999 (donc distance L2 et cosinus
  classent pareil).
- VLM : 24 s par image. Premier passage : `ReadTimeout` à 60 s (timeout par défaut du
  wrapper trop court), remonté comme `OllamaConnectionError`.
- `index_image` : 11 entrées en 26 s. Relance : 8 entrées (le VLM n'est pas
  déterministe), mais distances identiques sur les ids déjà présents : Chroma semble
  ignorer un `add` sur un id existant.
- bbox : 1 objet sur 9 en possède une. Unité probablement en pixels (constat visuel sur
  une seule bbox, non confirmé).
- Requête "Des pastèques verte et mûre" : melon d'eau au rang 6, meilleure distance
  0,77. Une seule requête, aucune conclusion.

### Difficultés rencontrées

- Passage en asynchrone : les faux modèles des tests ont dû être réécrits en
  asynchrone.
- CI rouge sur main après le merge de la PR #19 : imports de `tests/test_core.py` mal
  triés. Corrigé par `dhesdin/fix-test-imports`, CI verte sur la PR.
- Timeout du wrapper (60 s) trop court au premier appel du VLM : relevé à 300 s dans le
  script d'essai.

### Décisions techniques

- `index_dataset` saute une image dont la réponse du VLM est inexploitable
  (`VLMResponseParsingError`), mais laisse remonter `OllamaConnectionError` : si le
  serveur est injoignable, continuer sur les images suivantes n'a pas de sens.
- Appels séquentiels (pas de `asyncio.gather`) : un seul serveur Ollama partagé, le
  parallélisme n'apporterait rien de mesuré et compliquerait les erreurs.
- Position hors du texte embeddé : décision du 09/10 maintenue, hypothèse toujours non
  comparée pour l'instant pas la priorité.

---

## Séances du 13/11/2026 au 25/11/2026

Durée: 13H

### Contexte du travail

Rendre la recherche utilisable et mesurée (sprint 3) : `search_image`, indexation des
30 images, évaluation sur 10 requêtes, contrat de réponse pour l'API.

### Ce qui a été fait

- 13/11 : `search_image(query, embedding, index, k=5)` écrite dans `service/core.py` :
  gardes, embedding de la requête, `index.query` avec `k * ELEMENTS_PER_IMAGE` éléments,
  regroupement par image (élément le plus proche), tri par distance, coupe à k. Une
  ligne par image : `{image, distance, matched}`. Constante `ELEMENTS_PER_IMAGE = 10`
  ajoutée dans `config.py` avec l'accord de Frédéric.
- 23-25/11 : 9 tests de `search_image` (une ligne par image, élément le plus proche
  conservé, coupe à k, `k * ELEMENTS_PER_IMAGE` demandé à l'index, gardes de type,
  requête vide, k invalide, bool refusé, troncature). 136 tests au `make test`, CI
  verte, merge sur main.
- Indexation des 30 images sur le serveur IUT (`scripts/manual_dataset_index.py`,
  sortie dans `docs/essais/essai-3-index-dataset.md`) : 30 indexées, 0 échec,
  1552,6 s au total, soit 51,8 s par image (min 35,2 s, max 73,1 s). L'estimation de
  départ (environ 13 minutes) était fausse : le VLM met deux fois plus de temps que sur
  l'image unique mesurée le 10/11.
- Évaluation (`scripts/manual_eval_search.py`, `docs/essais/essai-4-evaluation.md`) :
  10 requêtes écrites depuis `dataset/ground_truth.json`, K = 3. L'image attendue est
  dans le top 3 pour 9 requêtes sur 10. Temps par requête : environ 1,7 s pour la
  première (démarrage à froid), 0,12 à 0,28 s ensuite.
- Diagnostics des limites (`essai-5-variantes-vocabulaire.md`,
  `essai-6-diagnostic-lampadaire.md`) :
  - " un scooter " : problème de vocabulaire. " un motocycle " retrouve les 2 images
    attendues sur 2.
  - " un réverbère " : échec non expliqué. " un lampadaire " échoue aussi, " un
    lampadaire noir " place l'image attendue au rang 1 (distance 0,489). Recherche du
    texte exact indexé : distance 0,0 et rang 1, donc le pipeline fonctionne. Hypothèse
    (la couleur fait partie du texte indexé) non testée, 2 cas seulement.
  - Faux positifs récurrents : workbench_1 revient 6 fois et desktop_0 4 fois dans les
    résultats de l'évaluation. Aucun seuil de distance exploitable mesuré.

### Difficultés rencontrées

- Premier lancement de l'indexation : `.env` surchargeait le modèle (`qwen3-vl:2b-instruct`
  introuvable, erreur 404). Corrigé dans `.env` (modèle 8b). Le dossier `data/chroma`
  avait déjà été créé avant l'échec : suppression nécessaire avant la relance (le
  script refuse de réutiliser un index existant).
- Garde du script d'évaluation inversée (`if not CHROMA_PATH.exists()`) et imports
  parasites ajoutés par l'éditeur : repérés en relecture.
- Un premier lancement du script d'évaluation a exécuté un ancien contenu (test
  d'index dans un dossier temporaire) : `data/chroma` n'avait pas été touché, fichier
  remplacé.
- Diagnostic erroné de ma part sur " un réverbère " (je l'avais d'abord attribué au
  vocabulaire) : " un lampadaire " échoue aussi
- Erreur de branche : j'ai commité scripts et essais directement sur main sans m'en
  apercevoir au début. Choix assumé ensuite pour ces petits fichiers (pas de code de
  service), mais c'est une entorse à la règle une branche par tâche.

### Décisions techniques

- Pas de VLM à la requête : le texte de l'utilisateur est embeddé par le même modèle
  (embeddinggemma). Le VLM ne sert qu'à l'indexation. Pas de reformulation ni de
  re-ranking (extension possible, hors périmètre).
- `search_image` renvoie des images, pas des éléments : `distance` est celle de
  l'élément le plus proche de l'image, `matched` le texte de cet élément. Pas de
  vignettes : Mathys construit le chemin depuis le dossier dataset.
- `k * ELEMENTS_PER_IMAGE` éléments demandés à Chroma, car une image produit une dizaine
  d'entrées (11 mesurées sur market_0.jpg). Le 10 reste une hypothèse : le nombre de
  doublons d'image n'a pas été compté sur les 10 requêtes.
- Requête tronquée à 100 caractères (une requête longue dilue le vecteur, les éléments
  indexés sont courts). Troncature silencieuse pour l'appelant.
- Distance Chroma par défaut (L2 au carré) : suffisant ici, vecteurs de norme 1, même
  classement que le cosinus. Le cosinus explicite est demandé à Frédéric.
- Évaluation limitée à 10 requêtes écrites par moi : petit échantillon, à présenter
  comme tel. Pas de seuil de distance : l'interface doit afficher un rang, pas un
  pourcentage de similarité.
- Limite connue, non traitée (hors périmètre de la semaine) : sensibilité aux
  synonymes (vocabulaire du VLM contre vocabulaire de la requête).

### Points ouverts

- Contrat de réponse `{image, distance, matched}` à valider avec Mathys.
- Frédéric : `exists(id)`, suppression par image ou upsert, métrique cosinus, renommer
  `VectoreSearchResult` (en cours).
- Préfixe de tâche d'embeddinggemma côté requête : à vérifier dans la fiche du modèle
  avant toute modification.