# #9075 — Simulateur SIA : envoyer les messages vers un recepteur secondaire

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Plugins - Capteurs experts |
| Catégorie | com.egidium.sia |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 22/09/2026 13:56 |
| Mis à jour le | 22/09/2026 13:59 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Release notes | Non |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9075 |

## Description

(aucune description)

## Pièces jointes

- [clipboard-202609221357-3xagi.png](pieces_jointes/clipboard-202609221357-3xagi.png) — 56 Ko, ajoutée par Alan Raynaud le 22/09/2026 13:57

## Historique

### 22/09/2026 13:58 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202609221357-3xagi.png

~~~textile
Il est désormais possible de préciser un recepteur secondaire :
!clipboard-202609221357-3xagi.png!

Dans ce cas d'illustration :
* Recepteur primaire : en local
* Recepteur secondaire : avignon
~~~

### 22/09/2026 13:59 — Alan Raynaud

~~~textile
Pour tester :
* Démo ACME sur deux postes différents
* Plugin SIA CSR activé sur les deux postes (dont parefeu autorisant les connexion UDP 10001)
* Utiliser le simulateur pour envoyer une alarme sur les deux systèmes en même temps
~~~

### 22/09/2026 13:59 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %
