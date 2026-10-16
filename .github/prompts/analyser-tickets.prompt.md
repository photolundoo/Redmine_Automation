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
python analyses.py preparer
```

Elle récupère les tickets, convertit les plans modifiés et affiche l'état. Si la récupération échoue, elle s'arrête : arrête-toi aussi. Si `decisions.md` n'a pas le format attendu, lance `python analyses.py reparer-decisions`, puis `python analyses.py etat`.

La liste « À analyser » donne l'ordre de traitement : d'abord les décisions à appliquer, puis les analyses à reprendre, puis les nouvelles. Respecte cet ordre.

Lis ensuite une fois `referentiel/correspondance-fonctions.md` et `referentiel/modele-analyse.md`.

## Étape 1 — Appliquer les décisions de la relecture

Pour chaque ticket listé avec le motif « décision à appliquer » :

| Décision | Ce que tu fais dans l'analyse du ticket |
|---|---|
| `valider` | Rien à changer dans le contenu. |
| `corriger :` suivi d'un texte | Applique exactement la correction décrite, dans les sections concernées. |
| `fiche :` suivi d'une fiche | Remplace « Plan cible » et « Fiche cible » par la fiche indiquée, avec l'identifiant et le titre exacts du plan, puis reprends les sections 3 et 5 pour cette fiche. |
| `réanalyser` | Lance `python analyses.py reprendre --ticket <n>`, puis refais l'analyse complète (étape 2). |
| `hors campagne` | Mets « Nature du test » à « Hors campagne », « Automatisabilité » à « Non applicable », et ajoute la décision en tête de la section 5. |
| `ignorer` | Rien à changer. |

Puis :
1. Mets « Décision humaine requise » à « Non » si plus aucune question de ce ticket n'attend de décision.
2. Lance `python analyses.py appliquer --ticket <n>`. Le script contrôle l'analyse et date la décision ; tu n'écris jamais toi-même dans `decisions.md`. S'il refuse, corrige l'analyse et relance-le.

Les décisions signalées « non reconnues » par `etat` sont à reformuler par l'humain : ne les applique pas, ne les modifie pas, et cite-les dans le message de fin.

## Étape 2 — Analyser les tickets

Traite les tickets de la liste « À analyser », dans l'ordre, jusqu'à atteindre `lot`.

Pour un ticket « non conforme » ou « modifié depuis l'analyse », commence par `python analyses.py reprendre --ticket <n>` : l'ancienne analyse est archivée et tu en écris une nouvelle, entièrement, à partir du ticket et des plans. Ne lis pas l'archive. Retoucher l'ancienne analyse pour faire disparaître les écarts n'est pas une reprise.

Pour chaque ticket :

### a. Lire le ticket

1. Lis `tickets/<version>/<n>/ticket.md` en entier : en-tête, description, et tout l'historique.
2. Quand un commentaire renvoie à une capture (`!nom.png!`), ouvre-la dans `tickets/<version>/<n>/pieces_jointes/` si tu peux lire les images.
3. Repère dans l'historique les commentaires de test du pôle QA (« Test non validé », « NOK », « Ajouté au plan de validation »…) et les changements de statut qui les accompagnent.

### b. Situer le ticket dans les plans

Cette recherche est obligatoire pour tous les tickets, y compris de configuration ou de migration : une fiche existante peut devoir être mise à jour (version d'un logiciel tiers, procédure d'installation, machine de test), même quand aucune fiche n'est à créer.

1. Détermine l'application et les plans à consulter avec `referentiel/correspondance-fonctions.md`, en appliquant ses règles.
2. Cherche `#<n>` dans tous les fichiers de `referentiel/plans/`.
3. Cherche ensuite les mots-clés du sujet et de la description (nom du composant, du logiciel tiers, du paramètre) dans les plans proposés, puis lis en entier la ou les sections pertinentes.
4. Ouvre la section 3 de l'analyse par un paragraphe « **Recherche dans les plans.** » qui rapporte chaque recherche et son résultat : `#<n>` d'abord, puis chaque mot-clé, avec le plan, la fiche et le sous-titre trouvés, ou « aucune occurrence ». Ne cite dans « Sources » que les plans que tu as réellement lus et dont la section 3 rapporte le contenu. Ajouter un plan aux sources sans l'avoir exploité est une faute, même si le vérificateur le réclame.

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

Repères :
1. **Application** : « Serveur et services » couvre les serveurs, processeurs, plugins, outils d'installation et de configuration ; « Transverse » couvre les bibliothèques et dépendances communes à plusieurs applications.
2. **Re-test ciblé** : le ticket a déjà été testé (commentaire QA dans l'historique ou `#<n>` présent au plan) et revient résolu. La procédure couvre en priorité les points signalés en échec, puis une vérification rapide du reste.
3. **Non-régression technique** et **Configuration d'environnement** : voir les règles 4 et 5 de la table de correspondance. La procédure vérifie le point précis corrigé ou mis en place par le ticket (par exemple l'erreur de démarrage décrite dans l'historique), pas seulement un fonctionnement général.
4. **Automatisabilité**, selon la grille du pôle QA et l'outillage actuel (Playwright, WebApp seulement) :
   - Automatisable : tout se fait dans le navigateur (WebApp), par un seul utilisateur. Un ticket serveur, WinApp ou mobile n'est jamais « Automatisable » ni « Difficile » ni « Impossible sans script externe » : il est « Hors outillage actuel ».
   - Difficile : plusieurs utilisateurs simultanés, attentes longues, données à préparer.
   - Impossible sans script externe : une étape sort du navigateur (fichier de configuration, grille, simulateur, IsapReporting).
   - Hors outillage actuel : WinApp, application mobile, serveur ou matériel, y compris les tickets de configuration et de non-régression technique.
   - Non applicable : relecture documentaire ou ticket hors campagne.
5. **Confiance** : Élevée seulement si le ticket dit clairement ce qui a été livré et comment l'observer. Moyenne si la procédure repose en partie sur des hypothèses. Faible si le ticket ne permet pas de savoir ce qui a été livré.

### c bis. Désigner la fiche cible

« Fiche cible » reprend l'identifiant et le titre exacts de la fiche, tels qu'ils figurent dans le plan, sous la forme `INT03 — Tests avec simulateur`. Ne prends jamais la description de la fiche pour son titre. Pour une fiche sans identifiant, recopie son titre. Valeurs possibles sinon : « À décider » (question inscrite dans `decisions.md`), « À créer » ou « Aucune ». Le vérificateur contrôle que l'identifiant existe dans le plan cible et que le titre est le bon.

### d. Rédiger l'analyse

Écris `analyses/<version>/<n>.md` en suivant la forme de `referentiel/modele-analyse.md`. Le modèle montre la forme attendue avec un exemple : toutes les valeurs sont à établir pour chaque ticket, rien n'est à recopier.

1. Première ligne : `<!-- ticket: <n> | mis à jour : … -->`, avec la valeur exacte du champ `updated_on` de `tickets/<version>/<n>/ticket.json`.
2. Les cinq sections numérotées suivent la méthode : étude du sujet, compte rendu de la situation, comparaison avec l'existant, procédure de test, intégration proposée.
3. Chaque étape de la procédure est une ligne commençant par « - », décrit une action, précise « Résultat attendu : » et se termine par `(#<n>)`. Aucun identifiant ni mot de passe.
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

## Conditions d'arrêt

Passe à l'étape 3 puis arrête-toi dès que :
- `lot` tickets ont été analysés ;
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
