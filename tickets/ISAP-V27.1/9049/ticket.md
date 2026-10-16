# #9049 — [ServerConfiguration] Lors du remplissage initial de la base, le configurateur cherche des fichiers dans le dossier Fingerprint

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Core - Configuration |
| Catégorie | com.egidium.configuration |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Pascal Vognin |
| Avancement | 100 % |
| Créé le | 07/09/2026 16:40 |
| Mis à jour le | 30/09/2026 11:08 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V5.5.1 |
| Release notes | Non |
| Lien Redmine | https://srvfr-redmine/issues/9049 |

## Description

~~~textile
La dossier fingerprint sert à migrer les bases d'une version à l'autre.

Les fichiers ne ce dossier ne doivent donc pas être utilisés pour le remplissage initial de la base.

Or, si des fichier .priv y sont présents, le configurateur les execute, ce qui provoque des erreurs car les templates se retrouvent alors en doublon.

Le problème existe depuis longtemps mais n'avait jamais été detecté car il n'y a habituellement pas de priv dans de dossier.

*NOTE* : En attendant j'ai renommé le Priv.isap en Priv.cisap pour débloquer la situation. Lors des tests bien vérifier que c'est redevenu un .isap sinon demandé à Fernand de le renommer sur le serveur CVS.
~~~

## Historique

### 07/09/2026 16:40 — Alan Raynaud

- Release notes : (vide) → Non

~~~textile
Le problème n'est rencontré qu'en interne (priv), donc pas RN
~~~

### 09/09/2026 13:47 — Fernand Alcatrao

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)
- Début : (vide) → 07/09/2026

### 30/09/2026 11:08 — Pascal Vognin

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
Corrigé, il n'y a qu'à cet endroit que la regex était permissive.
On skip le dossier si il contient dans son nom FingerPrints
~~~
