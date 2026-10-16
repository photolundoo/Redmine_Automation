# #9084 — [MobileApp] Score DEX inférieur au score minimum Playstore

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | WebApp - Mobile |
| Catégorie | com.egidium.isap.reporting |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8754 |
| Auteur | Lucie Thomas |
| Assigné à | Lucie Thomas |
| Avancement | 100 % |
| Créé le | 25/09/2026 13:43 |
| Mis à jour le | 14/10/2026 15:18 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V27.1 |
| Release notes | Non |
| Lien Redmine | https://srvfr-redmine/issues/9084 |

## Description

~~~textile
Nous avons un indice DEX très faible sur un point. Il nous est demandé par le playstore de le corriger d'ici février 2027.

!clipboard-202609251335-9xyya.png!


https://developer.android.com/topic/performance/issues/code-optimization?hl=fr
~~~

## Relations

- Bloque #6474

## Pièces jointes

- [clipboard-202609251335-9xyya.png](pieces_jointes/clipboard-202609251335-9xyya.png) — 13 Ko, ajoutée par Lucie Thomas le 25/09/2026 13:35

## Historique

### 25/09/2026 13:44 — Lucie Thomas

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 25/09/2026 14:14 — Fernand Alcatrao

- Priorité : Haut → Urgent
- Début : (vide) → 28/09/2026

~~~textile
J'ajoute dans le sprint du coup
~~~

### 25/09/2026 15:39 — Fernand Alcatrao

- Ticket parent : #6474 → #8754

### 28/09/2026 13:38 — Alan Raynaud

- Relation ajoutée (bloque) : #6474

### 01/10/2026 11:32 — Lucie Thomas

~~~textile
J'ai mis en place des règles de minimisation et d'obfuscation, on a réduit la taille de l'apk de manière assez conséquente et réduit le nombre de classes exposées.

L'application est en plein test par guillaume et moi même afin de vérifier que ces règles n'ont pas rendu inutilisable certains aspects de l'application.
~~~

### 02/10/2026 17:06 — Alan Raynaud

- Version cible : Candidate for next major release → ISAP-V27.1

### 05/10/2026 17:41 — Alan Raynaud

- Sujet : « [MobileApp] optimisation du code DEX » → « [MobileApp] Score DEX inférieur au score minimum Playstore »
- Statut : Nouveau → En cours
- Release notes : (vide) → Non

~~~textile
Anomalie : le titre indique le problème
Case interne à la version : pas en release note
~~~

### 12/10/2026 09:52 — Lucie Thomas

- Avancement : 0 % → 90 %

~~~textile
obfuscation et minification faites, sans pertes.

Il ne reste plus qu'à publier sur le playstore et vérifier que c'est bon.
~~~

### 14/10/2026 15:18 — Lucie Thomas

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %

~~~textile
application publiée sur le playstore, aucun message d'erreur
~~~
