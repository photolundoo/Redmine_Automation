# #9087 — AffectationTool v2

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - Administration |
| Catégorie | com.egidium.pr.python |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 25/09/2026 17:28 |
| Mis à jour le | 30/09/2026 14:53 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Release notes | Non |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9087 |

## Description

~~~textile
Suite au succès de l'utilisation de l'outils sur site, évolutions intéressante à prendre en compte :
* Affectation à un dossier (afficher la colonne + filtrer + permettre l'affectation des entités à un Dossier) (note: le template s'appelle bien Dossier et non pas Folder)
* Template Caméra (CameraType, Place, Dossier) en plus de Sensor et StandardAccess déjà existant
* Option pour le support des certificat wildcard
** Option de connexion au routeur (case à cocher décochée par défaut) + champs CN (défaut : "*.egidium.fr)
** Si coché, passer un dict au paramètre @params@ du routeur, avec les options
*** "IceSSL.CheckCertName" : "0"
*** "IceSSL.TrustOnly" : valeur du champs CN 


Code à éditer dans @com.egidium.pr.python\public\scripts\Samples\AffectationTool@
~~~

## Historique

### 25/09/2026 17:28 — Alan Raynaud

- Version cible : Candidate for next major release → ISAP-V27.1

### 25/09/2026 17:30 — Alan Raynaud

- Temps estimé : (vide) → 8.0 h

~~~textile
Temps estimé un peu large, car c'est l'occasion d'essayer de tester un processus où le case sert d'instruction.
~~~

### 30/09/2026 14:51 — Alan Raynaud

- Temps estimé : 8.0 h → 2.0 h

~~~textile
Tests MCP déplacés dans le case dédié : #9092 
~~~

### 30/09/2026 14:53 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %
- Release notes : (vide) → Non
