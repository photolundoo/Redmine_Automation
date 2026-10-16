# #9063 — [ServerSetup] L'option "début différé" n'est pas prise en compte pour tous les services

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | ISAP Core - Administration |
| Catégorie | com.egidium.installer |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 15/09/2026 17:27 |
| Mis à jour le | 22/09/2026 16:46 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V25.1 |
| Release notes | Oui |
| Lien Redmine | https://srvfr-redmine/issues/9063 |

## Description

~~~textile
!clipboard-202609151723-dehcf.png!

Sur le poste client, semble OK:
!clipboard-202609151726-n9a5m.png!

Je le rajoute dans la RN 25.1
~~~

## Pièces jointes

- [clipboard-202609151723-dehcf.png](pieces_jointes/clipboard-202609151723-dehcf.png) — 43 Ko, ajoutée par Fernand Alcatrao le 15/09/2026 17:23
- [clipboard-202609151726-n9a5m.png](pieces_jointes/clipboard-202609151726-n9a5m.png) — 3 Ko, ajoutée par Fernand Alcatrao le 15/09/2026 17:26

## Historique

### 15/09/2026 17:36 — Alan Raynaud

~~~textile
Pour les services hors-grid, il semble que l'installeur les passe en début différé puis en début auto.
~~~

### 15/09/2026 17:37 — Alan Raynaud

- Avancement : 0 % → 90 %

### 22/09/2026 16:46 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 90 % → 100 %

~~~textile
A tester à l'occasion d'une installation serveur : vérifier que si l'option "démarrage différé" est selectionnée, tous les services Smart Shield sont bien en démarrage différé.
~~~
