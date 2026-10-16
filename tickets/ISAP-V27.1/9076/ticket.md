# #9076 — Migration net-snmp 5.9.5.2

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Plugins - Capteurs experts |
| Catégorie | com.egidium.snmp |
| Version cible | ISAP-V27.1 |
| Auteur | Pascal Vognin |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 22/09/2026 17:42 |
| Mis à jour le | 23/09/2026 16:44 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9076 |

## Description

~~~textile
Semble nécessaire suite à la montée de version openssl.

Les binaires openssl ont changé de nom depuis la 1.2.

<pre>
/* MSVC OpenSSL linker settings. */
#if defined(_MSC_VER)
#  if defined(NETSNMP_USE_OPENSSL)
#    ifdef _DLL
#      ifdef _DEBUG
#        pragma comment(lib, "libeay32MDd.lib")
#      else
#        pragma comment(lib, "libeay32MD.lib")
#      endif
#    else
#      ifdef _DEBUG
#        pragma comment(lib, "libeay32MTd.lib")
#      else
#        pragma comment(lib, "libeay32MT.lib")
#      endif
#    endif
#    pragma comment(lib, "gdi32.lib")
#    pragma comment(lib, "user32.lib")
#  endif
#endif
</pre>

Dans la dernière :
<pre>
/* MSVC OpenSSL linker settings. */
#if defined(_MSC_VER)
#  if defined(NETSNMP_USE_OPENSSL)
#    ifdef _DLL
#      pragma comment(lib, "libcrypto.lib")
#      pragma comment(lib, "libssl.lib")
#    else
#      pragma comment(lib, "libcrypto_static.lib")
#      pragma comment(lib, "libssl_static.lib")
#    endif
#    pragma comment(lib, "gdi32.lib")
#    pragma comment(lib, "user32.lib")
#  endif
#endif<
</pre>
~~~

## Relations

- Liée à #8736
- Bloque #6918

## Historique

### 22/09/2026 17:42 — Pascal Vognin

- Relation ajoutée (bloque) : #6918

### 22/09/2026 17:43 — Pascal Vognin

~~~textile
Nécessaire à la compilation de SNMPManager.exe
~~~

### 22/09/2026 17:43 — Alan Raynaud

- Catégorie : (vide) → com.egidium.snmp
- Début : (vide) → 23/09/2026
- Fonction : ISAP Core - Gestion des capteurs → ISAP Plugins - Capteurs experts

### 23/09/2026 15:16 — Alan Raynaud

- Sujet : « Migration net-snmp » → « Migration net-snmp 5.9.5.2 »

### 23/09/2026 16:12 — Alan Raynaud

- Statut : Nouveau → En cours
- Temps estimé : (vide) → 8.0 h

### 23/09/2026 16:44 — Alan Raynaud

~~~textile
Le script de build fourni semble plutôt bien marcher.

J'ai ajouté un readme qui expliquer comment l'utiliser.
~~~

### 23/09/2026 16:44 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 0 % → 100 %

### 02/10/2026 14:44 — Alan Raynaud

- Relation ajoutée (liée à) : #8736
