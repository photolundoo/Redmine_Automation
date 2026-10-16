# #9093 — [PAVPlugin] Pouvoir désactiver la création d'alarme indépendamment du seuil

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Plugins - Capteurs experts |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 30/09/2026 14:15 |
| Mis à jour le | 30/09/2026 14:48 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Versailles Grand Parc |
| Projet 2 à livrer | Produit |
| Release notes | Non |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9093 |

## Description

~~~textile
Les alarmes (création d'incident) n'étaient pas souhaitée en prod.

Nous avons provisoirement baissé le seuil à -1% pour désactiver la création d'incident. Mais en conséquence, l'état @Triggered@ des capteurs n'est plus modifié, et il est donc impossible de filtrer pour trouver les PAV pleins.

Evolution : ajouter un flag (ex: @--create-incidents@), désactivé par défaut, indiquant que l'on souhaite créer des incidents
* Flag actif : sur franchissement de seuil, on change l'état du Sensor et on créé un incident
* Flag inactif : sur franchissement de seuil, on change uniquement l'état du Sensor
~~~

## Relations

- Liée à #9035

## Historique

### 30/09/2026 14:20 — Alan Raynaud

- Relation ajoutée (liée à) : #9035

### 30/09/2026 14:48 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
Déployé sur VGP et VGP-Sandbox :
* Seuil remis à 20%
* Incidents désactivés
~~~
