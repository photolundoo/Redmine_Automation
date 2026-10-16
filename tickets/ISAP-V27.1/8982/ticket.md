# #8982 — [WebApp] Timeout important sur les postes ne disposant pas du plugin vidéo en local

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | WebApp - Accès & Ressources |
| Catégorie | com.egidium.isap.gui.web |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 27/07/2026 11:30 |
| Mis à jour le | 17/08/2026 08:58 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V27.1 |
| Lien Redmine | https://srvfr-redmine/issues/8982 |

## Description

~~~textile
J'ai vu ça sur le serveur VGP, et testé à l'instant sur mon PC :
* Voir config #8941
* Arrêter son plugin video (depuis grid avignon ou en arrêtant le service sur son PC)

Se connecter à la main courante avignon : timeout de 4s :
https://dskfr-avignon.egidium.fr
!clipboard-202607271127-oorca.png!

Du coup j'ai désactivé sur la machine VGP pour ne pas pénaliser tout le monde (pas encore de plugin déployé).

Alan pense qu'il faut tester les proxies dans des threads pour ne pas bloquer le client.
~~~

## Pièces jointes

- [clipboard-202607271127-oorca.png](pieces_jointes/clipboard-202607271127-oorca.png) — 13 Ko, ajoutée par Fernand Alcatrao le 27/07/2026 11:27
- [clipboard-202607281239-5giso.png](pieces_jointes/clipboard-202607281239-5giso.png) — 76 Ko, ajoutée par Fernand Alcatrao le 28/07/2026 12:39

## Historique

### 28/07/2026 12:39 — Fernand Alcatrao

- Pièce jointe ajoutée : clipboard-202607281239-5giso.png

~~~textile
Je viens d'avoir ce problème car mon plugin n'était pas lancé. J'ai pas pensé à ça de suite. J'ai simplement voulu allé voir ici ce qui merdait et le plugin vidéo n'est pas présent avec l'alerte :
!clipboard-202607281239-5giso.png!
~~~

### 31/07/2026 16:27 — Fernand Alcatrao

- Version source : ISAP-V26.1 → ISAP-V27.1

### 05/08/2026 17:51 — Vincent Tellier

- Avancement : 0 % → 90 %

### 14/08/2026 12:55 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 17/08/2026 08:58 — Vincent Tellier

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %
