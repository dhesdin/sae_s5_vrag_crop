#### Sprint 0 : Socle & Pipeline d'Extraction Visuelle (V-CROP RAG)
 
**User Stories**
 
* US 1.0.1 *(Bloc A - ValentinD)* : En tant que développeur, je dispose d'un schéma Pydantic strict de décomposition de l'image (sujet principal, arrière-plan, liste d'objets notables avec attributs : couleur, position, état, bounding box).
  Fait - `service/schemas.py`, 13 tests, mergé sur `main`.
* US 1.0.2 *(Bloc A - ValentinD)* : En tant que développeur, je rédige un prompt d'extraction contraignant le VLM à produire une sortie JSON conforme au schéma ci-dessus.
  Fait - `service/prompts.py`, 6 tests, mergé sur `main`.
* US 1.0.3 *(Bloc A - ValentinD)* : En tant que développeur, je constitue un dataset de test de photographies complexes (scènes composées, densité d'objets variable) accompagné d'une vérité terrain annotée manuellement, pour mesurer objectivement à quel point le VLM extrait correctement les informations (plus tard).
  Fait - `dataset/` (30 images), `dataset/ground_truth.json` (30 entrées, validé `json.load()`), mergé sur `main`.
* US 1.0.4 *(Bloc B - FredericG)* : En tant que développeur, TODO
* US 1.0.5 *(Bloc C - MathysL)* : En tant que développeur, je développe l'interface utilisateur de l'application en **Vue.js**, avec pour objectif de fournir une expérience conversationnelle complète et cohérente avec les attentes fonctionnelles et ergonomiques des utilisateurs.
Le travail porte notamment sur la mise en place de l'interface de conversation sous la forme d'une messagerie, la structuration des différents composants UI, la gestion des interactions utilisateur et l'adaptation de l'affichage aux différents états de l'application.
Une première version de l'interface est également développée avec des **données temporaires/mockées**, afin de pouvoir avancer sur l'intégration et tester les différents parcours utilisateurs en attendant la disponibilité des données réelles provenant du back-end. L'architecture de l'UI est pensée pour permettre le remplacement de ces données temporaires par les données du back-end avec un minimum de modifications.



L'objectif est également de respecter les attentes utilisateurs en matière de **fonctionnalités, d'ergonomie, de navigation, de responsive design et de cohérence visuelle**, afin de disposer d'une base d'interface exploitable pour les prochaines étapes d'intégration.

**Livrables / DoR & DoD**
 
| Livrable | Statut | Preuve |
|---|---|---|
| Schéma JSON hiérarchique (Pydantic) | Fait | `service/schemas.py` + 13 tests passants |
| Prompt d'extraction VLM structuré | Fait | `service/prompts.py` + 6 tests passants |
| Loader de dataset | Fait | `service/dataset_loader.py` + tests |
| Dataset de démo (30 images) + vérité terrain | Fait | `dataset/*.jpg`, `dataset/ground_truth.json` |
| Client VLM validé sur un appel test réel (`format="json"`) | Bloquant | En attente de Bloc B |
| Interface utilisateur conversationnelle (Vue.js) | En cours | Développement de l'interface de messagerie, composants UI et parcours utilisateurs    |
| Adaptation des données côté front                | En cours | Données mockées utilisées temporairement en attendant les données réelles du back-end |
| Expérience utilisateur (UX/UI)                   | En cours | Travail sur l'ergonomie, la navigation, le responsive design et la cohérence visuelle |

 