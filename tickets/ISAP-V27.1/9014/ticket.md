# #9014 — [ActionManager] Erreur de traitement pour les desinhibitions automatiques

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Core - Gestion des capteurs |
| Catégorie | com.egidium.pr.action |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 11/08/2026 15:22 |
| Mis à jour le | 11/08/2026 15:41 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | EIFFAGE ES |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V25.1 |
| Release notes | Oui |
| Lien Redmine | https://srvfr-redmine/issues/9014 |

## Description

~~~textile
Cause par le code suivant :
<pre><code class="cpp">
		if(l_oldAuthor != author)
		{
			if(l_oldAuthor != -1)
			{
				CoreIsap::IsapClient::GetInstance().DeleteRelation(l_iInstance, author, ACTIONINSTANCE_AUTHOR_REL_BASE_TYPE);
			}
			CoreIsap::IsapClient::GetInstance().SendRelation(l_iInstance, author, ACTIONINSTANCE_AUTHOR_REL_BASE_TYPE, ACTIONINSTANCE_AUTHOR_REL_TYPE);
			
		}
</code></pre>

Dans le cas d'une désinhibition automatique, "l'auteur" est un processeur, ce qui provoque une erreur car la relation entre Processor et ActionDelayedInstance n'est pas autorisée.

Conséquences :
* des erreurs dans les logs
* les désinhibitions programmées sont mal effacées de la base
~~~

## Relations

- Liée à #8717

## Historique

### 11/08/2026 15:22 — Alan Raynaud

- Relation ajoutée (liée à) : #8717

### 11/08/2026 15:40 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
A tester dans le cadre du test du #8717 

Une fois les tests terminés, vérifier qu'il ne reste aucun ActionDelayer ou ActionInstance en base.
~~~

### 11/08/2026 15:41 — Alan Raynaud

- Version source : ISAP-V5.6.2 → ISAP-V25.1

~~~textile
Premier cas où le problème pouvait apparaitre : #8450 
~~~
