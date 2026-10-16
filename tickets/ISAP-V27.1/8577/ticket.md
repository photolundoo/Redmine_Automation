# #8577 — Le paramètre propagateRejectedActions n'est pas correctement pris en compte

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | WebApp - Runsheet |
| Catégorie | com.egidium.isap.reporting |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 02/09/2025 14:01 |
| Mis à jour le | 05/08/2026 17:52 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V25.1 |
| Release notes | Oui |
| Lien Redmine | https://srvfr-redmine/issues/8577 |

## Description

~~~textile
Sur https://demo-smartshield-erp.egidium.fr/, le paramètre est configuré de la manière suivante :

<pre><code class="javascript">
this.localStorage.iceMap_propagateRejectedActions = false // Supprime visuellement la tache sur un rejet pour tout le monde
</code></pre>


Or, dès qu'un utilisateur rejette une tâche, celle-ci n'apparait plus pour les autres utilisateurs.

Le paramètre @iceMap_propagateValidatedActions@ fonctionne correctement.
~~~

## Historique

### 30/09/2025 16:23 — Alan Raynaud

- Release notes : (vide) → Oui

### 21/07/2026 14:05 — Fernand Alcatrao

- Début : (vide) → 21/07/2026
- Temps estimé : (vide) → 2.0 h

### 27/07/2026 09:24 — Vincent Tellier

- Avancement : 0 % → 90 %

### 27/07/2026 18:28 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 05/08/2026 17:52 — Vincent Tellier

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %
