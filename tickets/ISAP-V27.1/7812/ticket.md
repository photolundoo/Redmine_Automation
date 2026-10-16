# #7812 — [Main Courante] Client léger spécifique à l'utilisation sur mobile V2

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | WebApp - Mobile |
| Catégorie | com.egidium.isap.gui.web |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Lucie Thomas |
| Avancement | 100 % |
| Créé le | 20/03/2024 16:11 |
| Mis à jour le | 14/10/2026 15:23 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Ville de Paris |
| Projet 2 à livrer | Produit |
| Release notes | Oui |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/7812 |

## Description

~~~textile
Voir #7643 pour plus de détail mais selon moi le plus important dans le Reste à faire est :
* Trop facile de créer un incident par erreur et tapant sur le +. Il faudrait une popup de confirmation
* Consultation des pièces jointes: Pas de dézoom possible
~~~

## Relations

- Liée à #5975
- Liée à #7643

## Pièces jointes

- [clipboard-202602031520-ohjou.png](pieces_jointes/clipboard-202602031520-ohjou.png) — 21 Ko, ajoutée par Lucie Thomas le 03/02/2026 15:20
- [clipboard-202609161505-zu1sd.png](pieces_jointes/clipboard-202609161505-zu1sd.png) — 35 Ko, ajoutée par Lucie Thomas le 16/09/2026 15:05
- [clipboard-202609161506-sfkws.png](pieces_jointes/clipboard-202609161506-sfkws.png) — 15 Ko, ajoutée par Lucie Thomas le 16/09/2026 15:06
- [clipboard-202610021554-2kz66.png](pieces_jointes/clipboard-202610021554-2kz66.png) — 211 Ko, ajoutée par Lucie Thomas le 02/10/2026 15:54

## Historique

### 20/03/2024 16:11 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V5.6.2

### 03/05/2024 13:43 — Fernand Alcatrao

- Début : (vide) → 06/05/2024

~~~textile
C'est pas le plus urgent si compliqué à faire (Le plus urgent = les Runsheets par places).
Mais si simple, ce serait sympas de voir les photos attachées.
~~~

### 06/05/2024 15:46 — Vincent Tellier

~~~textile
Le formulaire de création d'incident sur les champs obligatoire sert de validation
~~~

### 07/05/2024 16:37 — Vincent Tellier

~~~textile
Des tests pour le zoom mais ca me semble complexe. Je vais voir pour tester une librairie externe
~~~

### 22/05/2024 09:23 — Thibaut Wiart

- Fonction : ISAP Core - Main Courante → WebApp - Main Courante

### 03/06/2024 10:20 — Alan Raynaud

- Relation ajoutée (liée à) : #5975

### 26/06/2024 09:07 — Thibaut Wiart

- Fonction : WebApp - Main Courante → WebApp - Mobile

### 07/10/2024 13:56 — Alan Raynaud

- Version cible : ISAP-V5.6.2 → Candidate for next major release

### 07/02/2025 13:15 — Fernand Alcatrao

- Ticket parent : #7620 → (vide)

~~~textile
Je retire du macro case VdP JOP 2024
~~~

### 27/01/2026 10:04 — Alan Raynaud

- Relation ajoutée (liée à) : #7643

### 27/01/2026 10:05 — Fernand Alcatrao

- Assigné à : Vincent Tellier → Lucie Thomas

### 27/01/2026 10:16 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V27.1

### 03/02/2026 13:51 — Lucie Thomas

~~~textile
Est-ce qu'on peut définir le besoin plus en détail ?
~~~

### 03/02/2026 14:31 — Alan Raynaud

~~~textile
Lucie Thomas a écrit  (#note-13):
> Est-ce qu'on peut définir le besoin plus en détail ?

Vu avec Lucie, à noter que le problème de création accidentelle d'incident ne se produit que si l'on désactive le droit de créer des mentions.
~~~

### 03/02/2026 15:20 — Lucie Thomas

- Pièce jointe ajoutée : clipboard-202602031520-ohjou.png
- Avancement : 0 % → 50 %

~~~textile
Moitié du case réalisé, si qu'un des deux droits (incident/mention) est présent, on a quand même le même fonctionnement qu'avec les deux droits
!clipboard-202602031520-ohjou.png!
~~~

### 16/02/2026 09:36 — Lucie Thomas

- Avancement : 50 % → 90 %

~~~textile
Zoom fonctionnel.
~~~

### 24/02/2026 10:11 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 05/05/2026 13:57 — Lucie Thomas

~~~textile
bouton caméra ouvre la caméra sur l'application mobile
~~~

### 16/09/2026 15:07 — Lucie Thomas

- Pièce jointe ajoutée : clipboard-202609161505-zu1sd.png
- Pièce jointe ajoutée : clipboard-202609161506-sfkws.png
- Evolution majeure : (vide) → 0

~~~textile
Question, est-ce que le bouton pour ajouter des pièces jointes dans le détail des incidents doit proposer d'ouvrir la caméra ? actuellement nous avons qui ouvre la caméra :
!clipboard-202609161505-zu1sd.png!


Est-ce qu'on veut le même comportement ici :
!clipboard-202609161506-sfkws.png!
~~~

### 02/10/2026 15:54 — Lucie Thomas

- Pièce jointe ajoutée : clipboard-202610021554-2kz66.png

~~~textile
!clipboard-202610021554-2kz66.png!
~~~

### 06/10/2026 16:31 — Fernand Alcatrao

~~~textile
RàF ? Ou résolu ?
~~~

### 14/10/2026 15:23 — Lucie Thomas

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %
