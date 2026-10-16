# #9091 — Migration Ice 3.7.11 - Javascript

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | WebApp - Main Courante |
| Catégorie | com.egidium.isap.reporting |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8842 |
| Auteur | Alan Raynaud |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 29/09/2026 17:17 |
| Mis à jour le | 13/10/2026 16:10 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9091 |

## Description

~~~textile
Utilisé jusque présent 3.7.0

La version 3.7.11 génère des .js un peu différents, qui provoquent des erreurs de génération dans la configuration actuelle de l'environnement.

Pour l'instant, on peut contourner en :
* Installant Ice 3.7.0 : S:\ZeroC-ICE\Ice-3.7.0
* Mettre Ice dans le PATH (option dans l'installeur)
* Commenter dans le .profile la ligne qui fait pointer vers le slice2js de 3.7.11 (chercher 3.7.11)
~~~

## Historique

### 05/10/2026 09:32 — Vincent Tellier

- Avancement : 0 % → 90 %

~~~textile
La generation des fichiers a ete modifiee et le js est ok maintenant.
~~~

### 13/10/2026 16:10 — Vincent Tellier

- Statut : Nouveau → Résolu
- Avancement : 90 % → 100 %
