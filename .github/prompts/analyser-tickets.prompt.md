---
description: Analyser les tickets Redmine de la version selon la méthode en 5 étapes et préparer la campagne de test
agent: agent
---

# /analyser-tickets

Tu analyses les tickets Redmine de la version en cours, un par un, selon la méthode en 5 étapes du pôle QA. Tu travailles sans poser de question : ce que tu ne peux pas trancher va dans `decisions.md`. Respecte les règles de `.github/copilot-instructions.md`.

## Vérification préalable

Cette commande exige deux outils : l'exécution de commandes dans le terminal et l'écriture de fichiers dans l'espace de travail. Si l'un des deux manque dans cette session, n'essaie aucun contournement : réponds en une phrase quel outil manque, et arrête-toi.

## Paramètres

Lis-les dans le message qui suit la commande. Valeurs par défaut entre parenthèses.

- `lot=` nombre maximal de tickets traités pendant ce passage (8). Chaque ticket compte, qu'il s'agisse d'appliquer une décision, de reprendre une analyse ou d'en écrire une nouvelle.
- `ticket=` numéro d'un ticket à analyser ou réanalyser, même si son analyse est à jour. Dans ce cas, seul ce ticket est traité.
- `version=` dossier de version dans `tickets/` (la seule version présente).

Dans la suite, `<version>` désigne ce dossier, par exemple `ISAP-V27.1`, et `<n>` le numéro du ticket traité. Remplace toujours ces repères par les valeurs réelles : ne les écris jamais tels quels, ni dans un fichier ni dans une commande.

## Étape 0 — Préparation

À chaque passage, y compris quand tu reprends un passage interrompu, lance une seule commande :

```
python analyses.py preparer --lot <lot>
```

avec la valeur du paramètre `lot` (8 par défaut ; 1 avec le paramètre `ticket=`). Elle récupère les tickets, convertit les plans modifiés, fixe le lot du passage et affiche l'état. Si la récupération échoue, elle s'arrête : arrête-toi aussi.

Le script tient le compte du lot : `appliquer`, `reprendre`, `question` et `journal` comptent chacun le ticket concerné, et refusent tout nouveau ticket une fois le lot atteint. Ce refus est la condition d'arrêt : passe alors à l'étape 3 et arrête-toi, sans relancer `preparer` pour ouvrir un nouveau lot. Sans préparation de moins de 12 heures, ces mêmes commandes refusent de s'exécuter.

Pour revoir le début de la file sans tout afficher : `python analyses.py etat --max 10`. N'utilise jamais `Select-Object` ni de tube sur la sortie des scripts. Si `decisions.md` n'a pas le format attendu, lance `python analyses.py reparer-decisions`, puis `python analyses.py etat`.

La liste « À analyser » donne l'ordre de traitement : d'abord les décisions à appliquer, puis les analyses à reprendre, puis les nouvelles. Respecte cet ordre.

Lis ensuite une fois `referentiel/correspondance-fonctions.md` et `referentiel/modele-analyse.md`.

## Étape 1 — Appliquer les décisions de la relecture

Pour chaque ticket listé avec le motif « décision à appliquer » :

| Décision | Ce que tu fais dans l'analyse du ticket |
|---|---|
| `valider` (ou `validé`, `approuvé`) | La proposition est retenue : reporte-la dans l'analyse si elle n'y figure pas déjà (section 5 et, le cas échéant, « Plan cible » et « Fiche cible »). |
| `corriger :` suivi d'un texte | Applique exactement la correction décrite, dans les sections concernées. |
| `fiche :` suivi d'une fiche | Remplace « Plan cible » et « Fiche cible » par la fiche indiquée, avec l'identifiant et le titre exacts du plan, puis reprends les sections 3 et 5 pour cette fiche. |
| `nouveau plan :` suivi d'un intitulé | Mets « Plan cible » à « À créer — » suivi de l'intitulé, « Fiche cible » à « À créer — » suivi du titre que tu proposes, et reprends la section 5 pour ce nouveau plan. |
| `réanalyser`, éventuellement suivi de `:` et d'une consigne | Lance `python analyses.py reprendre --ticket <n>`, puis refais l'analyse complète (étape 2) en suivant la consigne. |
| `hors campagne` | Mets « Nature du test » à « Hors campagne », « Automatisabilité » à « Non applicable », et ajoute la décision en tête de la section 5. |
| `ignorer` | Rien à changer. |

Puis :
1. Mets « Décision humaine requise » à « Non » si plus aucune question de ce ticket n'attend de décision.
2. Lance `python analyses.py appliquer --ticket <n>`. Le script contrôle l'analyse et date la décision ; tu n'écris jamais toi-même dans `decisions.md`. S'il refuse, corrige l'analyse et relance-le.

Une ligne de relecture (« Relecture » dans la colonne Question) s'applique de la même façon : l'humain l'a ajoutée sur un ticket dont l'analyse semblait conforme.

Les décisions signalées « à reformuler par l'humain » par `etat` ne s'appliquent pas : ne les interprète pas, ne les modifie pas, et cite-les dans le message de fin.

## Étape 2 — Analyser les tickets

Traite les tickets de la liste « À analyser », dans l'ordre, jusqu'à atteindre `lot`.

Pour un ticket « non conforme » ou « modifié depuis l'analyse », commence par `python analyses.py reprendre --ticket <n>` : l'ancienne analyse est archivée et tu en écris une nouvelle, entièrement, à partir du ticket et des plans. Ne lis pas l'archive. Retoucher l'ancienne analyse pour faire disparaître les écarts n'est pas une reprise : le vérificateur maintient le signalement « à reprendre » tant que `reprendre` n'a pas été lancé.

Pour chaque ticket :

### a. Lire le ticket

1. Lis `tickets/<version>/<n>/ticket.md` en entier : en-tête, description, et tout l'historique.
2. Quand un commentaire renvoie à une capture (`!nom.png!`), ouvre-la dans `tickets/<version>/<n>/pieces_jointes/` si tu peux lire les images.
3. Repère dans l'historique les commentaires de test du pôle QA (« Test non validé », « NOK », « Ajouté au plan de validation »…) et les changements de statut qui les accompagnent.

### b. Situer le ticket dans les plans

Cette recherche est obligatoire pour tous les tickets, y compris de configuration ou de migration : une fiche existante peut devoir être mise à jour (version d'un logiciel tiers, procédure d'installation, machine de test), même quand aucune fiche n'est à créer.

1. Détermine l'application et les plans à consulter avec `referentiel/correspondance-fonctions.md`, en appliquant ses règles.
2. Cherche `#<n>` dans tous les fichiers de `referentiel/plans/`.
3. Cherche `#<n>` dans `referentiel/couverture-playwright.json` (clé `tickets`) : un test Playwright qui cite déjà le ticket se rapporte dans le paragraphe « Recherche dans les plans. », avec son fichier et son titre.
4. Cherche ensuite les mots-clés du sujet et de la description (nom du composant, du logiciel tiers, du paramètre) dans les plans proposés, puis lis en entier la ou les sections pertinentes.
5. Ouvre la section 3 de l'analyse par un paragraphe « **Recherche dans les plans.** » qui rapporte chaque recherche et son résultat : `#<n>` d'abord, puis chaque mot-clé, avec le plan, la fiche et le sous-titre trouvés, ou « aucune occurrence ». Ne cite dans « Sources » que les plans que tu as réellement lus et dont la section 3 rapporte le contenu. Ajouter un plan aux sources sans l'avoir exploité est une faute, même si le vérificateur le réclame.

### c. Qualifier le ticket

Chaque champ contrôlé de la fiche signalétique prend une seule des valeurs ci-dessous. Environnement peut en combiner plusieurs avec « + », la principale en premier. Aucune autre valeur n'est acceptée par `analyses.py verifier`.

| Champ | Valeurs autorisées |
|---|---|
| Application | WebApp · WinApp · Application mobile · Serveur et services · Transverse |
| Nature du test | Nouveau test · Re-test ciblé · Non-régression technique · Configuration d'environnement · Relecture documentaire · Hors campagne |
| Automatisabilité | Automatisable · Difficile · Impossible sans script externe · Hors outillage actuel · Non applicable |
| Environnement | WebApp · WinApp · Serveur / grille · Simulateur · Matériel · Mobile · Aucun |
| Confiance | Élevée · Moyenne · Faible |
| Décision humaine requise | Oui · Non |
| Issue | A — Reproduire l'existant · B — Adapter l'existant · C — Nouvelle procédure automatisable · D — Nouvelle procédure manuelle · Sans objet |

Repères :
1. **Application** : « Serveur et services » couvre les serveurs, processeurs, plugins, outils d'installation et de configuration ; « Transverse » couvre les bibliothèques et dépendances communes à plusieurs applications.
2. **Re-test ciblé** : le ticket a déjà été testé (commentaire QA dans l'historique ou `#<n>` présent au plan) et revient résolu. La procédure couvre en priorité les points signalés en échec, puis une vérification rapide du reste.
3. **Non-régression technique** et **Configuration d'environnement** : voir les règles 4 et 5 de la table de correspondance. La procédure vérifie le point précis corrigé ou mis en place par le ticket (par exemple l'erreur de démarrage décrite dans l'historique), pas seulement un fonctionnement général.
4. **Automatisabilité**, selon la grille du pôle QA et l'outillage actuel (Playwright, WebApp seulement) :
   - Automatisable : tout se fait dans le navigateur (WebApp), par un seul utilisateur. Un ticket serveur, WinApp ou mobile n'est jamais « Automatisable » ni « Difficile » ni « Impossible sans script externe » : il est « Hors outillage actuel ».
   - Difficile : plusieurs utilisateurs simultanés, attentes longues, données à préparer.
   - Impossible sans script externe : une étape sort du navigateur (fichier de configuration, grille, simulateur, IsapReporting).
   - Hors outillage actuel : WinApp, application mobile, serveur ou matériel, y compris les tickets de configuration et de non-régression technique.
   - Un ticket dont l'environnement comprend WebApp n'est jamais « Hors outillage actuel ». Si une étape sort du navigateur (attribut modifié dans IsapReporting, licence, script), il est « Impossible sans script externe ». Si rien ne se passe dans le navigateur (script SDK, envoi de courriel), l'environnement n'est pas WebApp.
   - Non applicable : relecture documentaire ou ticket hors campagne.
5. **Confiance** : Élevée seulement si le ticket dit clairement ce qui a été livré et comment l'observer. Moyenne si la procédure repose en partie sur des hypothèses. Faible si le ticket ne permet pas de savoir ce qui a été livré.

### b bis. Choisir l'issue

L'issue décide de ce que contient la section 4. Elle se choisit dans cet ordre, à partir de la recherche de l'étape b :

1. **Une fiche existante couvre la fonctionnalité du ticket ?** Lis-la en entier, puis écris en section 3 le paragraphe « **Comparaison des procédures.** » : même parcours, mêmes données, même résultat observé que ce que demande le ticket ? Point par point.
   - **Elle teste exactement la même chose : issue A — Reproduire l'existant.** Pas de nouvelle procédure. La section 4 s'ouvre par « **Procédure existante à rejouer.** », cite la fiche, le sous-titre et les étapes du plan, puis reprend ces étapes en lignes « - … Résultat attendu : … (#<n>) ». La section 5 indique seulement d'ajouter `#<n>` aux étapes rejouées.
   - **Elle couvre la fonctionnalité, mais pas de la même manière : issue B — Adapter l'existant.** La section 4 s'ouvre par « **Écarts avec la procédure existante.** » (étapes conservées, modifiées, ajoutées), puis donne la procédure adaptée.
2. **Aucune fiche ne couvre la fonctionnalité :** une nouvelle procédure est écrite à partir des prérequis du test.
   - **Tout se joue dans le navigateur (WebApp) : issue C — Nouvelle procédure automatisable.** La procédure est écrite pour être transcrite en test Playwright sans réinterprétation : une action par étape (clic, saisie, navigation), un résultat attendu vérifiable à l'écran (texte, élément, état).
   - **Une partie sort du navigateur : issue D — Nouvelle procédure manuelle.** La section 4 contient en plus le bloc « ### Prérequis et moyens » : matériel, simulateur, machine, accès, données, personne à solliciter.
3. **Relecture documentaire ou hors campagne : « Sans objet ».**

Pour toute procédure automatisable (issue C, et issue B quand l'automatisabilité est « Automatisable » ou « Difficile »), ajoute en fin de section 4 le bloc « ### Spécification Playwright », destiné au projet de campagne Playwright :

```
### Spécification Playwright

- Type : @lecture, @ecriture ou @perturbateur
- Compte : compte utilisé (Playwright, Operator, AA…)
- Dossier : dossier de travail (racine, A, AA…)
- Référentiel : données qui doivent exister avant le test, ou « Aucun »
- Données créées : ce que le test crée et devra supprimer, ou « Aucune »
```

`@lecture` ne modifie rien ; `@ecriture` crée ses propres données et les supprime ; `@perturbateur` modifie un état partagé (droits, options, mot de passe, alerte, hors ligne, purge serveur).

Le vérificateur contrôle la cohérence : A et B exigent une fiche existante et le paragraphe de comparaison ; C exige l'environnement WebApp et une automatisabilité « Automatisable » ou « Difficile » ; D l'interdit ; les blocs obligatoires doivent être présents et remplis.

### c bis. Désigner la fiche cible

« Fiche cible » reprend l'identifiant et le titre exacts de la fiche, tels qu'ils figurent dans le plan, sous la forme `INT03 — Tests avec simulateur`. Ne prends jamais la description de la fiche pour son titre. Pour une fiche sans identifiant, recopie son titre. Valeurs possibles sinon : « À décider » (question inscrite dans `decisions.md`), « À créer » ou « Aucune ». Le vérificateur contrôle que l'identifiant existe dans le plan cible, que le titre est le bon, que la section 5 nomme la fiche exactement de la même façon, et qu'aucune autre fiche du plan n'est présentée comme cible dans les sections 3 et 5.

### d. Rédiger l'analyse

Écris `analyses/<version>/<n>.md` en suivant la forme de `referentiel/modele-analyse.md`. Le modèle montre la forme attendue avec un exemple : toutes les valeurs sont à établir pour chaque ticket, rien n'est à recopier.

1. Première ligne : `<!-- ticket: <n> | mis à jour : … -->`, avec la valeur exacte du champ `updated_on` de `tickets/<version>/<n>/ticket.json`.
2. Les cinq sections numérotées suivent la méthode : étude du sujet, compte rendu de la situation, comparaison avec l'existant, procédure de test, intégration proposée.
3. Chaque étape de la procédure est une ligne commençant par « - », décrit une action, précise « Résultat attendu : » et se termine par `(#<n>)`. Une étape propre à un autre ticket appartient à l'analyse de cet autre ticket. Aucun identifiant ni mot de passe.
4. « Sources » liste les fichiers lus, dont au moins un plan de `referentiel/plans/` avec la section concernée.
5. Après avoir inscrit les éventuelles questions (étape e), lance `python analyses.py verifier --ticket <n>`. Corrige l'analyse jusqu'à obtenir « Aucun écart » avant de passer au ticket suivant.

### e. Reporter les questions

Pour chaque point ouvert, mets « Décision humaine requise » à « Oui ». Si la même question figure déjà dans `decisions.md` pour ce ticket, ne la répète pas. Sinon, inscris-la avec le script, jamais en écrivant toi-même dans `decisions.md` :

```
python analyses.py question --ticket <n> --question "Question fermée ?" --proposition "Ta proposition argumentée en une phrase."
```

Le script crée le fichier au bon format s'il n'existe pas.

### f. Journal

Inscris une ligne au journal avec le script :

```
python analyses.py journal --ticket <n> --texte "analysé — nature du test, fiche cible"
```

## Étape 3 — Synthèse

1. Lance `python analyses.py verifier` (sans `--ticket`). Corrige les écarts qui concernent les analyses de ce passage.
2. Lance `python analyses.py synthese` (avec `--version` si le paramètre est donné). Ne modifie pas `synthese.md` toi-même.
3. Lance `python analyses.py exporter`. Il écrit `export/<version>/campagne.json`, lu par le projet de campagne Playwright. Ne modifie jamais ce fichier toi-même.

## Conditions d'arrêt

Passe à l'étape 3 puis arrête-toi dès que :
- un script refuse un ticket parce que le lot est atteint ;
- la liste « À analyser » est vide ;
- deux tickets de suite ne peuvent pas être analysés (fichier absent ou illisible).

## Message de fin dans le chat

Six lignes au plus :
- le nombre de tickets analysés pendant ce passage et le nombre restant ;
- le nombre de décisions appliquées, le nombre en attente et les décisions non reconnues à reformuler ;
- les incidents de préparation (récupération, conversion des plans) ;
- le résultat de `python analyses.py verifier` ;
- le chemin de la synthèse ;
- la commande pour le passage suivant : `/analyser-tickets lot=8`.
