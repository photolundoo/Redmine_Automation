# #8971 — Iris/MCP : créer les incident à partir de l'entityid du type d'incident

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Fonctions - Iris |
| Catégorie | com.egidium.iris |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8962 |
| Auteur | Alan Raynaud |
| Assigné à | Mathieu Fournet-Carcopino |
| Avancement | 100 % |
| Créé le | 23/07/2026 15:09 |
| Mis à jour le | 18/09/2026 14:37 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8971 |

## Description

~~~textile
Utilise ajourd'hui le @Code@, qui sert principalement à communiquer avec les systèmes tiers, pour des types convenus à l'avance. Peu de type, en particulier les types manuels, ont donc un @Code@ pré-défini. Cela limite donc la capacité d'Iris à créer des incidents.

L'API va être étendue afin de permettre de créer un incident à partir de l'entityid de l'IncidentType.
~~~

## Relations

- Bloquée par #8970

## Historique

### 23/07/2026 15:09 — Alan Raynaud

- Relation ajoutée (bloquée par) : #8970

### 06/08/2026 16:50 — Mathieu Fournet-Carcopino

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %
- Evolution majeure : (vide) → 0

~~~textile
smartshield-mcp :

Ajout du paramètre alarm_type_eid (entier) dans le schéma du tool — il est désormais transmis tel quel dans le body de la requête POST /api/alarms/alarms
Le champ code reste disponible pour compatibilité ascendante mais n'est plus requis
Une erreur est levée si ni alarm_type_eid ni code ne sont fournis / trouvés

Iris  :
L'agent appelle directement data_list_entities(template="IncidentType", compact=false) pour récupérer tous les types avec leurs attributs
L'identification du type se fait par correspondance sur Name ou DisplayName (et non plus sur le Code)
L'entityId du type sélectionné est passé dans alarm_type_eid — Iris n'utilise plus de code texte ; code reste accepté par le MCP pour la compatibilité avec d'autres clients.
~~~

### 18/09/2026 14:37 — Fernand Alcatrao

- Fonction : ISAP Core - SDK → ISAP Fonctions - Iris
