# #8206 — [WebApp][MainCourante] Gestion des incidents sur capteurs

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | WebApp - Main Courante |
| Catégorie | com.egidium.isap.reporting |
| Version cible | ISAP-V27.1 |
| Auteur | Rodrigue Favrot |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 04/12/2024 17:27 |
| Mis à jour le | 17/09/2026 14:25 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V5.6.1 |
| Release notes | Non |
| Lien Redmine | https://srvfr-redmine/issues/8206 |

## Description

~~~textile
Vu au cours d'une présentation, la main courante récupère mal les données pour un incident sur capteur positionné dans une _place_  et un _local_ :

!clipboard-202412041704-ovggy.png!

*1. L'adresse n'est pas indiquée (carré rouge)*

L'incident étant positionné via le capteur, il faut récupérer la position GPS du capteur pour ensuite obtenir l'adresse.
 
*2. Il y a 2 lignes pour le même incident (carré vert)*

Cela est certainement dû au fait que le capteur est à la fois relié à une _place_  et un _local_. (carré bleu)
Le fait d'éditer la description de l'incident 1539 fait disparaitre la 2ième ligne mais provoque l'apparition d'autres incidents en triple.

A savoir: L'incident est bien positionné sur l'app _Situation_
~~~

## Pièces jointes

- [clipboard-202412041704-ovggy.png](pieces_jointes/clipboard-202412041704-ovggy.png) — 45 Ko, ajoutée par Rodrigue Favrot le 04/12/2024 17:04

## Historique

### 08/09/2025 17:03 — Alan Raynaud

- Version cible : Candidate for next major release → ISAP-V27.1

~~~textile
Urgent --> à mettre au moins dans la version suivante.
~~~

### 21/07/2026 13:29 — Fernand Alcatrao

- Début : (vide) → 21/07/2026

### 28/07/2026 13:48 — Fernand Alcatrao

- Statut : Nouveau → En cours
- Avancement : 0 % → 10 %
- Temps estimé : (vide) → 8.0 h

### 05/08/2026 17:46 — Vincent Tellier

- Avancement : 10 % → 90 %

~~~textile
J ai juste exclu de la requete les places provenant des locals. A voir si c est ce qu on veut

-			" 	AND er2.RELATION_TYPE_ID = " << INCIDENT_PLACE_REL_TYPE << " ";
+			" 	AND er2.RELATION_TYPE_ID = " << INCIDENT_PLACE_REL_TYPE << " "
+			" 	AND er2.PAR_ENTITY_ID IN ( "
+			" 		SELECT ENTITY_ID FROM ENTITY" << l_sqlUseTableHist << " "
+			" 		WHERE TEMPL_ENTITY_ID <> " << m_local_TID << " "
+			" 	) ";
~~~

### 17/08/2026 08:58 — Vincent Tellier

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %

### 17/09/2026 14:25 — Guillaume Lemaitre

~~~textile
Avant de finaliser la procédure de test, j'aurais besoin d'une clarification sur deux points liés au correctif décrit dans la note #4 :

L'exclusion des Places dérivées de Locals dans la requête corrige-t-elle uniquement le problème de doublon, ou traite-t-elle également l'absence d'adresse ? Les deux semblent liés mais rien ne l'indique explicitement.
Quel est le comportement attendu pour un capteur relié uniquement à un Local, sans relation directe à une Place ? Avec l'exclusion des relations Local, ce capteur ne remontera plus aucune Place (donc plus d'adresse sur l'incident correspondant). Est-ce le comportement voulu, ou faut-il prévoir un repli sur la Place parente du Local dans ce cas ?
~~~
