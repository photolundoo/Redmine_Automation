# #6918 — Migration POCO 1.15.3

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | ISAP Core - SDK |
| Catégorie | com.egidium.isap |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Pascal Vognin |
| Avancement | 100 % |
| Créé le | 20/04/2022 13:21 |
| Mis à jour le | 02/10/2026 09:35 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/6918 |

## Description

~~~textile
Version à déterminer.

La version actuellement utilisée (1.9.4) ne gère pas les cookies contenant l'attribut SameSite, ce qui pose problème.
~~~

## Relations

- Liée à #5705
- Liée à #6189
- Liée à #6721
- Liée à #8805
- Bloque #8208
- Bloque #8339
- Bloquée par #6017
- Bloquée par #9076

## Historique

### 20/04/2022 13:21 — Alan Raynaud

- Relation ajoutée (liée à) : #5705

### 20/04/2022 13:21 — Alan Raynaud

- Temps estimé : (vide) → 15.0 h

~~~textile
Estimation basée sur le temps passé dans #5705
~~~

### 20/04/2022 13:22 — Alan Raynaud

- Relation ajoutée (liée à) : #6189

### 04/05/2022 14:44 — Pascal Vognin

- Assigné à : Alan Raynaud → Pascal Vognin
- Début : (vide) → 04/05/2022

~~~textile
Je prends la main, on commence l'intégration dans un patch 5-4-1 pour techevent.

On pars sur la 1.11
~~~

### 04/05/2022 16:14 — Fernand Alcatrao

~~~textile
Comme indiqué ici #5705, on va être bloqué en tout cas avec poco : "La dernière version est la poco-1.10.1 mais VS2012 (110) n'est plus supporté. Il faut donc prendre la poco-1.9.4."
~~~

### 04/05/2022 16:54 — Fernand Alcatrao

~~~textile
Vu avec Pascal et Alan : on va faire un script python qui va faire les échange en FTP_TLS pour déposer sur un FTP local à la machine Viparis :
https://askcodez.com/ftpes-ftp-explicite-tls-ssl-en-python.html

Comme ça pas besoin de changer pour le moment le plugin techevent.
~~~

### 03/06/2022 14:00 — Alan Raynaud

- Début : 04/05/2022 → (vide)

### 29/06/2022 13:00 — Thibaut Wiart

- Version cible : ISAP-V5.5.1 → Candidate for next major release

### 07/03/2025 18:23 — Fernand Alcatrao

- Relation ajoutée (bloque) : #8208

### 07/03/2025 18:25 — Fernand Alcatrao

- Sujet : « Migration POCO » → « Migration POCO 1.14.1 »
- Version cible : Candidate for next major release → ISAP-V25.1
- Début : (vide) → 10/03/2025
- Temps estimé : 15.0 h → 24.0 h

### 10/03/2025 16:10 — Fernand Alcatrao

- Relation ajoutée (liée à) : #6721

### 28/07/2025 17:19 — Fernand Alcatrao

- Sujet : « Migration POCO 1.14.1 » → « Migration POCO 1.14.2 »

### 08/09/2025 14:46 — Alan Raynaud

- Version cible : ISAP-V25.1 → ISAP-V27.1

### 22/09/2025 17:03 — Alan Raynaud

~~~textile
Nettoyage du sprint hebdo en retirant les cases repoussés à la prochaine version.
~~~

### 22/09/2025 17:03 — Alan Raynaud

- Début : 10/03/2025 → (vide)

### 02/03/2026 08:58 — Pascal Vognin

- Statut : Nouveau → En cours
- Avancement : 0 % → 20 %

~~~textile
J'ai essayé une première compilation avec la nouvelle version qui date de 3 semaines : 1.15.0

Mais il n'y a pas le nécessaire comme avant (builwin.cmd)
J'ai quand même installé cmake via winget, et j'ai tenté de dérouler leur façon de faire.

Dans le cmake on a cette erreur :
<pre>
-- Could NOT find OpenSSL, try to set the path to OpenSSL root folder in the system variable OPENSSL_ROOT_DIR (missing: OPENSSL_CRYPTO_LIBRARY OPENSSL_INCLUDE_DIR) (Required is at least version "1.1.1")
</pre>
~~~

### 02/03/2026 08:59 — Pascal Vognin

~~~textile
J'ai donc essayé de revenir sur la version 1.14.2 comme indiqué par fernand (la précédente), mais je pense que openssl chez nous n'est pas à jour avec leur dépendances

Mais le link de la party crypto fail

<pre>
C:\DEV\EGIDIUM\org.pocoproject.cpplibs\poco2\Crypto\src\EVPCipherImpl.cpp(172,55): warning C4244: 'argument' : conversion de 'std::streamsize' en 'size_t',
 perte possible de données [C:\DEV\EGIDIUM\org.pocoproject.cpplibs\poco2\Crypto\Crypto_vs160.vcxproj]
  OpenSSL 1.0.1i 6 Aug 2014
     Création de la bibliothèque ..\lib\PocoCrypto.lib et de l'objet ..\lib\PocoCrypto.exp
RSACipherImpl.obj : error LNK2019: symbole externe non résolu _EVP_PKEY_type référencé dans la fonction "public: virtual __thiscall Poco::Crypto::RSACipher
Impl::~RSACipherImpl(void)" (??1RSACipherImpl@Crypto@Poco@@UAE@XZ) [C:\DEV\EGIDIUM\org.pocoproject.cpplibs\poco2\Crypto\Crypto_vs160.vcxproj]
RSADigestEngine.obj : error LNK2001: symbole externe non résolu _EVP_PKEY_type [C:\DEV\EGIDIUM\org.pocoproject.cpplibs\poco2\Crypto\Crypto_vs160.vcxproj]
</pre>
~~~

### 09/03/2026 08:17 — Pascal Vognin

- Relation ajoutée (liée à) : #8805

### 09/03/2026 10:09 — Alan Raynaud

- Début : (vide) → 02/03/2026

### 24/03/2026 14:14 — Fernand Alcatrao

- Relation ajoutée (bloque) : #8339

### 29/03/2026 21:37 — Pascal Vognin

- Avancement : 20 % → 60 %

### 22/09/2026 11:14 — Pascal Vognin

- Sujet : « Migration POCO 1.14.2 » → « Migration POCO 1.15.8 »
- Evolution majeure : (vide) → 0

### 22/09/2026 11:14 — Pascal Vognin

- Relation ajoutée (liée à) : #6017

### 22/09/2026 11:15 — Pascal Vognin

- Sujet : « Migration POCO 1.15.8 » → « Migration POCO 1.15.3 »
- Statut : En cours → Bloqué

### 22/09/2026 11:17 — Alan Raynaud

- Relation supprimée (liée à) : #6017

### 22/09/2026 11:17 — Alan Raynaud

- Relation ajoutée (bloquée par) : #6017

### 22/09/2026 14:06 — Fernand Alcatrao

~~~textile
> Migration POCO 1.15.8 à Migration POCO 1.15.3
Typo ? La 1.15.8 ne semble pas encore exister.
~~~

### 22/09/2026 17:42 — Pascal Vognin

- Relation ajoutée (bloquée par) : #9076

### 24/09/2026 17:55 — Fernand Alcatrao

~~~textile
Pris en compte et livré sous CVS pour linux (avec OpenSSL 3 aussi).

PI je me demandais quel c++ étaient utilisé par Poco qui autogénère les makefile. Voici comment :
<pre>
vmlfr-jenkins2:/c/DEV/EGIDIUM/org.pocoproject.cpplibs/private/cmake-build) strings ./Zip/CMakeFiles/Zip.dir/src/ZipStream.cpp.o | grep -- "-std="
GNU C++20 14.2.0 -mtune=generic -march=x86-64 -g -O2 -std=gnu++20 -fPIC -fasynchronous-unwind-tables
vmlfr-jenkins2:/c/DEV/EGIDIUM/org.pocoproject.cpplibs/private/cmake-build)
</pre>
~~~

### 02/10/2026 09:34 — Pascal Vognin

- Statut : Bloqué → En cours

### 02/10/2026 09:35 — Pascal Vognin

- Statut : En cours → Résolu
- Avancement : 60 % → 100 %

~~~textile
Les migrations snmp et imagemagick ont été réalisées.
~~~
