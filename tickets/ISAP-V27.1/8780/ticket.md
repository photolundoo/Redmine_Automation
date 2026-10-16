# #8780 — [IsapMobile] Les fonctionnalités utilisant des liens FTP(S) ne fonctionnent plus

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | ISAP Fonctions mobiles - Tracking mobile des positions |
| Catégorie | com.egidium.isap.mobile |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Lucie Thomas |
| Avancement | 100 % |
| Créé le | 23/02/2026 12:35 |
| Mis à jour le | 28/09/2026 14:28 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V25.1 |
| Lien Redmine | https://srvfr-redmine/issues/8780 |

## Description

~~~textile
Surement un problème côté serveur suite à une MàJ de FileZilla Server.
~~~

## Relations

- Liée à #8346
- Liée à #2541

## Historique

### 23/02/2026 13:48 — Alan Raynaud

- Relation ajoutée (liée à) : #8346

### 16/03/2026 14:08 — Alan Raynaud

- Assigné à : Fernand Alcatrao → Lucie Thomas

### 17/03/2026 16:56 — Lucie Thomas

- Avancement : 0 % → 80 %

~~~textile
Le FTPs fonctionne, c'était un problème avec les sessions TLS (Problème connu sur FTPs). 
Pour ça on contourne des restrictions mise sur android avec une librairie tiers. (apk android 28+)

Il y a des problèmes lors du premier lancement de l'application. J'ai du forcer l'arrêt dans les paramètres pour que l'application fonctionne correctement. (FTPs server puis si on swipe l'application, elle redémarre à plusieurs reprise. Second comportement pas constant)

Apk push

J'ai suivis ce qui a été fait dans ce stackoverflow (la seule réponse)
https://stackoverflow.com/questions/79026706/android-ftps-upload-issue-425-unable-to-build-data-connection-tls-session-of

il mène à ces deux réponses :
https://stackoverflow.com/questions/61348963/android-ftps-session-reuse-no-field-sessionhostportcache/62425820#62425820
https://stackoverflow.com/questions/61348963/android-ftps-session-reuse-no-field-sessionhostportcache/75539799#75539799
~~~

### 18/03/2026 14:00 — Fernand Alcatrao

~~~textile
Le site SFTP est : sftp.egidium.fr
Même user/mdp que pour l'ancien FTPS.

Restera à sécuriser :
* J'ai dû mettre @PasswordAuthentication yes@ dans /etc/ssh/sshd_config pour permettre de se connecter avec un mdp et donc sans certificats (obligerait à avoir un certificat par téléphone).
* Si on fait @sudo usermod -s /sbin/nologin isap_mobile@ pour désactiver la connexion via ssh, la connexion à SFTP ne se fonctionne plus
* Rendre le compte captif dans son répertoire (ne pas permettre d'aller vers ..)
* Obligation d'ouvrir le port ssh à public
* ...
~~~

### 18/03/2026 14:02 — Fernand Alcatrao

~~~textile
J'ai commencer à documenter ici : M:\DEVELOPPEMENTS\Documentation interne\Linux\01_Setup_VM.docx § 35
~~~

### 19/03/2026 10:11 — Fernand Alcatrao

~~~textile
Point oublié hier :
* Obligation d'ouvrir le port ssh à public
~~~

### 20/03/2026 10:14 — Fernand Alcatrao

- Relation ajoutée (liée à) : #2541

### 24/03/2026 11:29 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 09/04/2026 10:45 — Lucie Thomas

~~~textile
Les logs se trouvent dans @Android/data/com.egidium.isap.mobile/files@

Attention, il ne faut pas utiliser l'application de google
démarche avec files (google) :
- Ouvrir *Autre espace de stockage*
- *Trace du système*
- dans l'explorateur, choisir le téléphone (chez moi pixel 10)
- accèder aux logs @Android/data/com.egidium.isap.mobile/files@
~~~

### 10/04/2026 13:39 — Fernand Alcatrao

~~~textile
Sur FairPhone c'est plus compliqué. Avec Files de google :
* Autres espace de stockage en bas
* Rapports de bugs
* Puis icônes en haut à gauche choisir 'The FairPhone'
* Puis comme Lucie Android/data/com.egidium.isap.mobile/files/logs

Comme les fichiers de logs reçu via FTPS sur tacticplan, il n'y a que des fichiers YYYY-MM-DD-LogCat.log qui contiennent très peu de choses. Aucun vrai fichiers de logs applicatifs.
~~~

### 28/09/2026 14:28 — Alan Raynaud

- Statut : En cours → Résolu
- Début : 23/02/2026 → (vide)

~~~textile
On a un contournement degeu. La vrai solution sera SFTP #2541 
~~~

### 28/09/2026 14:28 — Alan Raynaud

- Avancement : 80 % → 100 %
