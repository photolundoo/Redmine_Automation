# #8183 — Pictogrammes des Sensor de type Sprinkler

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Plugins - Détection Incendie |
| Catégorie | com.egidium.isap.gui |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Pascal Vognin |
| Avancement | 100 % |
| Créé le | 14/11/2024 16:01 |
| Mis à jour le | 08/10/2026 15:25 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Release notes | Oui |
| Description release notes | Des pictogrammes sont désormais fournis pour le SensorType SPK (Sprinkler).    Sur les installation existantes, il faut effacer les pictogrammes auto-générés en supprimant le dossier @%EGIDIUM_DATA%\com.egidium.shared\public\data\Pictogram\Sensor\SPK@ (*attention* : il s'agit bien du dossier dans @%EGIDIUM_DATA%@, par défaut @C:\ProgramData\EGIDIUM Technologies\@ et non pas @%EGDIDIUM_HOME%@) |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8183 |

## Description

~~~textile
Sur une centrale Finsecure, les sprinklers peuvent avoir les états suivants :
* Nominal
* Alarme
* Défaut
* Hors-service

Dans SmartShield, il manque la représentation du capteur en l'état défaut. Même lorsque l'attribut @Failure@ passe à @True@, le capteur ne change pas de représentation.
~~~

## Pièces jointes

- [clipboard-202602031339-oajd3.png](pieces_jointes/clipboard-202602031339-oajd3.png) — 7 Ko, ajoutée par Alan Raynaud le 03/02/2026 13:39
- [clipboard-202603111358-szwbn.png](pieces_jointes/clipboard-202603111358-szwbn.png) — 28 Ko, ajoutée par Guillaume Lemaitre le 11/03/2026 13:58
- [clipboard-202610081456-qqfzc.png](pieces_jointes/clipboard-202610081456-qqfzc.png) — 5 Ko, ajoutée par Alan Raynaud le 08/10/2026 14:56
- [clipboard-202610081456-wi6z6.png](pieces_jointes/clipboard-202610081456-wi6z6.png) — 31 Ko, ajoutée par Alan Raynaud le 08/10/2026 14:56
- [clipboard-202610081500-tzkux.png](pieces_jointes/clipboard-202610081500-tzkux.png) — 28 Ko, ajoutée par Alan Raynaud le 08/10/2026 15:00

## Historique

### 14/11/2024 16:01 — Alan Raynaud

- Relation ajoutée (bloque) : #8099

### 07/03/2025 13:55 — Fernand Alcatrao

- Relation supprimée (bloque) : #8099

### 17/07/2025 17:19 — Rodrigue Favrot

- Temps estimé : (vide) → 4.0 h

### 07/08/2025 15:51 — Fernand Alcatrao

- Début : (vide) → 07/08/2025

~~~textile
QuickWin pour 25.1
~~~

### 08/09/2025 14:34 — Alan Raynaud

- Assigné à : Rodrigue Favrot → 57

### 02/02/2026 14:30 — Alan Raynaud

- Version cible : ISAP-V25.1 → ISAP-V27.1

### 03/02/2026 13:39 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202602031339-oajd3.png
- Sujet : « Pictogramme d'état de panne des Sensor de type Sprinkler » → « Pictogrammes des Sensor de type Sprinkler »

~~~textile
Après vérification, nous n'avons pas de picto Sprinkler. En l'état actuel, on affiche uniquement un picto avec "SPK" :

!clipboard-202602031339-oajd3.png!
~~~

### 13/02/2026 17:13 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
C:\DEV\EGIDIUM\com.egidium.shared\public\data\Pictogram\Sensor\SPK
~~~

### 24/02/2026 10:00 — Fernand Alcatrao

- Version cible : ISAP-V27.1 → ISAP-V25.1
- Release notes : (vide) → Oui

### 11/03/2026 14:11 — Guillaume Lemaitre

- Pièce jointe ajoutée : clipboard-202603111358-szwbn.png
- Statut : Résolu → Fermé

~~~textile
Test validé - Vérification de l'ajout du pictogramme SPK

!clipboard-202603111358-szwbn.png!

Ajouté au plan de validation 25.1 - WA
~~~

### 16/03/2026 14:55 — Alan Raynaud

- Description release notes : (vide) → Des pictogrammes sont désormais fournis pour le SensorType SPK (Sprinkler)

### 21/04/2026 14:03 — Guillaume Lemaitre

- Statut : Fermé → En cours
- Avancement : 100 % → 50 %

~~~textile
Rouvert suite aux test du plan de validation, les nouveaux pictogrammes SPK ne sont pas pris en compte
~~~

### 27/04/2026 13:52 — Alan Raynaud

- Assigné à : 57 → Alan Raynaud

### 23/06/2026 13:41 — Alan Raynaud

- Version cible : ISAP-V25.1 → ISAP-V27.1

### 08/10/2026 14:56 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202610081456-qqfzc.png
- Pièce jointe ajoutée : clipboard-202610081456-wi6z6.png
- Evolution majeure : (vide) → 0

~~~textile
Effectivement NOK alors que les pictos existent....

!clipboard-202610081456-qqfzc.png!

!clipboard-202610081456-wi6z6.png!
~~~

### 08/10/2026 15:00 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202610081500-tzkux.png
- Assigné à : Alan Raynaud → Pascal Vognin

~~~textile
L'IHM semble auto-générer au lancement des pictogrammes SPK même si des "vrai" pictogrammes sont déjà fournis.

Comportement de l'IHM à analyser pour voir s'il y a un truc en dur pour le SensorType SPK

!clipboard-202610081500-tzkux.png!
~~~

### 08/10/2026 15:25 — Alan Raynaud

- Description release notes : Des pictogrammes sont désormais fournis pour le SensorType SPK (Sprinkler) → Des pictogrammes sont désormais fournis pour le SensorType SPK (Sprinkler).

Sur les installation existantes, il faut effacer les pictogrammes auto-générés en supprimant le dossier @%EGIDIUM_DATA%\com.egidium.shared\public\data\Pictogram\Sensor\SPK@ (*attention* : il s'agit bien du dossier dans @%EGIDIUM_DATA%@, par défaut @C:\ProgramData\EGIDIUM Technologies\@ et non pas @%EGDIDIUM_HOME%@)

~~~textile
OK, il fallait corriger la génération auto.

Pour tester : commencer par bien lire ce qui est indiqué en release note.
~~~

### 08/10/2026 15:25 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 50 % → 100 %
