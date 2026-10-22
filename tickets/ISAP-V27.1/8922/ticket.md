# #8922 — Erreur sur calcul des seuils de comptage - Désynchronisation techevent plugin et countingprocessor

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Plugins - Contrôle d'Accès |
| Catégorie | com.egidium.pr.counting |
| Version cible | ISAP-V27.1 |
| Auteur | Pascal Vognin |
| Assigné à | Pascal Vognin |
| Avancement | 100 % |
| Créé le | 15/06/2026 11:53 |
| Mis à jour le | 19/10/2026 09:21 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | SIAE |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V5.5.1 |
| Lien Redmine | https://srvfr-redmine/issues/8922 |

## Description

~~~textile
Vu sur eurosatory ce weekend.

Le calcul des seuils n'est pas synchronisé avec la mise à zero des comptages par techvent.
Je détaillerai l'analyse qu'on a fait du code et les points à corriger améliorer.

Mais les objectifs de ce case sont déjà ciblés :
* Faire en sorte que le plugin techvent remette à zero ses comptages avant que counting processor mette à zero le seuil actuellement dépassé
** Pour ça on ajoutera une variable dans IsapGrid-Application qui est l'heure du reset des comptages
** Techevent devra utiliser cette heure -15min pour faire son reset des valeurs (ça permet d'être large pour mettre à jour les valeurs en base et qu'elle soit bien traitées si on a un très gros volume de données)
** CountingProcessor devra pouvoir être configuré pour utilise l'heure définie dans la grille pour reset (aujourd'hui ce n'est pas configurable)
~~~

## Historique

### 15/06/2026 11:53 — Pascal Vognin

- Version cible : Candidate for next major release → ISAP-V25.1
- Version source : ISAP-V25.1 → ISAP-V5.5.1

### 15/06/2026 12:08 — Pascal Vognin

~~~textile
Outre les développements et modifications de configuration à faire, on a remarqué un code assez complexe pour définir si on doit ou non appliquer le reset.

Le code date depuis longtemps (Février 2015).

Il est à revoir et corriger car je mélange des choses étranges/incompatibles pour déterminer si on doit reset
* On sauvegarde la date du dernier reset
* On vérifie si le nombre d'heures depuis ce dernier reset est > à l'heure locale au moment de la vérification du reset
** Si oui on fait le reset
** Si non on attend 24h apriori

* La sauvegarde est faite en HK_CURRENT_USER  : il faut aussi changer ça en localmachine car ce sont des procs
~~~

### 22/06/2026 11:11 — Pascal Vognin

~~~textile
Apriori seuls les app elevated via UAC sont capable d'écrire dans HKLM :

learn.microsoft.com/fr-fr/windows/win32/api/winreg/nf-winreg-regcreatekeyexa
stackoverflow.com/questions/3146666/access-to-hklm-registry-branch-on-win-7-from-within-application
~~~

### 22/06/2026 14:49 — Alan Raynaud

- Version cible : ISAP-V25.1 → ISAP-V27.1

### 28/07/2026 13:35 — Fernand Alcatrao

~~~textile
On pourrait aussi utiliser la base ISAP (sans doute plus simple)
~~~

### 28/07/2026 13:35 — Fernand Alcatrao

- Statut : Nouveau → En cours
- Avancement : 0 % → 10 %

### 06/10/2026 16:35 — Fernand Alcatrao

- Projet 1 à livrer : Produit → SIAE

### 07/10/2026 09:49 — Alan Raynaud

- Début : (vide) → 12/10/2026

~~~textile
Pour en parler lundi, surtout que Pascal avait en fait été presque jusqu'au bout.
~~~

### 19/10/2026 09:21 — Pascal Vognin

- Statut : En cours → Résolu
- Avancement : 10 % → 100 %

~~~textile
Ajout d'une configuration dans "C:\DEV\EGIDIUM\com.egidium.pr.counting\public\conf\grid\T-Server-CountingProcessor.xml"

<pre>
<parameter name="counting-reset-hour" default="3" />
</pre>

La configuration est en accord avec TechEventPlugin : 3h du matin par défaut.
TechEventPlugin fait le reset 5min avant l'heure configurée.
~~~
