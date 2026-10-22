# #9129 — SmartShieldWebAPI : Information sur la licence

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - SDK |
| Catégorie | com.egidium.api |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 21/10/2026 14:02 |
| Mis à jour le | 21/10/2026 15:39 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Release notes | Oui |
| Description release notes | Ajout de l’endpoint  @/api/system/license@ pour consulter la licence du serveur Smartshield. Formats disponibles :  * JSON générique contenant toutes les informations de licence  * JSON interprétable par PRTG (requiert PRTG >= 26.3.122), contenant la durée de validité des licences des postes    Cela permet donc d'automatiser le suivi de l'expiration de la licence Smart Shield. Documentation complète dans SystemAPI.yaml. |
| Evolution majeure | 1 |
| Lien Redmine | https://srvfr-redmine/issues/9129 |

## Description

~~~textile
Ajouter un blueprint @system@ donnant accès à des informations sur le système.

La première route à implémenter est la route @license@ qui donne les informations sur la licence du système. Cette route ne requiert pas d'authentification, puisque si la licence est expirée, le système d'authentification est de toute façon inaccessible.

Le format produit par défaut est json, contenant :
* La liste des postes autorisés, avec les dates de validités
* La liste des modules, avec les dates de validités
* Les limites, avec les dates de validités

Si la requête GET demande une réponse au format "application/PRTG", la réponse est à la place un JSON au format attendu par PRTG, avec 1 canal par poste autorisé (modules et limites ne sont pas remontés) :
* Valeur du canal : durée de validité restante (négatif si validité dépassée)
* Seuils du canal :
** warning : 7 jours
** erreur : 0

Plus d'info sur PRTG :
* https://helpdesk.paessler.com/en/support/solutions/articles/76000063370
* https://www.paessler.com/manuals/prtg/rest_json_data_sensor

Nouveau paramètre : chemin vers le fichier de licence (défaut : @%EGIDIUM_DATA%/licences/IsapLicense.lic@)

Format du fichier de licence décrit dans la page [[LicenseFile]] du wiki du redmine.
~~~

## Pièces jointes

- [clipboard-202610211502-qu4ah.png](pieces_jointes/clipboard-202610211502-qu4ah.png) — 84 Ko, ajoutée par Alan Raynaud le 21/10/2026 15:02

## Historique

### 21/10/2026 14:04 — Alan Raynaud

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 21/10/2026 15:06 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202610211502-qu4ah.png

~~~textile
Déployé en avance de phase sur airbus pour test :
!clipboard-202610211502-qu4ah.png!

Cela requiert une version de PRTG récente.
~~~

### 21/10/2026 15:27 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %
- Description release notes : (vide) → Ajout de l’endpoint public GET /api/system/license pour consulter les postes, modules et limites autorisés, avec leurs dates de validité. Une réponse au format PRTG v3 est également disponible : un canal par poste, exprimé en jours, avec seuils d’avertissement à 7 jours et d’erreur à 0. La validité illimitée est représentée par 9999 jours dans PRTG. Documentation de l’API : public/doc/SystemAPI.yaml.

~~~textile
Implémentation terminée : ajout de l’endpoint public GET /api/system/license, avec réponse JSON détaillée et format PRTG v3 (canaux par poste, validité en jours et seuils d’alerte). Le chemin du fichier de licence est configurable ; les erreurs de lecture ou de format renvoient une erreur serveur. La documentation de l’API a été mise à jour dans public/doc/SystemAPI.yaml. La vérification de signature reste hors périmètre de cette V1.

Mise à jour effectuée par GitHub Copilot.
~~~

### 21/10/2026 15:37 — Alan Raynaud

- Description release notes : Ajout de l’endpoint public GET /api/system/license pour consulter les postes, modules et limites autorisés, avec leurs dates de validité. Une réponse au format PRTG v3 est également disponible : un canal par poste, exprimé en jours, avec seuils d’avertissement à 7 jours et d’erreur à 0. La validité illimitée est représentée par 9999 jours dans PRTG. Documentation de l’API : public/doc/SystemAPI.yaml. → Ajout de l’endpoint  @/api/system/license@ pour consulter la licence du serveur Smartshield. Formats disponibles :
* JSON générique contenant toutes les informations de licence
* JSON interprétable par PRTG (requiert PRTG >= 26.3.122), contenant la durée de validité des licences des postes

Cela permet donc d'automatiser le suivi de l'expiration de la licence Smart Shield. Documentation complète dans SystemAPI.yaml.


- Evolution majeure : 0 → 1

~~~textile
Evolution majeure car l'info sur licence est quelque chose qui nous a souvent été demandé.
~~~

### 21/10/2026 15:39 — Alan Raynaud

~~~textile
Pour tester le mode stantard, aller sur l'API à /api/system/licence pour voir que l'on a bien les informations de licence.

Pour tester le mode PRTG, constater sur le PRTG que les informations de licence du serveur airbus sont bien analysées par PRTG : https://tacticplan1.egidium.fr:444/sensor.htm?id=2884&tabid=1
~~~

### 21/10/2026 15:39 — Alan Raynaud

~~~textile
Doc (yaml + word) mis à jour
~~~
