# #8966 — Iris : Lecture de mail HS pour curl < 7.62

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Fonctions - Iris |
| Catégorie | com.egidium.iris |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8955 |
| Auteur | Alan Raynaud |
| Assigné à | Fernand Alcatrao |
| Avancement | 100 % |
| Créé le | 22/07/2026 13:52 |
| Mis à jour le | 18/09/2026 14:37 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V27.1 |
| Lien Redmine | https://srvfr-redmine/issues/8966 |

## Description

~~~textile
Causé par un bug résolu sous curl 7.62

Or, le package curl disponible sous VS2019 via Nuget est curl 7.59
~~~

## Pièces jointes

- [clipboard-202607231006-xl2nu.png](pieces_jointes/clipboard-202607231006-xl2nu.png) — 11 Ko, ajoutée par Alan Raynaud le 23/07/2026 10:06
- [clipboard-202607231006-eivd8.png](pieces_jointes/clipboard-202607231006-eivd8.png) — 137 Ko, ajoutée par Alan Raynaud le 23/07/2026 10:06

## Historique

### 23/07/2026 10:05 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
Contournement : 
* Sous Windows, utiliser les ID séquentiels
* Sous Linux : utiliser les UID
~~~

### 23/07/2026 10:06 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202607231006-xl2nu.png
- Pièce jointe ajoutée : clipboard-202607231006-eivd8.png

~~~textile
!clipboard-202607231006-xl2nu.png!


!clipboard-202607231006-eivd8.png!
~~~

### 31/07/2026 16:27 — Fernand Alcatrao

- Version source : ISAP-V26.1 → ISAP-V27.1

### 12/08/2026 10:49 — Alan Raynaud

- Sujet : « Iris : Lecture de mail HS sous Windows » → « Iris : Lecture de mail HS pour curl < 7.62 »
- Statut : Résolu → En cours

~~~textile
Problème également rencontré sous Linux car la version utilisée sur vmsfr-jenkins est une 7.47
~~~

### 12/08/2026 10:55 — Alan Raynaud

- Assigné à : Alan Raynaud → Fernand Alcatrao
- Avancement : 100 % → 90 %

~~~textile
Reste à relivrer Linux
~~~

### 12/08/2026 13:43 — Fernand Alcatrao

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %

### 18/09/2026 14:37 — Fernand Alcatrao

- Fonction : ISAP Core - SDK → ISAP Fonctions - Iris
