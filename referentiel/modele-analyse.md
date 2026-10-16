<!-- ticket: 8887 | mis à jour : 2026-10-13T14:10:53Z -->
# Analyse #8887 — WebApp : Permettre une utilisation de la vidéo sans Joystick

## Fiche signalétique

| Champ | Valeur |
|---|---|
| Fonction Redmine | WebApp - Video |
| Application | WebApp |
| Module | Vidéo |
| Plan cible | 01 WebApp |
| Fiche cible | MC06 — Onglet Vidéo |
| Nature du test | Re-test ciblé |
| Automatisabilité | Automatisable |
| Environnement | WebApp |
| Prérequis particuliers | Plugin CCTV lancé, caméra PTZ (Atlantique) |
| Issue | B — Adapter l'existant |
| Confiance | Élevée |
| Décision humaine requise | Non |

## 1. Étude du sujet

(Ce que demande le ticket, en deux à cinq phrases, à partir de la description et des commentaires.)

## 2. Compte rendu de la situation

**Tenants.** (Contexte, origine de la demande, contraintes connues.)

**Aboutissants.** (Ce qui a été livré, d'après le dernier état du ticket.)

**Objectifs du test.** (Ce que la campagne doit établir, en une à trois phrases.)

## 3. Comparaison avec l'existant

**Recherche dans les plans.** `#8887` : trouvé dans le plan 01, fiche MC06 « Onglet Vidéo », sous-titre « Live ». « joystick » : plan 03, fiche WVID07 « Tests Joystick » (WinApp, hors sujet ici). (Chaque recherche effectuée et son résultat, y compris quand elle ne donne rien.)

**Comparaison des procédures.** (Issues A et B seulement. Confronter, point par point, ce que teste la fiche existante et ce que demande le ticket : même parcours, mêmes données, même résultat observé ? Ce qui est identique, ce qui diffère, ce qui manque. C'est ce paragraphe qui justifie A plutôt que B.)

**Issue retenue.** (Une phrase : A, B, C ou D, et pourquoi.)

## 4. Procédure de test proposée

**Écarts avec la procédure existante.** (Issue B : étapes de la fiche conservées, modifiées, ajoutées. Issue A : remplacer ce paragraphe par « **Procédure existante à rejouer.** » suivi de la fiche, du sous-titre et des étapes du plan à exécuter telles quelles.)

**Sous-titre de la procédure**
- Action à réaliser. Résultat attendu : comportement observable. (#8887)
- Action suivante. Résultat attendu : comportement observable. (#8887)

### Spécification Playwright

(Obligatoire pour l'issue C, et pour l'issue B quand l'automatisabilité est « Automatisable » ou « Difficile ». Une ligne par champ, valeurs « Aucun » ou « Aucune » si rien.)

- Type : @lecture
- Compte : Playwright
- Dossier : racine
- Référentiel : caméra PTZ Atlantique déclarée, plugin CCTV lancé
- Données créées : Aucune

### Prérequis et moyens

(Obligatoire pour l'issue D, à supprimer sinon. Tout ce qu'il faut réunir avant de jouer la procédure : matériel, simulateur, machine, accès, données, personne à solliciter.)

- Élément nécessaire et où le trouver.

## 5. Intégration proposée

(Où et comment intégrer la procédure : plan, fiche, sous-titre, position par rapport aux étapes existantes. Nouvelle fiche, ajout d'étapes, ou modification d'étapes existantes, en citant celles à modifier. Issue A : indiquer seulement d'ajouter le numéro du ticket aux étapes rejouées.)

## Points ouverts

(Questions que le ticket ne permet pas de trancher. Chaque point est reporté dans decisions.md. « Aucun » s'il n'y en a pas.)

## Sources

- tickets/ISAP-V27.1/8887/ticket.md
- referentiel/plans/01 V26.1 - WEBAPP.md — section « Onglet Vidéo - [MC06] »
