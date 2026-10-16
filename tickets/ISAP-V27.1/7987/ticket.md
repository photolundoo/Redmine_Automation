# #7987 — [DesktopApp] Lenteur d'affichage des cônes caméras sur ville de Paris

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | ISAP Core - Navigation 3D |
| Catégorie | com.egidium.isap.gui |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Rodrigue Favrot |
| Avancement | 100 % |
| Créé le | 17/06/2024 15:49 |
| Mis à jour le | 25/09/2026 15:47 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Ville de Paris |
| Projet 2 à livrer | Versailles Grand Parc |
| Version source | ISAP-V5.6.1 |
| Release notes | Non |
| Lien Redmine | https://srvfr-redmine/issues/7987 |

## Description

~~~textile
Dans fr.paris/public/install il y a 2 fichiers cisap pour créer des caméras :
* 91_VideoCamera-VDP.cisap (1516 caméras)
* 92_VideoCamera-VDP.cisap (2532 caméras)

J'avais remarqué que le CameraProcesseur calculait relativement vite mais que les cônes mettaient longtemps à s'afficher. Et si on fait plusieurs vision de suite, ça prenait du temps à disparaitre et à réapparaitre avec les nouvelles caméras. Etait-ce juste avec 1516 caméras ou bien avec les 1516+2532 ?

Dans le cadre VGP, essayez déjà avec le fichier avec 1516 caméras. Est-ce OK ?
Confirmer que c'est bien lent avec 2532 caméras supplémentaires et essayer de voir si optimisation rapide mais ne pas y passer trop de temps si OK avec 1516 caméras, car c'est la cible pour VGP.

Manip à faire :
* sqlsfillisap fr.paris
* testisapserver 91_VideoCamera-VDP.cisap 
* sqlsbak (pour pouvoir revenir à 1516 caméras rapidement) + renommer le fichier pour ne pas être écraser avec le prochain sqlsbak.
* testisapserver 92_VideoCamera-VDP.cisap 
* sqlsbak (pour pouvoir revenir à 1516+2532 caméras rapidement) + renommer le fichier.
~~~

## Historique

### 02/09/2024 17:24 — Alan Raynaud

- Début : 17/06/2024 → (vide)

~~~textile
Case hors version pas démarré --> Hors sprint
~~~

### 30/10/2024 15:39 — Alan Raynaud

- Priorité : Urgent → Haut

### 23/09/2026 11:43 — Rodrigue Favrot

- Statut : Nouveau → Résolu
- Version cible : Candidate for next major release → ISAP-V27.1
- Début : (vide) → 22/09/2026
- Avancement : 0 % → 100 %
- Release notes : (vide) → Non

~~~textile
Pendant le POC JOP2024, il avait été constaté l'impossibilité de démarrer l'application WinApp en raison du trop grand nombre d'évènements caméra reçus par IceStorm. Il avait fallu couper les retours des mouvements caméra pour pouvoir démarrer l'application.
Afin d'avoir l'état actuel +pour anticiper le POC de la ville de Meaux+ , j'ai testé avec 4048 caméras et un script de simulation d'event caméra.

Après test, avec une configuration lourde et un nombre important d'évènement envoyés :
* L'application a bien démarré 
* L'affichage des cônes caméra réagissaient rapidement

h4. Test réalisé

sqlsfillisap fr.paris
testisapserver 92_VideoCamera-VDP.cisap
Simulation massive d'appel "eventdirection"

=> Ne reproduisant pas la lenteur d'affichage des cônes, je résous le case.
~~~

### 23/09/2026 13:55 — Fernand Alcatrao

~~~textile
Il n'y avait pas de caméras sur fr.paris.
Le pb était sur VGP avec les caméras non quad qui "simulaient des quads" en bougeant de 90° toutes les 5 secondes environ.
~~~

### 25/09/2026 15:47 — Fernand Alcatrao

~~~textile
Le pb a donc disparu par enchantement. Surement dû à la migration VS 2019/2026 et l'optimisation de la mémoire des fenêtres vidéo ... ?
~~~
