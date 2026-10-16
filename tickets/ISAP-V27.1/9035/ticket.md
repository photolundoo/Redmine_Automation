# #9035 — [WebApp/Dashboard] Affichage des capteurs en fonction de leur type et de leur état

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | WebApp - Main Courante |
| Catégorie | com.egidium.isap.reporting |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Lucie Thomas |
| Avancement | 100 % |
| Créé le | 18/08/2026 11:25 |
| Mis à jour le | 30/09/2026 14:32 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9035 |

## Description

~~~textile
Pouvoir créer un dashbord qui liste les capteurs :
* Filtres
** Uniquement les capteurs de types choisis (ex: VERRE, EP et OM)
** Uniquement les capteurs dont les attributs booléens sont dans un état définis (ex: Active=true et Triggered=true)
* Colonnes : permette de choisir quels attributs des capteur afficher (DisplayName, Description, etc.)

Exemple de dashboard :
* PAV pleins (capteurs de type VERRE, EP et OM dont les attributs sont Active=true et Triggered=true)
* Guichets non-armés (capteurs de type ARME dont les attributs sont Active=true et Triggered=false)
* Pannes (capteur de tous types dont les attributs sont Active=true et Failure=true)

Remarque sur les attributs :
* Active : est-ce que le capteur est branché / est-ce qu'on est connecté au système qui gère ce capteur. C'est seulement dans le cas True que l'on a les informations temps réel sur le capteur et donc que les autres attibuts sont pertinents
* Triggered : capteur déclenché. La sémantique dépend du type de capteur.
* Failure : panne du capteur. Un problème interne empêche le capteur de fonctionner correctement, son état n'est donc pas fiable.
* Disrupted : capteur perturbé. Un élément externe empêche le capteur de fonctionner correctement, son état n'est donc pas fiable.
* Inhibited : capteur inhibé. On ne souhaite pas que le capteur déclenche des alarmes.
~~~

## Relations

- Liée à #9093

## Pièces jointes

- [clipboard-202609281524-dzuav.png](pieces_jointes/clipboard-202609281524-dzuav.png) — 14 Ko, ajoutée par Lucie Thomas le 28/09/2026 15:24
- [clipboard-202609301432-kz02i.png](pieces_jointes/clipboard-202609301432-kz02i.png) — 140 Ko, ajoutée par Alan Raynaud le 30/09/2026 14:32

## Historique

### 24/08/2026 09:25 — Lucie Thomas

- Avancement : 0 % → 80 %

### 25/09/2026 15:45 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 28/09/2026 15:23 — Lucie Thomas

- Statut : En cours → Résolu
- Avancement : 80 % → 100 %

~~~textile
Rodrigue doit faire la V2 du case

CF les filtres par attributs :
!clipboard-202609281522-6uwkq.png!
~~~

### 28/09/2026 15:24 — Lucie Thomas

- Pièce jointe ajoutée : clipboard-202609281524-dzuav.png

~~~textile
!clipboard-202609281524-dzuav.png!
~~~

### 30/09/2026 14:20 — Alan Raynaud

- Relation ajoutée (liée à) : #9093

### 30/09/2026 14:32 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202609301432-kz02i.png

~~~textile
Sur vgp-sandbox, test de dashboard pour les PAV :

!clipboard-202609301432-kz02i.png!
~~~
