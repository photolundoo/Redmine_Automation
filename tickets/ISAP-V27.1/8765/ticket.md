# #8765 — [MobileApp] Éxécution de tâche en arrière plan

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | ISAP Fonctions mobiles - Gestion mobile d'incidents |
| Catégorie | com.egidium.isap.mobile |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8754 |
| Auteur | Lucie Thomas |
| Assigné à | Lucie Thomas |
| Avancement | 100 % |
| Créé le | 05/02/2026 16:51 |
| Mis à jour le | 14/10/2026 15:21 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8765 |

## Description

~~~textile
L'application doit pouvoir rester connecter et/ou être notifié des incidents même lorsque l'application est en arrière plan.

Librairie en cours d’investigation :
https://capacitorjs.com/docs/apis/background-runner#examples
~~~

## Pièces jointes

- [clipboard-202602171630-usaaz.png](pieces_jointes/clipboard-202602171630-usaaz.png) — 703 Ko, ajoutée par Lucie Thomas le 17/02/2026 16:30

## Historique

### 17/02/2026 17:07 — Lucie Thomas

- Pièce jointe ajoutée : clipboard-202602171630-usaaz.png

~~~textile
Un service tourne bien en fond. Quel l'appareil soit en cour d'utilisation ou en veille. J'ai dû faire un slice Ice vers java. Je vais mettre mon alias qui copie les fichiers dans @src-capacitor\android\app\src\main\slice@

Le reste est fait lors de la compilation.

!clipboard-202602171630-usaaz.png!
~~~

### 20/02/2026 11:07 — Lucie Thomas

- Avancement : 0 % → 70 %

### 24/02/2026 10:11 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 05/05/2026 14:00 — Lucie Thomas

~~~textile
Le service fait bien le lien avec la webview ce qui limite les déconnexions. Si le service perd la connexion, une notification est envoyée pour l'informer.
~~~

### 12/10/2026 09:57 — Lucie Thomas

- Avancement : 70 % → 90 %
- Evolution majeure : (vide) → 0

~~~textile
le service tourne bien, de jeudi 15h à lundi 9h30, aucune déconnexion avec une reconnexion au re-lancement de l'application.
Uniquement Android car native.

Reste à déployer sur le playstore.
~~~

### 12/10/2026 13:10 — Alan Raynaud

- Début : (vide) → 05/10/2026

### 14/10/2026 15:21 — Lucie Thomas

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %
