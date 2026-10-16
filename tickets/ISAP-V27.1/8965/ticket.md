# #8965 — [MobileApp] Permettre de configurer son serveur au lancement

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Core - Gestion mobilité |
| Catégorie | com.egidium.isap.reporting |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8754 |
| Auteur | Fernand Alcatrao |
| Assigné à | Lucie Thomas |
| Avancement | 100 % |
| Créé le | 22/07/2026 11:37 |
| Mis à jour le | 25/09/2026 15:44 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Versailles Grand Parc |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8965 |

## Description

~~~textile
Ce sera à demander au premier lancement. Mettre aussi une option (bouton "pas trop visible") pour permettre de le changer.
Plutôt que de permettre de taper "vgp" qu'on transformera en vgp.egidium.fr/isap-vgp.egidium.fr, j'ai pensé à transformer vgp en un code réversible pour éviter les "force brutes" surtout si on connait nos clients.

Faudra adapter le code python ci-joint généré par IA pour faire le décodage dans la MobileApp.

L'idéal est sans doute d'avoir un serveur intermédiaire que ferait le liens entre un code/chiffre et une machine ? Mais bon ça ira dans un premier temps.

Avec l'algo généré, on est limité à 11 caractères pour le nom du client. Au pire on créera des alias, par exemple torann-fr pour torann-france.
On pourrait aussi essayer de trouver un meilleur algo.

*Il ne faut pas déployer sur le PlayStore une nouvelle appli sans ce mécanisme (et contenant à la place vgp en dur).*
~~~

## Pièces jointes

- [numeric_cipher.py](pieces_jointes/numeric_cipher.py) — 8 Ko, ajoutée par Fernand Alcatrao le 22/07/2026 11:36

## Historique

### 22/07/2026 11:37 — Fernand Alcatrao

~~~textile
<pre>
$ python numeric_cipher.py encode vgp
9zhL0QXCcX
$ python numeric_cipher.py decode 9zhL0QXCcX
vgp
$
</pre>
~~~

### 22/07/2026 11:40 — Fernand Alcatrao

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 22/07/2026 11:44 — Fernand Alcatrao

~~~textile
Commité ici avec un autre nom : /c/DEV/EGIDIUM/com.egidium.tools.python/private/Crypt-DNS-ShortName.py
Il nous le faudra pour générer les codes à transmettre au client.
<pre>
$ priv tools.python
$ python Crypt-DNS-ShortName.py encode vgp
9zhL0QXCcX
$ python Crypt-DNS-ShortName.py decode 9zhL0QXCcX
vgp
$ 
</pre>
~~~

### 22/07/2026 12:29 — Fernand Alcatrao

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 03/08/2026 10:07 — Lucie Thomas

- Evolution majeure : (vide) → 0

~~~textile
Est-ce qu'il ne serait pas bon de communiquer le code au serveur qui lui décode et redirige le client vers le bon serveur (puis stocké en cache blablabla) ?

Est-ce que je fais le dev dans le serveur de la webapp ou le python (ou autre) serait un service à part ?

Il nous faut plus de 11 charactère si on veut pouvoir y mettre typiquement "isap-demo-smartshield-erp.egidium.fr"
~~~

### 10/08/2026 15:34 — Lucie Thomas

~~~textile
Décision :

L'utilisateur doit taper l'url vers le serveur en question avant la page de login. Une fois spécifié, c'est stocké dans les sharedPreferences. Pour le modifier, ajout d'un bouton sa la page de login.

Pas de cipher ni d'accès à serveur distant pour rerouter. (car c'est l'équivalent de le faire sur le web, juste plus compliqué sur mobile)
~~~

### 12/08/2026 11:50 — Lucie Thomas

- Avancement : 0 % → 80 %

### 14/08/2026 12:55 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 14/08/2026 17:01 — Lucie Thomas

- Avancement : 80 % → 90 %

### 31/08/2026 13:45 — Lucie Thomas

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %

### 18/09/2026 11:20 — Lucie Thomas

- Ticket parent : (vide) → #8754

### 25/09/2026 15:44 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V27.1
