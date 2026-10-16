# #8772 — Outils d'ajout de plugin

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - Administration |
| Catégorie | com.egidium.grid |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 11/02/2026 15:11 |
| Mis à jour le | 02/10/2026 13:59 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Release notes | Oui |
| Description release notes | L'outils PluginWizard (com.egidium.grid\public\tools\PluginWizard) a pour but de faciliter l'ajout de nouveaux plugin dans le système. Il est particulièrement utile dans le cas des systèmes qui requièrent une instance de plugin par équipement (ex: centrales anti-intrusion).    Il gère pour le moment les plugins suivants :  * Vanderbilt SPC  * Honeywell Galaxy |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8772 |

## Description

~~~textile
En croisant Damien à Verdun, j'ai pensé qu'il était assez complexe d'ajouter un plugin, même dans le cas où le métier est déjà prêt.

Cf. par exemple pour Vanderbilt, où on a dû mettre une procédure : https://support.egidium.fr/projects/common/wiki/Vanderbilt_SPC6300#Dupliquer-les-plugins-SPC6300

Il faut effectivement :
* Modifier la grille pour ajouter le plugin ET le processeur
* Créer un fichier .cfg pour les logs
* Créer des choses en base (SubSystemCollection) pour faire le lien entre processor et plugin

Ces étapes pourraient être facilitées par un outils qui permette à un intégrateur de facilement ajouter une nouvelle centrale.
~~~

## Pièces jointes

- [clipboard-202602121717-tofux.png](pieces_jointes/clipboard-202602121717-tofux.png) — 17 Ko, ajoutée par Alan Raynaud le 12/02/2026 17:17
- [clipboard-202602121717-xovgm.png](pieces_jointes/clipboard-202602121717-xovgm.png) — 13 Ko, ajoutée par Alan Raynaud le 12/02/2026 17:17
- [clipboard-202602121717-nvbi3.png](pieces_jointes/clipboard-202602121717-nvbi3.png) — 13 Ko, ajoutée par Alan Raynaud le 12/02/2026 17:17
- [clipboard-202602121717-ggaxi.png](pieces_jointes/clipboard-202602121717-ggaxi.png) — 14 Ko, ajoutée par Alan Raynaud le 12/02/2026 17:17
- [clipboard-202602121718-pgf9y.png](pieces_jointes/clipboard-202602121718-pgf9y.png) — 22 Ko, ajoutée par Alan Raynaud le 12/02/2026 17:18
- [clipboard-202602121718-ybh19.png](pieces_jointes/clipboard-202602121718-ybh19.png) — 35 Ko, ajoutée par Alan Raynaud le 12/02/2026 17:18
- [clipboard-202602121719-nus7n.png](pieces_jointes/clipboard-202602121719-nus7n.png) — 42 Ko, ajoutée par Alan Raynaud le 12/02/2026 17:19
- [clipboard-202602121719-7sjlv.png](pieces_jointes/clipboard-202602121719-7sjlv.png) — 23 Ko, ajoutée par Alan Raynaud le 12/02/2026 17:19
- [clipboard-202602121719-nn30i.png](pieces_jointes/clipboard-202602121719-nn30i.png) — 19 Ko, ajoutée par Alan Raynaud le 12/02/2026 17:19
- [clipboard-202602121719-7e1bb.png](pieces_jointes/clipboard-202602121719-7e1bb.png) — 3 Ko, ajoutée par Alan Raynaud le 12/02/2026 17:19
- [clipboard-202603121416-vr7ef.png](pieces_jointes/clipboard-202603121416-vr7ef.png) — 226 Ko, ajoutée par Guillaume Lemaitre le 12/03/2026 14:16
- [clipboard-202603171348-txnaj.png](pieces_jointes/clipboard-202603171348-txnaj.png) — 6 Ko, ajoutée par Guillaume Lemaitre le 17/03/2026 13:48
- [clipboard-202603171348-blahn.png](pieces_jointes/clipboard-202603171348-blahn.png) — 6 Ko, ajoutée par Guillaume Lemaitre le 17/03/2026 13:48

## Historique

### 11/02/2026 17:22 — Alan Raynaud

- Début : (vide) → 11/02/2026

### 12/02/2026 13:29 — Alan Raynaud

~~~textile
En rédigeant une procédure d'ajout de centrale pour QQVL, je me rends compte que la procédure est en fait beaucoup plus longue et complexe qu'on pourrait le croire.

Ex, le wiki indique :
> Que chaque plugin ait un SubsystemCollection unique, créé en base ISAP.
> (Celui-ci doit lui-même avoir un OperationalState dédié)

Ces deux lignes masquent une grande complexité, au niveau des entités à créer, attributs à remplir et relations à faire.
~~~

### 12/02/2026 14:51 — Alan Raynaud

~~~textile
Reste à faire :
* Mise en base
** SSC (dont lien vers SSC supérieur et icone)
** OpS (dont option lien vers MainHeart)
* IsapTemplate si manquant
* Retour
~~~

### 12/02/2026 17:18 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202602121717-tofux.png
- Pièce jointe ajoutée : clipboard-202602121717-xovgm.png
- Pièce jointe ajoutée : clipboard-202602121717-nvbi3.png
- Pièce jointe ajoutée : clipboard-202602121717-ggaxi.png

~~~textile
!clipboard-202602121717-tofux.png!

!clipboard-202602121717-xovgm.png!

!clipboard-202602121717-nvbi3.png!

!clipboard-202602121717-ggaxi.png!
~~~

### 12/02/2026 17:19 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202602121718-pgf9y.png
- Pièce jointe ajoutée : clipboard-202602121718-ybh19.png
- Pièce jointe ajoutée : clipboard-202602121719-nus7n.png

~~~textile
!clipboard-202602121718-pgf9y.png!

!clipboard-202602121718-ybh19.png!

!clipboard-202602121719-nus7n.png!
~~~

### 12/02/2026 17:20 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202602121719-7sjlv.png
- Pièce jointe ajoutée : clipboard-202602121719-nn30i.png
- Pièce jointe ajoutée : clipboard-202602121719-7e1bb.png

~~~textile
!clipboard-202602121719-7sjlv.png!

!clipboard-202602121719-nn30i.png!

!clipboard-202602121719-7e1bb.png!
~~~

### 12/02/2026 17:25 — Alan Raynaud

- Version cible : ISAP-V27.1 → ISAP-V25.1

~~~textile
Outils indépendant sans interaction avec les autres système et qu'il va être intéressant d'avoir en prod assez vite.
~~~

### 13/02/2026 16:11 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

### 12/03/2026 14:17 — Guillaume Lemaitre

- Pièce jointe ajoutée : clipboard-202603121416-vr7ef.png
- Statut : Résolu → En cours
- Avancement : 100 % → 90 %

~~~textile
Test invalidé  - éléments ajoutés au plan de validation 25.1 Outils Externe


h3. *Erreur constaté sur la configuration de Honeywell Galaxy*

!clipboard-202603121416-vr7ef.png!
~~~

### 16/03/2026 15:09 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %

~~~textile
Cause du problème trouvée + corrigé.

Attention, si le fichier grille a été corrompu par la version précédente de cet outils, il faut le supprimer et le récupérer à nouveau depuis CVS.
~~~

### 16/03/2026 15:13 — Alan Raynaud

- Description release notes : (vide) → L'outils PluginWizard (com.egidium.grid\public\tools\PluginWizard) a pour but de faciliter l'ajout de nouveaux plugin dans le système. Il est particulièrement utile dans le cas des systèmes qui requièrent une instance de plugin par équipement (ex: centrales anti-intrusion).

Il gère pour le moment les plugins suivants :
* Vanderbilt SPC
* Honeywell Galaxy

### 17/03/2026 13:48 — Guillaume Lemaitre

- Pièce jointe ajoutée : clipboard-202603171348-txnaj.png
- Pièce jointe ajoutée : clipboard-202603171348-blahn.png
- Statut : Résolu → Fermé

~~~textile
Test validé - Ajouté et documenté dans le plan de validation *Outils externes 25.1*
!clipboard-202603171348-blahn.png!
~~~

### 16/04/2026 10:42 — Alan Raynaud

- Statut : Fermé → En cours
- Version cible : ISAP-V25.1 → ISAP-V27.1
- Avancement : 100 % → 60 %

~~~textile
Le plan de validation a montré qu'il y a pas mal de souci. En particulier, si la grille met trop de temps à se mettre à jour (ex: IsapReportingServer tarde à s'arrêter), l'opération est interrompue et le relancer va créer des doublons.

De plus, la liste des plugin est encore trop limitée pour être pratique. Autant repousser à la version suivante pour l'améliorer (peut avec d'autres sous-cases, etc.) 
~~~

### 02/10/2026 10:16 — Alan Raynaud

- Evolution majeure : (vide) → 0

~~~textile
Utilisé lors du déploiement Verdun, et a très largement facilité l'ajout de centrales Vanderbilt.

Problèmes constaté :
* Problème dans le nom de l'OpS créé vs attendu (_OpS au lieu de -OpS) --> corrigé à la volée
* Les plugin sont actuellement mis en @manual@ par défaut --> corrigé à la volée
* Si l'application de grille échoue (ex: certains services mettent du temps à s'arrêter), les entités sont toute de même crées, ce qui provoque au final des doublons. Il faudrait appliquer les modifications de grille avant tout changement en base.
* Peu de choix de plugin : sera fait dans un autre case, pas à gérer ici

Par ailleurs, étant donné que cet outils ne sera disponible que sur les nouveaux site, il serait intéressant de faire un peu de reverse engineering sur la procédure complète pour ajouter un nouveau plugin intrusion. En effet, les difficultés rencontrées lors du développement de ce case n'ont pas très bien été documentée (ex: note 2). L'ajout de plugin intrusion est particulièrement notable, car l'ajout d'une nouvelle centrale est une opération courante (contrairement à l'ajout d'un nouveau serveur de contrôle d'accès).
~~~

### 02/10/2026 13:57 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 60 % → 100 %

### 02/10/2026 13:59 — Alan Raynaud

~~~textile
Wiki entièrement revu : https://support.egidium.fr/projects/common/wiki/Vanderbilt_SPC6300#Int%C3%A9gration-dune-nouvelle-centrale-Vanderbilt

On a désormais la procédure complète pour l'ajout d'une nouvelle centrale. Sera en particulier utile à LMV.
~~~
