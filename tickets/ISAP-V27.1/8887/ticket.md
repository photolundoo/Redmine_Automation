# #8887 — WebApp : Permettre une utilisation de la vidéo sans Joystick

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | WebApp - Video |
| Catégorie | com.egidium.isap.gui.web |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8843 |
| Auteur | Fernand Alcatrao |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 05/05/2026 18:00 |
| Mis à jour le | 13/10/2026 16:10 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8887 |

## Description

~~~textile
On ne peut pas bouger les caméras sans le joystick. Du coup faire :
- A la souris style genetec avec molette et @-/+@ pour zoom/dezoom
- Au clavier avec les flèches et @-/+@ pour zoom/dezoom
- Permettre de taper le physical ID de la camera + return pour changer de camera
- Delete/Suppr pour la supprimer
- PX pour aller au preset X

Vincent a aussi mis la dichotomie mais avec dates parfois dans le futur donc sans images. Je vais demander à Pascal d'indiquer les règles dans la WinApp.
~~~

## Pièces jointes

- [clipboard-202607271754-vwrvy.png](pieces_jointes/clipboard-202607271754-vwrvy.png) — 2 Ko, ajoutée par Fernand Alcatrao le 27/07/2026 17:54

## Historique

### 03/06/2026 11:23 — Fernand Alcatrao

- Tracker : Configuration → Evolution
- Sujet : « Configurer et tester la vidéo dans la WebApp (dont le joystick) » → « WebApp : Permettre une utilisation de la vidéo sans Joystick »
- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)
- Catégorie : (vide) → com.egidium.isap.gui.web
- Version cible : ISAP-V25.1 → ISAP-V27.1
- Début : (vide) → 27/05/2026
- Temps estimé : 2.0 h → 60.0 h
- Fonction : (vide) → WebApp - Video

### 03/06/2026 11:26 — Fernand Alcatrao

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 03/06/2026 11:44 — Pascal Vognin

~~~textile
Pour l'investigation dans la winApp voici les règles :
* Lorqu'on investigue un objet on configure l'UI, pour utiliser l'intervalle suivant (date de départ - 1800sec) et (date de départ).
** Dans le cas d'un clique dans la 3D : date de départ = time of click
** Dans le cas d'un incident : date de départ = incident.creationtime
** Dans le case d'un securityevent : date de départ = securityevent.creationtime
** Dans le case d'une operation : date de départ = first-securityevent.creationtime

Les 1800 secendes étaient prévues comme configurables, mais on a jamais fini le code qui configure ce temps, car personne n'a demandé à ce que ce soit différent
~~~

### 03/06/2026 12:51 — Fernand Alcatrao

~~~textile
Vincent, il faut aussi un bouton pour pouvoir dézoomer dans la dichotomie.
~~~

### 03/06/2026 13:17 — Pascal Vognin

~~~textile
Pour le dézoom, on garde l'idée que l'opérateur cherche toujours dans le passé, donc on conserve le temps à droite (pour avoir la même image)
Et on agrandis la taille entre la première et la denière

currentTimestep = le temps entre deux images (car on en affiche 3).
<pre>
		auto l_tbegin = m_currentBegin - (m_currentTimestep * 2);
		auto l_tend = m_currentEnd;
</pre>
~~~

### 27/07/2026 17:55 — Fernand Alcatrao

- Pièce jointe ajoutée : clipboard-202607271754-vwrvy.png
- Statut : Nouveau → En cours
- Avancement : 0 % → 80 %

~~~textile
Le joystick et l'utilisation à la souris et clavier sont fonctionnelles.

J'ai constaté ce soucis :
* Afficher une caméra live.
* Passer en rejeu.
* Revenir au live. Il se souvient de la caméra mais n'arrive pas à l'afficher :
!clipboard-202607271754-vwrvy.png!

Pour la dichotomie, c'est fonctionnel à part les temps parfois affichés dans le futur et donc sans imagettes, notamment au démarrage car il centre sur le l'heure courante.
~~~

### 27/07/2026 17:56 — Fernand Alcatrao

- Assigné à : Fernand Alcatrao → Vincent Tellier

### 05/08/2026 17:54 — Vincent Tellier

- Statut : En cours → Résolu
- Avancement : 80 % → 100 %
- Evolution majeure : (vide) → 0

### 15/09/2026 16:37 — Guillaume Lemaitre

- Statut : Résolu → En cours
- Avancement : 100 % → 90 %

~~~textile
Test non validé - La fonction Suppr (Delete) ne fonctionne pas
Ajouté au plan de validation 01 V26.1 - WEBAPP
~~~

### 13/10/2026 16:10 — Vincent Tellier

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %
