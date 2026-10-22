# #8653 — [WebApp] Nombreuses déconnexions lors de la présentation NaTran

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | WebApp - Main Courante |
| Catégorie | com.egidium.isap.gui.web |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 30/10/2025 09:17 |
| Mis à jour le | 20/10/2026 10:59 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V25.1 |
| Lien Redmine | https://srvfr-redmine/issues/8653 |

## Description

~~~textile
D'après Mickaël il ne l'a constaté que depuis un partage de connexion en 4G (il était à l’hôtel le matin).
Depuis chez lui en Wifi, il n'avait pas eu ces soucis.
Chez NaTran on a pu avoir un accès Wifi mais il ne permettait pas d'utiliser un VPN (déjà vu à VGP mairie de Buc). La démo préparée/utilisée est ici :
https://vmsfr-demo01.egidium.fr/maincourante/#/

J'avais tout remis sur le PC de Mickaël pour faire la démonstration en local sur son PC, mais il me semble qu'il avait rencontré un autre soucis ?

Heureusement ça ne s'est pas trop vu ...

Mickaël essaye de reproduire en affichant la console et appelle Vincent pour lui montrer les erreurs.
Après coup, peut-être que le paramètre iceMap_accountUseMultipleTimeTimeout=0 permet de contourner ? On pourra essayer une fois qu'on aura reproduit.

Pas mal de bugs aussi concernant la vidéo avec le bouton vision qui n'affichait/rafraichissait pas dans la fenêtre vidéo, ... Mickaël a souvent fermer les onglets vidéo, puis les a remis et mis les caméras en manuel.
~~~

## Pièces jointes

- [clipboard-202608101815-fbkxi.png](pieces_jointes/clipboard-202608101815-fbkxi.png) — 37 Ko, ajoutée par Fernand Alcatrao le 10/08/2026 18:15
- [Logs.zip](pieces_jointes/Logs.zip) — 70 Ko, ajoutée par Fernand Alcatrao le 04/09/2026 10:35

## Historique

### 30/10/2025 09:18 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V25.1

### 07/11/2025 17:09 — Fernand Alcatrao

- Priorité : Urgent → Haut

~~~textile
D'après Mickael on perdait aussi le RDP donc pertes réseaux liées au partage réseau 5G sur téléphone.
Ca reconnexion devrait quand même se faire.

Pour reproduire, utilisé un partage de connexion 4G/5G
~~~

### 11/02/2026 17:09 — Lucie Thomas

- Avancement : 0 % → 40 %

~~~textile
J'ai push sur la branche #8653-connectionLost_intempestif un correctif.

Ce correctif passe un paramètre à connectionManager si c'est une nouvelle connexion qui permet de ne pas utiliser l'ancien uuid et en générer un nouveau. Je ferme les proxycon après la reconnexion pour qu'ils soient régénérés de manière clean.

ça résout par ailleurs des problèmes sur le mobile quand on "quitte" l'application (veille ou background task)
~~~

### 13/02/2026 09:19 — Lucie Thomas

- Assigné à : Vincent Tellier → Lucie Thomas

### 24/02/2026 10:11 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 28/07/2026 13:20 — Fernand Alcatrao

- Version cible : ISAP-V25.1 → ISAP-V27.1

### 10/08/2026 18:14 — Fernand Alcatrao

- Pièce jointe ajoutée : clipboard-202608101814-q1rvj.png

~~~textile
J'ai mis à jour la machine demo. Avant je me suis déconnecté de l'application mobile.
Puis j'ai arrêté les services ISAP pour pouvoir appliqué les MàJ des binaires.
L'application mobile qui affichait la page de connexion a détecté cette perte de connexion et affiché :
~~~

### 10/08/2026 18:15 — Fernand Alcatrao

- Pièce jointe supprimée : clipboard-202608101814-q1rvj.png

### 10/08/2026 18:15 — Fernand Alcatrao

- Pièce jointe ajoutée : clipboard-202608101815-fbkxi.png

~~~textile
!clipboard-202608101815-fbkxi.png!
~~~

### 04/09/2026 10:35 — Fernand Alcatrao

- Pièce jointe ajoutée : Logs.zip

~~~textile
Sur mobile, ça continue de se déconnecter. Vu hier soir en arrivant à la maison.
Mais c'est beaucoup mieux qu'au début.
~~~

### 28/09/2026 14:34 — Alan Raynaud

- Assigné à : Lucie Thomas → Vincent Tellier

### 20/10/2026 10:59 — Vincent Tellier

- Statut : En cours → Résolu
- Avancement : 40 % → 100 %
