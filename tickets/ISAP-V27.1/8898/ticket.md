# #8898 — Le script SendMailOnIncident.py n'envoi pas la cartographie dans le mail

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - Main Courante |
| Catégorie | com.egidium.pr.python |
| Version cible | ISAP-V27.1 |
| Auteur | Guillaume Lemaitre |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 22/05/2026 10:11 |
| Mis à jour le | 07/10/2026 10:47 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V25.1 |
| Lien Redmine | https://srvfr-redmine/issues/8898 |

## Description

~~~textile
Procédure de test :

!clipboard-202605221002-bxshv.png!

Constaté dans la fenêtre cygwin du script : 
!clipboard-202605221010-hikzh.png!

Notes : les valeurs sont abberrantes pour les champs, c'est normal c'est du smash clavier
~~~

## Relations

- Liée à #8725

## Pièces jointes

- [clipboard-202605221002-bxshv.png](pieces_jointes/clipboard-202605221002-bxshv.png) — 42 Ko, ajoutée par Guillaume Lemaitre le 22/05/2026 10:02
- [clipboard-202605221010-hikzh.png](pieces_jointes/clipboard-202605221010-hikzh.png) — 51 Ko, ajoutée par Guillaume Lemaitre le 22/05/2026 10:10

## Historique

### 28/05/2026 09:13 — Guillaume Lemaitre

- Catégorie : (vide) → com.egidium.pr.python
- Assigné à : (vide) → Alan Raynaud
- Début : (vide) → 22/05/2026

### 01/06/2026 13:44 — Alan Raynaud

- Relation ajoutée (liée à) : #8725

### 23/06/2026 11:14 — Alan Raynaud

- Sujet : « Script Python n'envoi pas la cartographie dans le mail » → « Le script SendMailOnIncident.py n'envoi pas la cartographie dans le mail »
- Version cible : Candidate for next major release → ISAP-V27.1

### 07/08/2026 16:51 — Alan Raynaud

- Début : 22/05/2026 → (vide)

### 14/08/2026 09:39 — Alan Raynaud

- Temps estimé : (vide) → 2.0 h

### 02/10/2026 14:21 — Alan Raynaud

~~~textile
En profiter pour analyser la ligne louche :

<pre><code class="python">
    type_eid = incident["parents"][6]
</code></pre>
~~~

### 07/10/2026 10:47 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
Résolu : remplacement du service de tuiles igngp.geoapi.fr, qui n'était plus disponible, par OpenStreetMap comme pour le ticket #8725. Ajout de l'attribution OpenStreetMap dans la carte jointe et remplacement du chargement spécifique de arial.ttf par la police par défaut de Pillow. Testé : l'envoi du mail avec la carte en pièce jointe fonctionne.
~~~
