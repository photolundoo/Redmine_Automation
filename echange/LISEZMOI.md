# Échange avec le projet Playwright (Test_Git)

Ce dossier est le seul point de contact entre `Redmine_Automation` et `Test_Git`.

## Règles

1. Chaque dépôt n'écrit que chez lui. `Redmine_Automation` ne modifie jamais `Test_Git`, et `Test_Git` ne modifie jamais `Redmine_Automation`.
2. Ce dossier ne contient que des fichiers générés par `python analyses.py exporter`. Aucun identifiant, aucun mot de passe, aucun contenu du `.env`.
3. Une fiche dont le contenu change a une nouvelle `empreinte` dans `index.json` : c'est le signal « à reprendre » pour Test_Git.

## Contenu

| Fichier | Rôle |
|---|---|
| `playwright/<version>/index.json` | Manifeste : version du contrat, date, un enregistrement par ticket concerné par la WebApp, avec son empreinte |
| `playwright/<version>/<n>.md` | Fiche de transmission du ticket `<n>` : issue, plan et fiche cibles, prérequis, bloc Playwright, étapes et résultats attendus |

Le fichier `export/<version>/campagne.json` (format 1) reste le contrat complet de toutes les analyses.

## Version du contrat

`format_contrat: 1`. Si ce numéro change, Test_Git doit s'arrêter et le signaler au lieu de lire.
