# À reprendre dans le projet Test_Git (lecture seule)

Bloc à ajouter à `.github/copilot-instructions.md` de Test_Git, avant la section « Sécurité ». Rien n'est modifié dans Test_Git par la mise à jour de Redmine_Automation : c'est à toi de le coller.

```markdown
## Fiches issues des tickets Redmine
- Les fiches de transmission des tickets se trouvent dans `..\Redmine_Automation\echange\playwright\<version>\` (`index.json` + une fiche `<n>.md` par ticket concerné par la WebApp). Ce dossier se lit seulement : ne jamais y écrire, ne jamais écrire ailleurs dans `Redmine_Automation`.
- Avant de lire, vérifier que `format_contrat` de `index.json` vaut 1. Sinon, s'arrêter et le signaler.
- Une fiche indique la fiche cible, la nature, les prérequis et les étapes avec leurs résultats attendus. Elle ne remplace pas le plan : `docs/plans/01_V26.1 - WEBAPP - Automatisation.md` reste la source de vérité. Un écart entre la fiche et le plan est signalé en annotation, jamais corrigé en silence.
- Un ticket est repris quand son empreinte dans `index.json` a changé depuis la dernière reprise. Le ticket repris est cité dans le titre du test ou du groupe sous la forme `(#NNNN)`, comme le fait déjà `MC09 - Iris (#9011)`.
- Les étapes d'une fiche qui ne sont pas automatisables restent déclarées (`etapeManuelle`, `etapeHorsPerimetre` ou `test.fixme` avec motif), comme le reste du plan.
- Les anciens tests de `tests/` ne sont jamais modifiés pour traiter un ticket.
```

## Ligne à retirer

Les sept dernières lignes actuelles (« Fichier d'échange : `echange/COTE_TEST_GIT.md` » et les consignes sur les informations sensibles) décrivent un fichier qui n'existe pas dans Test_Git. Le fichier d'échange est dans Redmine_Automation. Ces lignes sont à remplacer par le bloc ci-dessus : la consigne de sécurité sur les identifiants est déjà dans la section « Sécurité ».
