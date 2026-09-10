# Eleve & Introduction
DHESDIN Valentin

**Ce report à un simple but : Un journal de bord qui retrace par session :**

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
Durée: 3h00

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