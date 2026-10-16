# Redmine_Automation — règles du projet

## Contexte

1. Ce projet automatise la récupération et l'analyse des tickets Redmine à tester pour Smart Shield ERP, la suite logicielle d'Egidium Technologies (nom interne : ISAP).
2. Smart Shield ERP comprend deux applications majeures : la WebApp (supervision dans le navigateur) et la WinApp, aussi appelée DeskApp ou IHM 3D (client lourd Windows).
3. Lexique : Suite logicielle > Application (WebApp, WinApp, application mobile…) > Applicatif ou module (Main Courante, Vidéo, Situation…) > Onglet ou fonctionnalité. « Application » ne désigne jamais un module.
4. Les analyses produites ici sont des documents internes. Les procédures destinées à un plan de validation reprennent la terminologie du plan.
5. Le poste est sous Windows : le terminal est PowerShell. Python est le WinPython du SDK Egidium : n'utiliser que la bibliothèque standard, ne jamais lancer `pip install`.

## Organisation des fichiers

| Emplacement | Rôle | Qui écrit |
|---|---|---|
| `recuperer_tickets.py` | Récupère les tickets de la version dans `tickets/` | Script, lancé par l'agent ou l'utilisateur |
| `convertir_plans.py` | Convertit les plans de validation Word en Markdown dans `referentiel/plans/` | Script |
| `analyses.py` | `preparer` : récupération, conversion et état ; `etat` ; `verifier` : contrôle des analyses ; `reprendre` : archive une analyse à refaire ; `question`, `appliquer` et `journal` : seules écritures autorisées dans `decisions.md` et `journal.md` ; `synthese` ; `reparer-decisions` | Script |
| `tickets/<version>/` | Tickets récupérés (`ticket.md`, `ticket.json`, pièces jointes) et `index.md` | Script uniquement |
| `referentiel/plans/` | Copies de lecture des plans Word | Script uniquement |
| `referentiel/correspondance-fonctions.md` | Fonction Redmine → plan et fiches à consulter | Humain |
| `referentiel/modele-analyse.md` | Forme d'une analyse de ticket | Humain |
| `analyses/<version>/<numéro>.md` | Analyse d'un ticket | Agent |
| `analyses/<version>/decisions.md` | Questions à trancher et décisions humaines | Script (questions et dates d'application), humain (décisions) |
| `analyses/<version>/archives/` | Analyses remplacées lors d'une reprise | Script uniquement ; l'agent ne les lit pas |
| `analyses/<version>/synthese.md` | Vue d'ensemble et ordre de campagne | Script uniquement |
| `analyses/<version>/journal.md` | Une ligne par action de l'agent | Script, appelé par l'agent |
| `referentiel/couverture-playwright.md` et `.json` | Fiches et tickets déjà couverts par la campagne Playwright, lus dans le projet Playwright | Script uniquement (`python analyses.py couverture`) |
| `referentiel/correspondance-playwright.md` | Rattachements imposés entre groupes de tests Playwright et fiches du plan | Humain |
| `export/<version>/campagne.json` | Analyses conformes exportées pour le projet de campagne Playwright | Script uniquement |

## Sources de vérité

1. Le ticket Redmine, tel que récupéré dans `tickets/`, fait foi pour ce qui a été demandé et livré. Lire la description et tout l'historique : les commentaires des développeurs contiennent souvent les règles fonctionnelles.
2. Le plan de validation Word fait foi pour les procédures existantes. `referentiel/plans/` en est une copie de lecture.
3. Ce qui ne figure ni dans le ticket ni dans le plan est une hypothèse : l'écrire comme telle et la reporter dans `decisions.md` si elle change la procédure.

## Interdits

1. Ne jamais écrire dans Redmine. Ne jamais appeler l'API Redmine autrement que par `recuperer_tickets.py`.
2. Ne jamais modifier à la main `tickets/`, `referentiel/plans/`, `referentiel/couverture-playwright.*`, `synthese.md` ni `export/` : ils sont régénérés par les scripts.
3. Ne jamais modifier les plans de validation Word.
4. Ne jamais ouvrir, afficher ni recopier le contenu de `.env`.
5. Ne jamais recopier d'identifiant ni de mot de passe lu dans un ticket ou un plan. Les remplacer par un repère explicite, par exemple `<MDP_LOCALADMIN>` ou `<IDENTIFIANT_SMTP>`.
6. Ne jamais trancher à la place de l'humain : une anomalie probable, un choix de fiche ambigu, une fiche à créer ou une procédure à supprimer passent par `decisions.md`.
7. Ne jamais écrire dans `decisions.md` : seules les commandes `python analyses.py question`, `appliquer` et `reparer-decisions` le modifient.
8. Ne jamais écrire dans `journal.md` autrement que par `python analyses.py journal`.
9. Ne jamais ajuster une analyse dans le seul but de satisfaire `python analyses.py verifier` : chaque écart signalé se corrige sur le fond, à partir du ticket et des plans.
10. Une analyse n'est terminée que lorsque `python analyses.py verifier --ticket <numéro>` répond « Aucun écart ».
11. Ne jamais lire ni modifier les scripts (`*.py`) ni les fichiers techniques `analyses/<version>/.preparation` et `.reprises.json`. Les messages des scripts et `python analyses.py --help` suffisent pour les utiliser.
12. Ne jamais filtrer la sortie d'un script avec `Select-Object` ou un tube : lire la sortie complète.

## Rédaction

1. Français soigné, phrases complètes, sans formule d'introduction ni de conclusion.
2. Une procédure de test suit le format des fiches du plan : des sous-titres en gras, puis une ligne par étape, chacune décrivant une action et son résultat observable, avec le numéro de ticket en fin de ligne, par exemple `(#8887)`.
3. Un résultat attendu est observable et vérifiable par un testeur : pas de « fonctionne correctement » sans préciser ce qui est constaté.
4. Une fiche se désigne toujours par son identifiant suivi de son titre, car certains identifiants sont utilisés plusieurs fois. La section 5 nomme la fiche exactement comme le champ « Fiche cible ».
5. Une analyse ne contient que les étapes du ticket analysé. Quand deux tickets se testent ensemble, chaque analyse garde ses propres étapes et la section 5 indique de les exécuter à la suite.
