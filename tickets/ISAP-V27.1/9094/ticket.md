# #9094 — [PAVPlugin] PAV en doublons

| Champ | Valeur |
|---|---|
| Tracker | Configuration |
| Statut | Résolu |
| Priorité | Urgent |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 01/10/2026 10:12 |
| Mis à jour le | 01/10/2026 11:27 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Versailles Grand Parc |
| Projet 2 à livrer | Produit |
| Lien Redmine | https://srvfr-redmine/issues/9094 |

## Description

~~~textile
Constaté sur vgp mais pas vgp-sandbox. La différence entre les deux est la configuration du dossier de travail du plugin.

A faire :
* Vérifier la config
* Trouver d'où vient le bug
* Nettoyer les doublons sur VGP
~~~

## Historique

### 01/10/2026 10:51 — Alan Raynaud

~~~textile
C'est en fait la configuration du plugin sur vgp qui est complètement bizarre. Peut-être une tentative de faire une config spécial Buc ? Mais le mélange entre PAV pre-changement et PAV-post changement embrouille le plugin : il ne trouve que le PAV de BUC, mais le SIG lui renvoie tous les PAV existant, et donc créé ceux manquants.
~~~

### 01/10/2026 10:53 — Alan Raynaud

- Tracker : Anomalie → Configuration
- Champ personnalisé 6 : ISAP-V25.1 → (vide)
- Champ personnalisé 7 : ISAP Plugins - Capteurs experts → (vide)
- Champ personnalisé 8 : Non → (vide)

### 01/10/2026 10:53 — Alan Raynaud

- Projet 1 à livrer : Produit → Versailles Grand Parc

### 01/10/2026 11:27 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
Config VGP corrigée + doublons nettoyés.
~~~
