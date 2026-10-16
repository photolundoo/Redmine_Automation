# #9108 — [WebApp][Runsheet] Changement non désiré des temps Durée et Pré-Affichage

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | WebApp - Runsheet |
| Catégorie | com.egidium.isap.reporting |
| Version cible | ISAP-V27.1 |
| Auteur | Rodrigue Favrot |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 09/10/2026 18:17 |
| Mis à jour le | 13/10/2026 12:59 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V25.1 |
| Lien Redmine | https://srvfr-redmine/issues/9108 |

## Description

~~~textile
Dans le module RunSheet, lors de la création d'une Task/Event, les valeurs *_Durée_* et *_Pré-Affichage_* sont modifiées quelques secondes après le changement de valeur par l'opérateur.

Pour reproduire :
# Créer une Task ou Event sans sauvegarder
# Editer ensuite la valeur des champs *_Début_*  , *_Durée_ *  ou *_Pré- affichage_*
# Attendre environ 6s
# *Anomalie* : Constater le changement non désiré des champs *_Durée_*  et/ou *_Pré-affichage_*

+A savoir+  : Lors de l'édition du champ *Début*, plus utilisateur choisit une date éloignée de l'heure courante, plus les valeurs *Durée* et *Pré-Affichage* se retrouvent avec des valeurs importantes.
Exemple avec l'édition de 09/10/2026 à 18/10/2026 :
!clipboard-202610091814-qlgqy.png!
~~~

## Pièces jointes

- [clipboard-202610091814-qlgqy.png](pieces_jointes/clipboard-202610091814-qlgqy.png) — 8 Ko, ajoutée par Rodrigue Favrot le 09/10/2026 18:14

## Historique

### 12/10/2026 14:07 — Alan Raynaud

- Version cible : Candidate for next major release → ISAP-V27.1

### 13/10/2026 12:59 — Vincent Tellier

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
Résolu en 27.1
~~~
