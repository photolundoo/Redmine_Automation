# #8830 — [WinApp] Permettre de configuré la barre d'état au dessus de tout ou pas

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | ISAP Core - Navigation 3D |
| Catégorie | com.egidium.isap.gui |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Pascal Vognin |
| Avancement | 100 % |
| Créé le | 24/03/2026 11:43 |
| Mis à jour le | 19/10/2026 09:34 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Description release notes | Ajout d'un attribut sur la balise menubar  <pre>  <!-- opsbarAlwaysOnTop : if set to true, opsbar will be always on top of operating system - default value = true -->  <menuBar opsbarAlwaysOnTop="true">  ...  </menuBar>  </pre> |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8830 |

## Description

~~~textile
La barre d'état doit être au dessus de tout dans la WinApp, mais pas forcément au dessus de toutes les fenêtres Windows ...
Mettre un paramètre pour permettre de changer ce comportement.
~~~

## Historique

### 24/03/2026 11:43 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V27.1

### 05/10/2026 11:56 — Pascal Vognin

- Statut : Nouveau → En cours
- Avancement : 0 % → 90 %
- Evolution majeure : (vide) → 0

### 19/10/2026 09:34 — Pascal Vognin

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %
- Description release notes : (vide) → Ajout d'un attribut sur la balise menubar
<pre>
<!-- opsbarAlwaysOnTop : if set to true, opsbar will be always on top of operating system - default value = true -->
<menuBar opsbarAlwaysOnTop="true">
...
</menuBar>
</pre>

~~~textile
Ajout d'un attribut sur la balise menuBar
<pre>
<!-- opsbarAlwaysOnTop : if set to true, opsbar will be always on top of operating system - default value = true -->
<menuBar opsbarAlwaysOnTop="true">
...
</menuBar>
</pre>

Si la valeur est vraie, on garde le comportement actuelle : bar de synthèse au dessus de tout
Si la valeur n'est pas vraie, la barre sera au dessus des fenêtre de l'application Isap3DGui uniquement.
~~~
