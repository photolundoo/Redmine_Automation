# #8992 — [WebApp] Impossible de se connecter après avoir accepté les CGU

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | WebApp - Accès & Ressources |
| Catégorie | com.egidium.isap.gui.web |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 31/07/2026 14:57 |
| Mis à jour le | 17/08/2026 08:56 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V27.1 |
| Lien Redmine | https://srvfr-redmine/issues/8992 |

## Description

~~~textile
Nouveau compte créé.
On se connecte avec et on accepte les CGU : IsapSystem::ExceptionsManagement::UserDoNotHaveRightsToPerformAction
A vérifier en 25.1 !

Second problème. Si on refait connecté, ça considère qu'on est toujours connecté et popup d'avertissement.

PI, AcceptedCGU ne passe pas à 1 donc on tourne en rond.
~~~

## Historique

### 31/07/2026 15:07 — Fernand Alcatrao

~~~textile
OK en 25.1 ;-)
~~~

### 31/07/2026 15:08 — Fernand Alcatrao

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 31/07/2026 16:25 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V27.1

### 31/07/2026 16:27 — Fernand Alcatrao

- Version source : ISAP-V26.1 → ISAP-V27.1

### 31/07/2026 16:28 — Fernand Alcatrao

- Version cible : ISAP-V27.1 → Candidate for next major release

### 31/07/2026 16:29 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V27.1

### 05/08/2026 17:41 — Vincent Tellier

- Statut : Nouveau → En cours
- Avancement : 0 % → 90 %

### 17/08/2026 08:56 — Vincent Tellier

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %
