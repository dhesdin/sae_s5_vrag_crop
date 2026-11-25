# V-CROP RAG

Recherche d'images par leurs éléments constitutifs.

L'idée de départ est simple : une recherche d'image classique résume une
photo en un seul vecteur, ce qui noie les détails. Un parasol rouge au fond
d'une photo de plage passe inaperçu. Ici, chaque image est décrite par un VLM
(sujet principal, décor, objets avec couleur et état), puis **chaque élément
reçoit son propre embedding**. Une requête comme « un mètre ruban » peut donc
retrouver une photo d'établi même si le mètre n'en est pas le sujet.

## Où en est le projet (25/11/2026)

Le moteur fonctionne de bout en bout côté Python :

- les 30 images du dataset ont été indexées sur le serveur Ollama de l'IUT
  (30 réussies, 0 échec, environ 26 minutes au total) ;
- la recherche a été évaluée sur 10 requêtes : l'image attendue apparaît
  dans les 3 premiers résultats pour 9 requêtes sur 10 ;
- une requête répond en 0,12 à 0,28 s une fois le modèle chargé.

Ce qui manque encore : le branchement de l'API et de l'interface web sur la
recherche (le format de réponse reste à valider avec le Bloc C), et la
reprise d'une indexation interrompue. Le détail des mesures est dans
[Essais et mesures](technique/essais.md).

## Équipe

| Membre | Bloc | Rôle |
|---|---|---|
| DHESDIN Valentin | A - Perception & Retrieval | schéma, prompt, parsing, indexation, recherche |
| GOBFERT Frédéric | B - Infra & données | accès aux modèles Ollama, stockage ChromaDB |
| LEVITRE Mathys | C - Interface & livraison | interface web, API, Docker |

## Organisation de la documentation

- **Documentation utilisateur** : installer le projet, indexer le dataset,
  lancer une recherche et lire un résultat.
  Point d'entrée : [Installation & lancement](utilisateur/installation.md).
- **Documentation technique** : architecture en blocs, schéma de données,
  choix techniques, stockage vectoriel, essais réels et déploiement.
  Point d'entrée : [Architecture](technique/architecture.md).

Le suivi semaine par semaine (sprints, journaux de bord, sorties brutes des
essais) n'est pas sur ce site mais dans le dossier `docs/` du dépôt.

Code source : [dhesdin/sae_s5_vrag_crop](https://github.com/dhesdin/sae_s5_vrag_crop)

SAE BUT3 Application Intelligente, IUT du Littoral.
