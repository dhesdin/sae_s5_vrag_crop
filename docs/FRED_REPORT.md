# Points d'avancement du projet V-CROP RAG - PARTIE B : Infra & données

## 10/09/26
- rectifications apportées au main suite à une mauvaise compréhension de la répartition des tâches sur un sujet à la frontière entre parties A et B.
- Construction de la partie commune (pour OllamaVLM, OllamaEmbedding, OllamaLLM)

## 11/09/26
- panne matérielle, perte de la connexion de mon disque dur contenant toutes mes données liées à la SAE (entre autres) et la partition Linux en dual boot.

## 13/09/26
- Tests de fonctionnement des différents modèles en local (qwen3:1.7b, gemma3:1b, qwen3-vl:2B-instruct, embeddinggemma:latest)
- Insertion du fichier ollama_wrapper_iut.py
- Création des interfaces BaseVLM et BaseEmbedding
- Création des adaptateurs OllamaVLM et OllamaEmbedding + tests
- MAJ du monitoring (Sprint 00)

## 21/09/26
- Réflexion en commun sur la méthode utilisée afin d'intégrer la documentation utilisateur. Choix arrêté sur mkdoc et l'intégration continue avec Git.

## 22/09/26
- Relecture du code et mise en commun des implémentations.
- Développements et recherches sur ChromaDB et sur la méthode pour implémenter les classes en minimisant les dépendances aux choix de base.
- Développement des tests d'initialisation d'une collection persistante et de l'envoi de données à chroma en mock
- Réalisation des tests sur id invalide

## 23/09/26 et 24/09/26
- Avancée sur le développement d'une classe ChromaVectorIndex héritant de BaseVectorIndex afin de laisser la possibilité de changer de base ultérieurement
- Développement des tests et des mocks sur ChromaVectorIndex

## 25/09/26
- Réalisation de tests d'intégration en utilisant réellement chromadb
- Interrogation écrite (avec Mme Pacou) et présentation du fonctionnement demandé au niveau de l'interaction IA <-> fichiers

