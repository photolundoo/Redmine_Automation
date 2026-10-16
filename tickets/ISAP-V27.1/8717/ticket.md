# #8717 — [IntrusionProcessor] Inhibition avec temporisation

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Core - Gestion des capteurs |
| Catégorie | com.egidium.pr.intrusion |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 09/12/2025 16:18 |
| Mis à jour le | 13/08/2026 14:16 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | EIFFAGE ES |
| Projet 2 à livrer | Produit |
| Release notes | Oui |
| Description release notes | L'IntrusionProcessor permet désormais de configurer une inhibition temporisée : après une commande d'inhibition, une commande de desinhibition sera automatiquement envoyée une fois un temps configuré écoulé.    Il est recommandé de configurer les inhibitions temporisées directement sur les équipements souhaités. Mais en cas de besoin, cette nouvelle fonctionnalité permet d'avoir une inhibition temporisée applicable à tous les capteurs.    Nouveau paramètre :  * @inhibition-duration@  ** Durée des inhibitions temporisées  ** Valeur possibles :  *** 0 : les inhibitions ne sont pas temporisées  *** X : la temporisation est de X minutes, ie. une commande de desinhibition sera automatiquement envoyée après X minutes  ** Valeur par défaut : 0 (pas de temporisation) |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8717 |

## Description

~~~textile
Fonction déjà réalisée sur le SensorProcessor pour le 1RCH

Mais si on veut plus tard se connecter à de vraies centrales (ex: Vanderbilt), on ne va plus avoir la fonction.

Cela va vite être nécessaire si jamais on doit étendre le 1RCH + utile pour beaucoup d'autres sites.
~~~

## Relations

- Liée à #8450
- Liée à #9014

## Historique

### 09/12/2025 16:19 — Alan Raynaud

- Relation ajoutée (liée à) : #8450

### 09/12/2025 16:22 — Alan Raynaud

- Priorité : Urgent → Haut

~~~textile
Peut-être pas si urgent, car ces règles pourraient en fait être programmées directement sur les centrales.
~~~

### 28/01/2026 10:31 — Alan Raynaud

- Projet 1 à livrer : Produit → EIFFAGE ES

~~~textile
Va être nécessaire si on étend le système de Verdun à des "vraies" centrales.
~~~

### 10/08/2026 11:41 — Alan Raynaud

- Priorité : Haut → Urgent
- Début : (vide) → 10/08/2026
- Evolution majeure : (vide) → 0

### 11/08/2026 14:03 — Alan Raynaud

~~~textile
Il faudra également préparer une version 5.6.2 (pour Verdun)
~~~

### 11/08/2026 15:22 — Alan Raynaud

- Relation ajoutée (liée à) : #9014

### 11/08/2026 15:49 — Alan Raynaud

- Statut : Nouveau → En cours

### 12/08/2026 13:03 — Alan Raynaud

- Avancement : 0 % → 30 %

### 13/08/2026 14:10 — Alan Raynaud

- Release notes : (vide) → Oui
- Description release notes : (vide) → L'IntrusionProcessor permet désormais de configurer une inhibition temporisée : après une commande d'inhibition, une commande de desinhibition sera automatiquement envoyée une fois un temps configuré écoulé.

Il est recommandé de configurer les inhibitions temporisées directement sur les équipements souhaités. Mais en cas de besoin, cette nouvelle fonctionnalité permet d'avoir une inhibition temporisée applicable à tous les capteurs.

Nouveau paramètre :
* @inhibition-duration@
** Durée des inhibitions temporisées
** Valeur possibles :
*** 0 : les inhibitions ne sont pas temporisées
*** X : la temporisation est de X minutes, ie. une commande de desinhibition sera automatiquement envoyée après X minutes
** Valeur par défaut : 0 (pas de temporisation)

### 13/08/2026 14:14 — Alan Raynaud

~~~textile
Pour tester, dans la demo ACME (en gras la nouvelle fonctionnalité) :
* Mettre une valeur X au paramètre @inhibition-duration@ de l'IntrusionProcessor (ex: 1)
* Utiliser un simulateur d'intrusion (ex: @intrusion_simulator@)
* Inhiber un des capteur simulé : il passe à inhiber dans l'affichage de Smart Shield
* *Attendre X minute, et constater que le capteur de desinhibe automatiquement*
~~~

### 13/08/2026 14:14 — Alan Raynaud

~~~textile
Wiki mis à jour
~~~

### 13/08/2026 14:16 — Alan Raynaud

~~~textile
Compilé et testé en 5.6.2 en prévision de la livraison à Verdun.
~~~

### 13/08/2026 14:16 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 30 % → 100 %
