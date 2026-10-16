# Couverture Playwright

Générée le 16/10/2026 17:34 par `python analyses.py couverture`. Ne pas modifier à la main : corriger les rattachements dans `referentiel/correspondance-playwright.md`.

- Tests lus : 437
- Fiches du plan 01 couvertes : 11 sur 15
- Tickets cités dans les titres de test : 121

## Fiches couvertes

| Fiche | Tests | Dont @a-valider | Fichiers |
|---|---|---|---|
| MC01 — Généraux | 9 | 1 | main-courante/Automatique_mc01-generaux-connexion.spec.ts |
| MC02 — Onglet Main Courante | 159 | 76 | main-courante/Automatique_mc02-01-presence-elements.spec.ts, main-courante/Automatique_mc02-01b-traduction.spec.ts, main-courante/Automatique_mc02-01c-parametres-avances.spec.ts, main-courante/Automatique_mc02-02-applications.spec.ts, main-courante/Automatique_mc02-03-mode-lecture.spec.ts, main-courante/Automatique_mc02-04-options-affichage.spec.ts, main-courante/Automatique_mc02-05-comportement-lignes.spec.ts, main-courante/Automatique_mc02-06-parametres-incidents.spec.ts, main-courante/Automatique_mc02-07-session-timeout.spec.ts, main-courante/Automatique_mc02-08-lieux-adresse.spec.ts, main-courante/Automatique_mc02-09-bandeau-superieur.spec.ts, main-courante/Automatique_mc02-10-bulletin.spec.ts, ../fixtures/plan.ts, main-courante/Automatique_mc02-11-activites.spec.ts, main-courante/Automatique_mc02-12-administration.spec.ts |
| MC03 — Onglet Statistiques | 40 | 35 | statistiques/Automatique_mc03-statistiques.spec.ts |
| MC04 — Onglet Situation | 35 | 35 | situation/Automatique_mc04-situation.spec.ts |
| MC05 — Onglet Vidéo | 26 | 25 | video/Automatique_mc05-video.spec.ts |
| MC06 — Onglet Evénements | 16 | 12 | evenements-planifies/Automatique_mc06-evenements-planifies.spec.ts |
| MC07 — Onglet Evénements | 7 | 6 | evenements/Automatique_mc07-evenements.spec.ts |
| MC10 — Onglet Administration | 67 | 50 | administration/Automatique_mc10-00-controle-page-object.spec.ts, administration/Automatique_mc10a-dossiers-comptes.spec.ts, administration/Automatique_mc10b-referentiels.spec.ts |
| MC11 — Onglet Mode expert (IsapReporting) | 19 | 19 | isap-reporting/Automatique_mc11-isap-reporting.spec.ts |
| MC12 — Tests à plusieurs personnes | 16 | 15 | multi-utilisateurs/Automatique_mc12-multi-utilisateurs.spec.ts |
| MC13 — Manipulation des fichiers | 13 | 12 | fichiers-et-scripts/Automatique_mc13-fichiers-scripts.spec.ts |

## Rattachement des groupes de tests

| Groupe Playwright | Fiche du plan | Rattachement | Remarque |
|---|---|---|---|
| MC01 - Généraux | MC01 — Généraux | identifiant et libellé |  |
| MC02 - Activités | MC02 — Onglet Main Courante | identifiant et libellé |  |
| MC02 - Applications | MC02 — Onglet Main Courante | identifiant et libellé |  |
| MC02 - Bandeau inférieur de la Main Courante | MC02 — Onglet Main Courante | imposé |  |
| MC02 - Bandeau supérieur | MC02 — Onglet Main Courante | imposé |  |
| MC02 - Bulletin | MC02 — Onglet Main Courante | identifiant et libellé |  |
| MC02 - Comportement des lignes | MC02 — Onglet Main Courante | identifiant et libellé |  |
| MC02 - Lieux, Intervenants & Champs adresse | MC02 — Onglet Main Courante | imposé |  |
| MC02 - Mode Lecture | MC02 — Onglet Main Courante | identifiant et libellé |  |
| MC02 - Mode lecture | MC02 — Onglet Main Courante | identifiant et libellé |  |
| MC02 - Onglet Administration | MC02 — Onglet Main Courante | identifiant et libellé |  |
| MC02 - Options d'affichage et générales de la table | MC02 — Onglet Main Courante | imposé |  |
| MC02 - Paramètres avancés | MC02 — Onglet Main Courante | imposé |  |
| MC02 - Paramètres incidents | MC02 — Onglet Main Courante | imposé |  |
| MC02 - Paramètres incidents & formulaires | MC02 — Onglet Main Courante | imposé |  |
| MC02 - Présence des éléments | MC02 — Onglet Main Courante | imposé |  |
| MC02 - Session & Timeout Multi | MC02 — Onglet Main Courante | imposé |  |
| MC02 - Traduction de l'interface | MC02 — Onglet Main Courante | imposé |  |
| MC03 - Statistiques | MC03 — Onglet Statistiques | identifiant et libellé |  |
| MC04 - Situation | MC04 — Onglet Situation | identifiant et libellé |  |
| MC05 - Vidéo | MC05 — Onglet Vidéo | identifiant et libellé |  |
| MC06 - Évènements planifiés | MC06 — Onglet Evénements | identifiant et libellé |  |
| MC07 - Évènements | MC07 — Onglet Evénements | identifiant et libellé |  |
| MC09 - Iris (#9011) | — | imposé | fiche imposée « — » introuvable dans le plan 01 : la recopier depuis la liste « Fiches du plan 01 » ci-dessous, ou écrire « Aucune » |
| MC10 - Administration | MC10 — Onglet Administration | identifiant et libellé |  |
| MC10 - SDK Python | — | imposé | fiche imposée « — » introuvable dans le plan 01 : la recopier depuis la liste « Fiches du plan 01 » ci-dessous, ou écrire « Aucune » |
| MC11 - IsapReporting | MC11 — Onglet Mode expert (IsapReporting) | identifiant et libellé |  |
| MC12 - Tests à plusieurs personnes | MC12 — Tests à plusieurs personnes | identifiant et libellé |  |
| MC13 - IsapReportingServer | MC13 — Manipulation des fichiers | imposé |  |
| MC13 - Log démarrage serveur et PermissionsVerifier | MC13 — Manipulation des fichiers | imposé |  |
| MC13 - Perte de connexion (#8739) | MC13 — Manipulation des fichiers | imposé |  |
| MC13 - Python SDK | MC13 — Manipulation des fichiers | imposé |  |
| MC13 - Test unitaire WebService (#8366) | MC13 — Manipulation des fichiers | imposé |  |
| MC13 - TestIsapServer (#8570) | MC13 — Manipulation des fichiers | imposé |  |

## Fiches du plan 01

Désignations exactes, à recopier telles quelles dans `correspondance-playwright.md`.

| Fiche | Titre de section | Couverte |
|---|---|---|
| MC01 — Généraux | Généraux – connexion | oui |
| MC02 — Onglet Main Courante | Onglet Main Courante | oui |
| MC03 — Onglet Statistiques | Onglet Statistiques | oui |
| MC04 — Onglet Situation | Onglet Situation & Partage de Situation | oui |
| MC05 — Onglet Vidéo | Onglet Vidéo | oui |
| MC06 — Onglet Evénements | Onglet Evénements planifiés | oui |
| MC07 — Onglet Evénements | Onglet Evénements | oui |
| MC08 — Onglet Evénements | Onglet Planification | non |
| MC09 — Iris | Iris | non |
| MC10 — Onglet Administration | Onglet Administration | oui |
| MC11 — Onglet Mode expert (IsapReporting) | Onglet Mode expert- ISAPREPORTING | oui |
| MC10 — Export de données | Tests exports de données | non |
| MC12 — Tests à plusieurs personnes | Tests à plusieurs personnes @ | oui |
| MC13 — Manipulation des fichiers | Tests via modification des fichiers | oui |
| MC12 — Configuration Grille & Droits | Configuration Grille & droits | non |
