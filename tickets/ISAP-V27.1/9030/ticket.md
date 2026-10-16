# #9030 — WebApp : Paramètre permettant de masquer les labels de certaines caméras

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | ISAP Core - Navigation 3D |
| Catégorie | com.egidium.isap.gui.web |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 14/08/2026 11:38 |
| Mis à jour le | 13/10/2026 16:10 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Versailles Grand Parc |
| Projet 2 à livrer | Produit |
| Release notes | Non |
| Numéro de Patch | 00 |
| Evolution majeure | 1 |
| Lien Redmine | https://srvfr-redmine/issues/9030 |

## Description

~~~textile
QuickWin pour mieux gérer les caméras Quad : ajouter un attribut displayLabel aux caméras.
Si = false, la 3D n'affiche pas le label pour ne pas qu'ils soient superposés.
On pourra ainsi mettre les 5 caméras au même endroit.

On en aura besoin pour VGP. 25.1 ?
~~~

## Relations

- Copiée depuis #8775

## Pièces jointes

- [clipboard-202609091512-uyglq.png](pieces_jointes/clipboard-202609091512-uyglq.png) — 5 Ko, ajoutée par Alan Raynaud le 09/09/2026 15:12
- [clipboard-202609091512-pozid.png](pieces_jointes/clipboard-202609091512-pozid.png) — 2 Ko, ajoutée par Alan Raynaud le 09/09/2026 15:12

## Historique

### 14/08/2026 11:38 — Fernand Alcatrao

- Relation ajoutée (copiée depuis) : #8775

### 14/08/2026 11:44 — Fernand Alcatrao

- Avancement : 100 % → 0 %

### 24/08/2026 09:20 — Vincent Tellier

- Avancement : 0 % → 90 %

~~~textile
Le titre est trompeur du coup : ce sont les labels que nous masquons, pas les cameras
~~~

### 01/09/2026 17:56 — Fernand Alcatrao

- Sujet : « WebApp : Paramètre permettant de masquer certaines caméras » → « WebApp : Paramètre permettant de masquer les labels de certaines caméras »

### 01/09/2026 17:58 — Fernand Alcatrao

- Release notes : Oui → Non
- Description release notes : Un nouvel attribut a été ajouté au template Camera pour permettre de masquer leur label dans la WebApp : @DisplayLabel@

Par défaut les labels sont affichés, si cette valeur booléen est mise à faux, le label camera sera masqué.

Suggestion d'usage : caméras "double" ou "quad" qui sont représentées par X caméras fictives dans la VMS (ex: Genetec). Ce paramètre permet de ne garder qu'un seul label dans la WinApp.

Suite du case #8775 concernant la WinApp → (vide)

~~~textile
#8775 déjà dans release notes. Pas la peine d'y mettre un case pour la WinApp et un autre pour la WebApp.
~~~

### 02/09/2026 15:03 — Vincent Tellier

- Statut : Nouveau → Résolu
- Avancement : 90 % → 100 %

### 09/09/2026 15:12 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202609091512-uyglq.png
- Pièce jointe ajoutée : clipboard-202609091512-pozid.png
- Statut : Résolu → En cours
- Avancement : 100 % → 80 %

~~~textile
Testé NOK sur vgp-sandbox

!clipboard-202609091512-uyglq.png!

!clipboard-202609091512-pozid.png!
~~~

### 29/09/2026 12:01 — Vincent Tellier

~~~textile
Ca ne fonctionne effectivement pas dans la situation 2d. Cela n'a été implementé que dans la situation 3d. Je le rajoute du coup
~~~

### 29/09/2026 12:26 — Fernand Alcatrao

~~~textile
C'est à cause du :
> Copié depuis Evolution #8775: Paramètre permettant de masquer les labels de certaines caméras ajouté

Je n'avais pas changé la description du case WinApp.
~~~

### 09/10/2026 10:19 — Vincent Tellier

- Avancement : 80 % → 90 %

### 13/10/2026 16:10 — Vincent Tellier

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %
