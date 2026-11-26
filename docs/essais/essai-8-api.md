# Essai 8 : recherche de bout en bout par l'API

Date : 26/11/2026
Branche testée : `mlevitre/RequestRouter` (route `POST /requests/`, non mergée à ce stade)
Contexte : réseau IUT, vrai index `data/chroma` (30 images, essai-3), back lancé avec `python -m backend.main`.
Commande :
`curl -X POST localhost:8000/requests/ -H "Content-Type: application/json" -d '{"query":"un ananas","k":3}'`
Résultat : market_0 et kitchen_0 aux rangs 1 et 2, mêmes distances que l'appel direct de `search_images`. Rang 3 : desktop_0 (« plante vert »), faux positif. Durée de cette première requête : environ 2 s (démarrage à froid).

## Sortie

```json
[{"rank":1,"image":"market_0.jpg","distance":0.5310430526733398,"matched":"ananas jaune dans un bac"},{"rank":2,"image":"kitchen_0.jpg","distance":0.5387313365936279,"matched":"ananas vert et jaune entier, intact"},{"rank":3,"image":"desktop_0.jpg","distance":0.8587518930435181,"matched":"plante vert"}]
```