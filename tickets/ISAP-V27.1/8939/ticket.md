# #8939 — Tomcat ne fonctionne plus en mode non https

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - SDK |
| Catégorie | com.egidium.tools.java |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Fernand Alcatrao |
| Avancement | 100 % |
| Créé le | 29/06/2026 14:53 |
| Mis à jour le | 16/10/2026 13:35 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V25.1 |
| Lien Redmine | https://srvfr-redmine/issues/8939 |

## Description

~~~textile
Le fichier de configuration fourni est KO.
Vu sur VGP.
L'utilisation de l'ancien fichier de 2024 a permis de contourner.

En même temps c'est pas très conseillé d'utiliser http ...
~~~

## Historique

### 21/07/2026 11:12 — Alan Raynaud

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 06/10/2026 16:34 — Fernand Alcatrao

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 16/10/2026 13:35 — Fernand Alcatrao

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %

~~~textile
C'était à cause de ça :
<pre><code class="diff">
<       <transport-guarantee>CONFIDENTIAL</transport-guarantee>
---
>       <transport-guarantee>NONE</transport-guarantee>
4794c4774
<   <!-- Enable HSTS -->
---
>   <!-- HTTP header security -->
4801c4781
<     <param-value>true</param-value>
---
>     <param-value>false</param-value>
</code></pre>
~~~
