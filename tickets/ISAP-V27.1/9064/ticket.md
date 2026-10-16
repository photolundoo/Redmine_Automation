# #9064 — Migration cryptopp en 890

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - SDK |
| Catégorie | com.egidium.cryptopp |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Pascal Vognin |
| Avancement | 100 % |
| Créé le | 15/09/2026 17:35 |
| Mis à jour le | 13/10/2026 14:17 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Release notes | Non |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9064 |

## Description

~~~textile
La veille Version 562 du 20/02/2013 provoquait des warnings avec le nouvel environnement de compilation jenkins2 en debian13.
Du coup, j'en ai profité pour mettre à jour en Version 890 du 01/10/2023
~~~

## Historique

### 15/09/2026 17:36 — Fernand Alcatrao

- Catégorie : (vide) → com.egidium.cryptopp

### 15/09/2026 17:39 — Fernand Alcatrao

- Statut : Nouveau → En cours
- Assigné à : Fernand Alcatrao → Pascal Vognin
- Avancement : 0 % → 70 %

~~~textile
Il y avait encore des warnings sur Windows/linux, du coup 3 fichiers patchés avec le master en cours:
<pre><code class="diff">
##############################################
# Fix pour enlever des warnings en 890 (d'après master pour ces 3 fichiers):
##############################################
/c/DEV/EGIDIUM/com.cryptopp/private) diffbw "../../../SRC-EXTRA/cryptopp890.ORIG/esign.cpp" "./esign.cpp" # TAKE CARE: BACKUP IS OLDER !!!
++ diff -bw ../../../SRC-EXTRA/cryptopp890.ORIG/esign.cpp ./esign.cpp
113a114,116
> 		if (seedParam.size() > seed.ELEMS_MAX - 4)
> 			throw InvalidArgument("InvertibleESIGNFunction::GenerateRandom: buffer overflow");
>
/c/DEV/EGIDIUM/com.cryptopp/private) diffbw "../../../SRC-EXTRA/cryptopp890.ORIG/integer.cpp" "./integer.cpp" # TAKE CARE: BACKUP IS OLDER !!!
++ diff -bw ../../../SRC-EXTRA/cryptopp890.ORIG/integer.cpp ./integer.cpp
3059c3059
< #if (CRYPTOPP_MSC_VERSION >= 1500)
---
> #if (CRYPTOPP_MSC_VERSION >= 1500) && (CRYPTOPP_MSC_VERSION < 1938)
/c/DEV/EGIDIUM/com.cryptopp/private) diffbw "../../../SRC-EXTRA/cryptopp890.ORIG/zdeflate.cpp" "./zdeflate.cpp" # TAKE CARE: BACKUP IS OLDER !!!
++ diff -bw ../../../SRC-EXTRA/cryptopp890.ORIG/zdeflate.cpp ./zdeflate.cpp
415,421c415,416
< 			unsigned int len = (unsigned int)(
< #if defined(_STDEXT_BEGIN) && !(defined(CRYPTOPP_MSC_VERSION) && (CRYPTOPP_MSC_VERSION < 1400 || CRYPTOPP_MSC_VERSION >= 1600)) && !defined(_STLPORT_VERSION)
< 				stdext::unchecked_mismatch
< #else
< 				std::mismatch
< #endif
< #if CRYPTOPP_MSC_VERSION >= 1600
---
> 			unsigned int len = (unsigned int)(std::mismatch
> #if (CRYPTOPP_MSC_VERSION >= 1600) && (CRYPTOPP_MSC_VERSION < 1938)
/c/DEV/EGIDIUM/com.cryptopp/private) diffbw "../../../SRC-EXTRA/cryptopp-master/esign.cpp" "./esign.cpp" # TAKE CARE: BACKUP IS OLDER !!!
/c/DEV/EGIDIUM/com.cryptopp/private) diffbw "../../../SRC-EXTRA/cryptopp-master/integer.cpp" "./integer.cpp" # TAKE CARE: BACKUP IS OLDER !!!
/c/DEV/EGIDIUM/com.cryptopp/private) diffbw "../../../SRC-EXTRA/cryptopp-master/zdeflate.cpp" "./zdeflate.cpp" # TAKE CARE: BACKUP IS OLDER !!!
</code></pre>

Linux commité.

Pour Windows, Pascal profitera de sa compilation openssl/poco pour prendre en compte.
~~~

### 21/09/2026 13:57 — Alan Raynaud

- Début : (vide) → 21/09/2026

### 23/09/2026 10:48 — Pascal Vognin

~~~textile
<pre>
#NOK assembly Net 4.5 introuvable build_project aescryptclr DEBUG rebuild
#NOK assembly Net 4.5 introuvable build_project aescryptclr RELEASE rebuild
#NOK imagemagick imcompatibilty build_project genericrecorderplugin DEBUG rebuild
#NOK imagemagick imcompatibilty build_project genericrecorderplugin RELEASE rebuild
#NOK imagemagick imcompatibilty build_project indigovisionplugin DEBUG rebuild
#NOK imagemagick imcompatibilty build_project indigovisionplugin RELEASE rebuild
#NOK v145 non installé sur ma machine build_project csrplugin DEBUG rebuild
#NOK v145 non installé sur ma machine build_project csrplugin RELEASE rebuild
#NOK openssl imcompatibilty build_project snmpmanager DEBUG rebuild
#NOK openssl imcompatibilty build_project snmpmanager RELEASE rebuild
</pre>
~~~

### 13/10/2026 14:17 — Pascal Vognin

- Statut : En cours → Résolu
- Avancement : 70 % → 100 %

~~~textile
Fini en même temps que les case OpenSSL et Poco

#8805
~~~
