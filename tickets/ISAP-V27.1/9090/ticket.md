# #9090 — [WebApp] Vision NOK dans le cas d'incident ayant pour source un capteur relié à une place

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | WebApp - Video |
| Catégorie | com.egidium.isap.reporting |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 29/09/2026 11:49 |
| Mis à jour le | 13/10/2026 16:10 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V25.1 |
| Release notes | Oui |
| Lien Redmine | https://srvfr-redmine/issues/9090 |

## Description

~~~textile
Exemple de scénario :
* Demo ACME
* Utilisation du simulateur SIA pour simuler des alarmes
* Le capteur simulé est positionné dans le champs de vision d'Atlantique, dans les bureaux
* Scénario NOK :
## On relie le capteur à l'étage 1 du bâtiment
## On simule une alarme
## Un incident est créé, ayant pour source le capteur et relié à l'étage
*** Vision OK dans la WinApp
*** Vision NOK dans la WebApp : "pas de caméra", mais les logs CameraProcessor indiquent qu'ils n'y a même pas d'appel
* Scénario OK
## On retire la relation entre le capteur et l'étage (quand on passe au RDC, il continue donc d'être affiché en l'air)
## On simule une alarme
## Un incident est créé, ayant pour source le capteur 
*** Vision OK dans la WinApp
*** Vision OK dans la WebApp
~~~

## Historique

### 09/10/2026 10:15 — Vincent Tellier

- Avancement : 0 % → 90 %

### 13/10/2026 16:10 — Vincent Tellier

- Statut : Nouveau → Résolu
- Avancement : 90 % → 100 %
