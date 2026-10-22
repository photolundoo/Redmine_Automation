# #9081 — [WinApp] Créer le MonitoredProcess s'il n'existe pas

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | ISAP Core - Navigation 3D |
| Catégorie | com.egidium.isap.gui |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Pascal Vognin |
| Avancement | 100 % |
| Créé le | 24/09/2026 09:44 |
| Mis à jour le | 19/10/2026 09:16 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9081 |

## Description

~~~textile
Sur satory lors du fillisap les Monitored Process n'ont pas été créés :
!clipboard-202609240941-ywvwa.png!

C'est un problème récurrent quand on ajoute un nouveau poste client sans passer par le configurateur comme en dev chez nous.
Il faudrait que l'iHM le créé s'il n'existe pas et si la configuration est bien "Enabled".

Pour le DisplayName fr/en mettre le nom de la machine.
~~~

## Pièces jointes

- [clipboard-202609240941-ywvwa.png](pieces_jointes/clipboard-202609240941-ywvwa.png) — 17 Ko, ajoutée par Fernand Alcatrao le 24/09/2026 09:41

## Historique

### 12/10/2026 09:24 — Pascal Vognin

- Statut : Nouveau → En cours
- Avancement : 0 % → 80 %

### 12/10/2026 13:14 — Alan Raynaud

- Version cible : Candidate for next major release → ISAP-V27.1

### 19/10/2026 09:16 — Pascal Vognin

- Statut : En cours → Résolu
- Avancement : 80 % → 100 %
