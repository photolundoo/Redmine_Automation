# #6017 — Migrer vers ImageMagick++ 7.1.2

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Plugins - Cameras & Encodeurs |
| Catégorie | com.egidium.video |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 23/10/2020 11:49 |
| Mis à jour le | 21/10/2026 14:57 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Release notes | Non |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/6017 |

## Description

~~~textile
* Lister les plugin utilisant ImageMagick
* Les recompiler + tester avec la dernière version
* Trouver comment livrer le runtime ImageMagick
~~~

## Relations

- Liée à #5958
- Liée à #6135
- Liée à #9022
- Bloque #8994
- Bloque #6918

## Pièces jointes

- [clipboard-202610191043-w2au2.png](pieces_jointes/clipboard-202610191043-w2au2.png) — 4 Ko, ajoutée par Pascal Vognin le 19/10/2026 10:43

## Historique

### 23/10/2020 11:49 — Alan Raynaud

- Relation ajoutée (liée à) : #5958

### 26/10/2020 09:36 — Thibaut Wiart

- Sujet : « Migrer vers la dernière version d'ImageMagcik » → « Migrer vers la dernière version d'ImageMagick »

### 02/12/2020 06:35 — Fernand Alcatrao

- Version cible : ISAP-V5.3.1 → ISAP-V5.3.2

### 01/02/2021 10:25 — Alan Raynaud

- Relation ajoutée (liée à) : #6135

### 01/02/2021 10:25 — Alan Raynaud

- Début : 26/10/2020 → 15/02/2021

### 23/03/2021 15:14 — Fernand Alcatrao

- Version cible : ISAP-V5.3.2 → ISAP-V5.4.0

### 07/07/2021 09:45 — Thibaut Wiart

- Release notes : (vide) → Non

### 21/09/2021 10:36 — Fernand Alcatrao

- Version cible : ISAP-V5.4.0 → ISAP-V5.4.1

### 22/09/2021 14:29 — Thibaut Wiart

- Priorité : Haut → Bas

### 22/11/2021 10:07 — Alan Raynaud

- Version cible : ISAP-V5.4.1 → ISAP-V5.5.0

### 13/12/2021 10:40 — Alan Raynaud

- Début : 15/02/2021 → 01/02/2022

### 31/01/2022 10:18 — Alan Raynaud

- Début : 01/02/2022 → 07/02/2022

### 07/03/2022 10:29 — Alan Raynaud

- Version cible : ISAP-V5.5.0 → ISAP-V5.5.1

### 16/05/2022 10:10 — Alan Raynaud

- Début : 07/02/2022 → (vide)

### 29/06/2022 13:07 — Thibaut Wiart

- Version cible : ISAP-V5.5.1 → Candidate for next major release

### 31/07/2026 16:48 — Pascal Vognin

- Relation ajoutée (bloque) : #8994

### 22/09/2026 11:14 — Pascal Vognin

- Relation ajoutée (liée à) : #6918

### 22/09/2026 11:17 — Alan Raynaud

- Relation supprimée (liée à) : #6918

### 22/09/2026 11:17 — Alan Raynaud

- Relation ajoutée (bloque) : #6918

### 22/09/2026 11:18 — Alan Raynaud

- Priorité : Bas → Urgent
- Version cible : Candidate for next major release → ISAP-V27.1
- Début : (vide) → 23/09/2026
- Evolution majeure : (vide) → 0

~~~textile
La version actuellement utilisée n'est pas compatible C++20.
~~~

### 25/09/2026 11:11 — Alan Raynaud

- Sujet : « Migrer vers la dernière version d'ImageMagick » → « Migrer vers ImageMagick 7.1.2 »

### 25/09/2026 13:24 — Alan Raynaud

- Statut : Nouveau → En cours

### 25/09/2026 13:29 — Alan Raynaud

~~~textile
Dépendances C++ :
* genericrecorderplugin
* sensorrepresentationprocessor
* utf8-labelgenerator
* indigovisionplugin
~~~

### 25/09/2026 14:02 — Alan Raynaud

- Sujet : « Migrer vers ImageMagick 7.1.2 » → « Migrer vers ImageMagick++ 7.1.2 »

### 25/09/2026 16:32 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 0 % → 100 %

### 06/10/2026 11:17 — Alan Raynaud

- Statut : Résolu → En cours

~~~textile
NOK pour utf8-labelgenerator
~~~

### 06/10/2026 11:17 — Alan Raynaud

- Avancement : 100 % → 60 %

### 06/10/2026 11:23 — Alan Raynaud

~~~textile
Deux soucis :
* Le calcul de dépendance ne détecte pas que vsnSystem dépend de UTF8Generator, donc la lib UTF8 generator apparait comme une lib obsolète
* Utf8 generator utilise des fonctions dépréciée de ImageMagick
~~~

### 06/10/2026 11:36 — Alan Raynaud

~~~textile
Autre souci : vsnSystem n'est pas compatible C++20.
~~~

### 06/10/2026 11:43 — Alan Raynaud

- Relation ajoutée (liée à) : #9022

### 06/10/2026 11:44 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 60 % → 100 %

~~~textile
Cause :
* UTF8-Generator utilisait une fonction dépréciée de ImageMagick
* vsnSystem, qui utilise UTF8-Generator n'est pas détecté par l'algo de calcul de dépendances
~~~

### 19/10/2026 10:44 — Pascal Vognin

- Pièce jointe ajoutée : clipboard-202610191043-w2au2.png

~~~textile
!clipboard-202610191043-w2au2.png!

Est-ce qu'il manque un fichier à commit?

J'ai eu la même erreur avec SensorRepresentationProcessor
~~~

### 21/10/2026 10:37 — Alan Raynaud

- Statut : Résolu → En cours
- Avancement : 100 % → 90 %

### 21/10/2026 13:39 — Alan Raynaud

~~~textile
CORE_RL_Magick_.lib n'existe plus dans la nouvelle version de ImageMagick. Suite à la migration, certains projets continuait de pointer dessus, et échouent à compiler suite à suppression de cette lib obsolète de CVS.

Impactés :
* SensorRepresentationProcessor -> corrigé par Pascal
* GenericRecorderPlugin -> je m'en charge
~~~

### 21/10/2026 14:57 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %
