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
- Développement des tests d'initialisation d'une collection persistente et de l'envoi de données à chroma en mock
- Réalisation des tests sur id invalide