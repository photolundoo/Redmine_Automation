# #8465 — [WebApp/Administration] Bugs constatés dans la configuration d'un compte

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | WebApp - Administration |
| Catégorie | com.egidium.isap.gui.web |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 15/06/2025 17:02 |
| Mis à jour le | 05/08/2026 17:53 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V5.6.2 |
| Lien Redmine | https://srvfr-redmine/issues/8465 |

## Description

~~~textile
J'ai voulu enlever Wilfrid du groupe Mercure Salle C3, mais ça ne disparait pas :
!clipboard-202506151701-mrbhk.png!

Mais en fait si :
!clipboard-202506151701-sneux.png!

Et si je me reconnecte pour vérifier c'est bon :
!clipboard-202506151701-sjmq4.png!

Autre mais qui lui ne marche pas du tout :
Si je veux me passer (ou qq'un d'autre) à aucun sur Main Courante pour arriver directement à la connexion sur Situation ça ne sauvegarde pas :
!clipboard-202506151700-yqogs.png!
~~~

## Pièces jointes

- [clipboard-202506151700-yqogs.png](pieces_jointes/clipboard-202506151700-yqogs.png) — 98 Ko, ajoutée par Fernand Alcatrao le 15/06/2025 17:00
- [clipboard-202506151701-sjmq4.png](pieces_jointes/clipboard-202506151701-sjmq4.png) — 10 Ko, ajoutée par Fernand Alcatrao le 15/06/2025 17:01
- [clipboard-202506151701-sneux.png](pieces_jointes/clipboard-202506151701-sneux.png) — 26 Ko, ajoutée par Fernand Alcatrao le 15/06/2025 17:01
- [clipboard-202506151701-mrbhk.png](pieces_jointes/clipboard-202506151701-mrbhk.png) — 10 Ko, ajoutée par Fernand Alcatrao le 15/06/2025 17:01

## Historique

### 21/07/2026 14:11 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V27.1
- Début : (vide) → 21/07/2026

### 27/07/2026 08:58 — Vincent Tellier

- Avancement : 0 % → 50 %

### 27/07/2026 18:28 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 29/07/2026 11:52 — Vincent Tellier

~~~textile
Actuellement, il y a un garde fou qui empêche de retirer ses propres droits sur les droits: Maincourante, Consigne, Partage de situation, Iris, Statistiques, Planification
~~~

### 05/08/2026 17:53 — Vincent Tellier

- Statut : En cours → Résolu
- Avancement : 50 % → 100 %
