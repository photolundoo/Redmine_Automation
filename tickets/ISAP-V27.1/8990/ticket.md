# #8990 — Crash applicatif si la licence contient une limite non reconnue

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Core - SDK |
| Catégorie | com.egidium.licensing |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8986 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 31/07/2026 13:40 |
| Mis à jour le | 04/08/2026 16:37 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V5.5.1 |
| Release notes | Oui |
| Lien Redmine | https://srvfr-redmine/issues/8990 |

## Description

~~~textile
Recompilations nécessaires :
* La dll StaticLicenseChecker.dll
* Les applicatifs qui utilisent les fonctions de plus bas niveau pour vérifier les éléments de licence exacts 
** APIServer
** DBImporter
** Emulator
** Importer3D
** IsapReportingServer
** Isap3DGUI
** UAEUpdater
~~~

## Relations

- Liée à #8551
- Liée à #7903

## Historique

### 31/07/2026 14:04 — Alan Raynaud

- Relation ajoutée (liée à) : #8551

### 31/07/2026 14:12 — Alan Raynaud

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 31/07/2026 14:17 — Alan Raynaud

- Relation ajoutée (liée à) : #7903

### 31/07/2026 16:03 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 80 %

### 31/07/2026 16:04 — Alan Raynaud

~~~textile
Reste à recompiler :
* DBImporter
* Emulator
* Importer3D
* Isap3DGUI
* UAEUpdater
~~~

### 03/08/2026 13:06 — Guillaume Lemaitre

- Statut : Résolu → Fermé

### 03/08/2026 13:23 — Alan Raynaud

- Statut : Fermé → En cours

### 04/08/2026 16:38 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 80 % → 100 %
