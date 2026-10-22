# Mise à jour 16 — échange avec le projet Playwright, sans rien modifier de l'autre côté

1. `python analyses.py exporter` (appelé aussi par `bilan`) écrit désormais `echange/playwright/<version>/` : une fiche par ticket concerné par la WebApp et un manifeste `index.json` avec une empreinte par fiche. Les fiches de tickets qui ne sont plus concernés sont supprimées dans ce seul dossier.
2. Aucune écriture dans `Test_Git` : la règle 15 des consignes l'interdit, et le script n'y touche pas.
3. `echange/LISEZMOI.md` décrit le contrat. `echange/COTE_TEST_GIT.md` est le texte à copier, si tu le souhaites, dans les consignes de Test_Git.
4. Rien d'autre ne change : `couverture` et `campagne.json` fonctionnent comme avant.

Installation : décompresser sur `Redmine_Automation` en écrasant (maj13 à maj15 déjà installées), lancer `python analyses.py exporter`, puis commiter `echange/` via Fork.
