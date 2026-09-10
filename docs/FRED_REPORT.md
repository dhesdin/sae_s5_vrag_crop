# Points d'avancement du projet V-CROP RAG - PARTIE B : Infra & données

## 10/09/26
- rectifications apportées au main suite à une mauvaise compréhension de la répartition des tâches sur un sujet à la frontière entre parties A et B.
- Construction de la partie commune (pour OllamaVLM, OllamaEmbedding, OllamaLLM)
- architecture visée:
                   BaseModelEndpoint
                   ─────────────────
                   URL Ollama
                   nom du modèle
                   appel HTTP commun
                         ▲
              ┌──────────┼──────────┐
              │          │          │
          OllamaVLM   Embedding    LLM

