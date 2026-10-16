# #9026 — [Ansible] Prendre en compte WebAPI/Iris

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - Administration |
| Catégorie | com.egidium.installer |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Mathieu Fournet-Carcopino |
| Avancement | 100 % |
| Créé le | 13/08/2026 16:05 |
| Mis à jour le | 12/10/2026 14:31 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9026 |

## Description

~~~textile
Avec paramètres oui/non et autres paramètres nécessaires comme la clé Mistral ...
Pour WebAPI, voir doc : m:\DEVELOPPEMENTS\Documentation CD\com.egidium.api\private\doc
~~~

## Historique

### 12/10/2026 09:09 — Mathieu Fournet-Carcopino

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
Iris et l'API s'installent lors d'une instalation d'ISAP en version supérieur ou égale à la version 27.1 via Ansible 
~~~

### 12/10/2026 09:22 — Mathieu Fournet-Carcopino

~~~textile
Par conséquent, ajout des variables suivantes dans les inventories : 
mistral_api_key: 
email_agent_user: 
email_agent_password: 
email_imap: 
email_password: 
email_poll_interval: 
email_user: 
~~~

### 12/10/2026 13:12 — Alan Raynaud

- Version cible : Candidate for next major release → ISAP-V27.1

### 12/10/2026 14:10 — Mathieu Fournet-Carcopino

- Ticket parent : (vide) → #9052

### 12/10/2026 14:13 — Mathieu Fournet-Carcopino

- Ticket parent : #9052 → (vide)

### 12/10/2026 14:18 — Mathieu Fournet-Carcopino

~~~textile
De plus, pour la création de l'utilisateur IrisMail (par defaut) pour la gestion des mails en utilisant la WebAPI, j'ai modifié / créer les fichiers suivants :
- "C:\DEV\EGIDIUM\com.egidium.bb.events\public\install\CreateEntities.isap" : Ajout de la création de l'utilisateur
- "C:\DEV\EGIDIUM\com.egidium.bb.events\public\install\LinkEntities.isap" : Ajout de la relation pour l'utilisateur IrisMail vers le dossier parent
- "C:\DEV\EGIDIUM\com.egidium.bb.events\public\install\FingerPrints\27.1.00\Patch-25.1.00-27.1.00.isap" : Ajout de la création de l'utilisateur
- "C:\DEV\EGIDIUM\com.egidium.bb.events\public\install\FingerPrints\27.1.00\Patch-25.1.00-27.1.00-Links.isap" : Ajout de la relation pour l'utilisateur IrisMail vers le dossier parent
~~~

### 12/10/2026 14:23 — Mathieu Fournet-Carcopino

~~~textile
Aussi, ces ajouts m'ont permis de voir qu'il y avait des erreurs dans mon script de mise à jour de la base de données via les FingerPrint : 
- Les Patchs se lançaient plusieurs fois au lieu d'une seule
- Les Patch-*-Links ne se lançaient pas car il y avait des problèmes dans la liste des dossiers.

Par conséquence (pour prendre l'exemple d'Iris) je me retrouvais avec deux utilisateurs IrisMail dont aucun qui n'était reliés au Dossier.

Après modification du script, cela est à présent résolu.
~~~

### 12/10/2026 14:31 — Mathieu Fournet-Carcopino

~~~textile
A noter, le fait d'installer la WebAPI nécessite la création du venv dans "/home/isap/venv/" mais aussi l'installation de smartshieldwebapi prennent un peu plus de temps lors de l'installation.
~~~
