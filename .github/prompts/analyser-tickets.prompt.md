---
description: Analyser les tickets Redmine de la version selon la méthode en 5 étapes et préparer la campagne de test
agent: agent
---

# /analyser-tickets

Tu analyses les tickets Redmine de la version en cours, un par un, selon la méthode en 5 étapes du pôle QA. Tu travailles sans poser de question : ce que tu ne peux pas trancher va dans `decisions.md`. Respecte les règles de `.github/copilot-instructions.md`.

## Paramètres

Lis-les dans le message qui suit la commande. Valeurs par défaut entre parenthèses.

- `lot=` nombre maximal de tickets analysés pendant ce passage (8).
- `ticket=` numéro d'un ticket à analyser ou réanalyser, même si son analyse est à jour. Dans ce cas, seul ce ticket est traité.
- `version=` dossier de version dans `tickets/` (la seule version présente).

Dans la suite, `<version>` désigne ce dossier, par exemple `ISAP-V27.1`, et `<n>` le numéro du ticket traité. Remplace toujours ces repères par les valeurs réelles : ne les écris jamais tels quels dans un fichier.

## Étape 0 — Préparation

1. Lance `python recuperer_tickets.py`. En cas d'échec, écris la cause dans le journal et arrête-toi : sans tickets à jour, l'analyse n'a pas de sens.
2. Lance `python convertir_plans.py`. En cas d'échec, continue avec les plans déjà présents dans `referentiel/plans/` et signale-le dans le message de fin. Si ce dossier est vide, arrête-toi.
3. Lance `python analyses.py etat` (ajoute `--version` si le paramètre est donné). La liste « À analyser » donne l'ordre de traitement.
4. Lis une fois `referentiel/correspondance-fonctions.md` et `referentiel/modele-analyse.md`.

## Étape 1 — Appliquer les décisions de la relecture

Ouvre `analyses/<version>/decisions.md` s'il existe. Pour chaque ligne dont la colonne « Décision » est remplie et la colonne « Appliquée le » est vide :

| Décision | Ce que tu fais dans l'analyse du ticket |
|---|---|
| `valider` | Rien à changer dans le contenu. |
| `corriger :` suivi d'un texte | Applique exactement la correction décrite, dans les sections concernées. |
| `fiche :` suivi d'une fiche | Remplace « Plan cible » et « Fiche cible », puis reprends les sections 3 et 5 pour cette fiche. |
| `réanalyser` | Refais l'analyse complète du ticket (étape 2). |
| `hors campagne` | Mets « Nature du test » à « Hors campagne » et ajoute la décision en tête de la section 5. |
| `ignorer` | Rien à changer. |

Puis :
1. Mets « Décision humaine requise » à « Non » si plus aucune ligne de ce ticket n'attend de décision.
2. Inscris la date du jour au format JJ/MM/AAAA dans la colonne « Appliquée le ».
3. Une décision qui ne correspond à aucune forme du tableau reste telle quelle : signale-la dans le message de fin.

## Étape 2 — Analyser les tickets

Traite les tickets de la liste « À analyser », dans l'ordre, jusqu'à atteindre `lot`. Pour chaque ticket :

### a. Lire le ticket

1. Lis `tickets/<version>/<n>/ticket.md` en entier : en-tête, description, et tout l'historique.
2. Quand un commentaire renvoie à une capture (`!nom.png!`), ouvre-la dans `tickets/<version>/<n>/pieces_jointes/` si tu peux lire les images.
3. Repère dans l'historique les commentaires de test du pôle QA (« Test non validé », « NOK », « Ajouté au plan de validation »…) et les changements de statut qui les accompagnent.

### b. Situer le ticket

1. Détermine l'application et les plans à consulter avec `referentiel/correspondance-fonctions.md`, en appliquant ses règles.
2. Cherche `#<n>` dans tous les fichiers de `referentiel/plans/`.
3. Cherche ensuite les mots-clés du sujet et de la description dans les plans proposés, puis lis en entier la ou les sections pertinentes.

### c. Qualifier le ticket

Chaque champ contrôlé de la fiche signalétique prend une seule des valeurs ci-dessous (Environnement peut en combiner plusieurs avec « + », la principale en premier).

| Champ | Valeurs autorisées |
|---|---|
| Nature du test | Nouveau test · Re-test ciblé · Non-régression technique · Configuration d'environnement · Relecture documentaire · Hors campagne |
| Automatisabilité | Automatisable · Difficile · Impossible sans script externe · Hors outillage actuel · Non applicable |
| Environnement | WebApp · WinApp · Serveur / grille · Simulateur · Matériel · Mobile · Aucun |
| Confiance | Élevée · Moyenne · Faible |
| Décision humaine requise | Oui · Non |

Repères :
1. **Re-test ciblé** : le ticket a déjà été testé (commentaire QA dans l'historique ou `#<n>` présent au plan) et revient résolu. La procédure couvre en priorité les points signalés en échec, puis une vérification rapide du reste.
2. **Non-régression technique** et **Configuration d'environnement** : voir les règles 4 et 5 de la table de correspondance. La procédure se limite aux vérifications propres au ticket (version installée, service démarré, absence d'erreur au démarrage).
3. **Automatisabilité**, selon la grille du pôle QA et l'outillage actuel (Playwright, WebApp seulement) :
   - Automatisable : tout se fait dans le navigateur, par un seul utilisateur.
   - Difficile : plusieurs utilisateurs simultanés, attentes longues, données à préparer.
   - Impossible sans script externe : une étape sort du navigateur (fichier de configuration, grille, simulateur, IsapReporting).
   - Hors outillage actuel : WinApp, application mobile ou matériel.
   - Non applicable : relecture ou ticket hors campagne.
4. **Confiance** : Faible dès que le ticket ne permet pas de savoir ce qui a été livré ou comment l'observer.

### d. Rédiger l'analyse

Écris `analyses/<version>/<n>.md` en suivant la forme de `referentiel/modele-analyse.md`. Le modèle montre la forme attendue avec un exemple : toutes les valeurs sont à établir pour chaque ticket, rien n'est à recopier.

1. Première ligne : `<!-- ticket: <n> | mis à jour : … -->`, avec la valeur exacte du champ `updated_on` de `tickets/<version>/<n>/ticket.json`. C'est elle qui permet de savoir si l'analyse est à jour.
2. Les cinq sections numérotées suivent la méthode : étude du sujet, compte rendu de la situation, comparaison avec l'existant, procédure de test, intégration proposée.
3. La procédure de test suit les règles de rédaction des instructions du projet. Aucun identifiant ni mot de passe.
4. « Sources » liste les fichiers lus, avec la section du plan concernée.

### e. Reporter les questions

Pour chaque point ouvert, ajoute une ligne à la fin du tableau de `analyses/<version>/decisions.md`, et mets « Décision humaine requise » à « Oui ». Si le fichier n'existe pas, crée-le avec exactement cet en-tête, en remplaçant le titre par la version :

```
# Décisions à prendre — ISAP-V27.1

Remplir la colonne « Décision » avec l'une des formes suivantes, puis relancer `/analyser-tickets` :
- `valider` : la proposition de l'agent est retenue ;
- `corriger :` suivi de la correction, par exemple `corriger : la procédure doit aussi couvrir le mode Rejeu` ;
- `fiche :` suivi de la fiche à retenir, par exemple `fiche : MC02 Onglet Main Courante` ;
- `réanalyser` : l'agent refait l'analyse complète du ticket ;
- `hors campagne` : le ticket n'est pas testé dans cette campagne ;
- `ignorer` : la question est sans objet.

| Ticket | Question | Proposition de l'agent | Décision | Appliquée le |
|---|---|---|---|---|
```

Chaque ligne : le ticket sous la forme `#<n>`, une question fermée, ta proposition argumentée en une phrase, puis deux cellules vides. N'écris jamais le caractère `|` dans une cellule.

### f. Journal

Ajoute une ligne à `analyses/<version>/journal.md` : `- AAAA-MM-JJ HH:MM — #<n> analysé — <nature du test>, <fiche cible>`, en remplaçant les repères.

## Étape 3 — Synthèse

Lance `python analyses.py synthese` (avec `--version` si le paramètre est donné). Ne modifie pas `synthese.md` toi-même.

## Conditions d'arrêt

Passe à l'étape 3 puis arrête-toi dès que :
- `lot` tickets ont été analysés ;
- la liste « À analyser » est vide ;
- deux tickets de suite ne peuvent pas être analysés (fichier absent ou illisible).

## Message de fin dans le chat

Six lignes au plus :
- le nombre de tickets analysés pendant ce passage et le nombre restant ;
- le nombre de décisions appliquées et le nombre de décisions en attente ;
- les incidents de préparation (récupération, conversion des plans) ;
- le chemin de la synthèse ;
- la commande pour le passage suivant : `/analyser-tickets lot=8`.
