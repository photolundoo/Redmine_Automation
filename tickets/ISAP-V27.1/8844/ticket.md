# #8844 — Configurer le site ACME avec les caméra Hanwha

| Champ | Valeur |
|---|---|
| Tracker | Configuration |
| Statut | Résolu |
| Priorité | Normal |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8841 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 01/04/2026 10:27 |
| Mis à jour le | 13/10/2026 14:19 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Lien Redmine | https://srvfr-redmine/issues/8844 |

## Description

~~~textile
* Installer et configurer un broker MQTT
* Installer et configurer les caméras (dont algos)
* Intégrer les caméras dans Genetec
* Màj la demo Acme avec ces caméras
~~~

## Pièces jointes

- [clipboard-202604011722-wlvuq.png](pieces_jointes/clipboard-202604011722-wlvuq.png) — 330 Ko, ajoutée par Alan Raynaud le 01/04/2026 17:22
- [clipboard-202604011723-pt6rk.png](pieces_jointes/clipboard-202604011723-pt6rk.png) — 356 Ko, ajoutée par Alan Raynaud le 01/04/2026 17:23
- [clipboard-202604011725-axydd.png](pieces_jointes/clipboard-202604011725-axydd.png) — 387 Ko, ajoutée par Alan Raynaud le 01/04/2026 17:25

## Historique

### 01/04/2026 11:23 — Alan Raynaud

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 01/04/2026 13:30 — Alan Raynaud

- Relation ajoutée (bloquée par) : #8848

### 01/04/2026 17:20 — Alan Raynaud

~~~textile
Broker Mosquitto installé sur srvfr-satory, port 1883

Comptes :
* Pour les caméra : hanwha/hanwha
* Pour le plugin : hanwha_plugin/hanwha_plugin
~~~

### 01/04/2026 17:26 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202604011722-wlvuq.png
- Pièce jointe ajoutée : clipboard-202604011723-pt6rk.png
- Pièce jointe ajoutée : clipboard-202604011725-axydd.png

~~~textile
Algos configurés sur la caméra :

* Comptage de personnes
** Ligne : devant la porte d'entrée (niveau des boites aux lettre)
** Cible : piétons
* Comptage de véhicules
** Ligne : moitié du parking
** Cible : tous vehicule
** *Actuellement désactivé à cause de #8848*
* Détection de présence prolongée
** Zone : devant la porte d'entrée
** Sensibilité : 10s
* Détection de départ/arrivé
** Zone : sur la place de parking handicapé 

Configuration MQTT :
* Vers srvfr-satory
* Prefixe de topic : Hanwha/241


!clipboard-202604011722-wlvuq.png!

!clipboard-202604011723-pt6rk.png!

!clipboard-202604011725-axydd.png!
~~~

### 01/04/2026 17:27 — Alan Raynaud

- Statut : Nouveau → En cours
- Avancement : 0 % → 80 %

~~~textile
Reste à mettre les caméras dans la 3D
~~~

### 02/04/2026 14:04 — Alan Raynaud

- Statut : En cours → Bloqué
- Avancement : 80 % → 90 %

~~~textile
Reste à activer le compteur de vehicule quand #8848 sera résolu
~~~

### 23/04/2026 16:50 — Alan Raynaud

~~~textile
J'ai basculé le broker MQTT vers dskfr-orleans
~~~

### 27/07/2026 14:50 — Alan Raynaud

- Début : 01/04/2026 → (vide)

### 13/10/2026 14:19 — Alan Raynaud

- Relation supprimée (bloquée par) : #8848

### 13/10/2026 14:19 — Alan Raynaud

- Statut : Bloqué → Résolu
- Avancement : 90 % → 100 %
