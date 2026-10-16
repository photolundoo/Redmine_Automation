# #8805 — Mise à jour openSSL 3.5.8

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - SDK |
| Catégorie | com.egidium.isap |
| Version cible | ISAP-V27.1 |
| Auteur | Pascal Vognin |
| Assigné à | Pascal Vognin |
| Avancement | 100 % |
| Créé le | 09/03/2026 08:16 |
| Mis à jour le | 01/10/2026 14:37 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8805 |

## Description

~~~textile
Poco ne supporte plus openSSL 1.1.0 que l'on utilise.

Le mieux d'après tout ce que j'ai lu serait de monter à la version de openSSL la plus récente.
~~~

## Relations

- Liée à #6918

## Pièces jointes

- [clipboard-202603091421-6hdky.png](pieces_jointes/clipboard-202603091421-6hdky.png) — 50 Ko, ajoutée par Alan Raynaud le 09/03/2026 14:21

## Historique

### 09/03/2026 08:17 — Pascal Vognin

- Relation ajoutée (liée à) : #6918

### 09/03/2026 13:17 — Pascal Vognin

- Sujet : « Mise à jour openSSL 3.6.5 » → « Mise à jour openSSL 3.6.1 »
- Statut : Nouveau → En cours
- Avancement : 0 % → 20 %

~~~textile
Il y a tous les projets qui utilisent com.egidium.licensing qui embarquent un bout de openssl
Via l'include #include <applink.c>

Voici la liste des projets qui ont l'air d'utiliser openssl
<pre>
./com.egidium.api/
./com.egidium.bb.events/private/IsapServer/
./com.egidium.licensing/
./com.egidium.rtspserver/
./org.apache.log4cxx
./org.net-snmp
./org.pocoproject.cpplibs
</pre>
~~~

### 09/03/2026 13:21 — Pascal Vognin

~~~textile
Je me suis cassé les dents sur la compilation/tests de openssl 3.6.1.

Dans le doute j'ai quand même compilé openssl et run leur test en 1.1.1w. Et ça a l'air d'aller au bout.

Gros "changement" les .lib ne sont plus plus libeay32.dll et ssleay32.lib

J'ai généré ça:
libcrypto-1_1.dll
libssl-1_1.dll

libcrypto.lib
libssl-1_1.dll

Ca a aussi l'air de dépendre d'un répertoire engine :
lib/engines-1_1/capi.dll
lib/engines-1_1/padlock.dll
~~~

### 09/03/2026 14:22 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202603091421-6hdky.png

~~~textile
Pour référence, les versions

!clipboard-202603091421-6hdky.png!
~~~

### 22/03/2026 22:20 — Pascal Vognin

- Sujet : « Mise à jour openSSL 3.6.1 » → « Mise à jour openSSL 3.5.5 »
- Avancement : 20 % → 50 %

### 23/09/2026 14:41 — Pascal Vognin

- Sujet : « Mise à jour openSSL 3.5.5 » → « Mise à jour openSSL 3.5.8 »
- Evolution majeure : (vide) → 0

### 23/09/2026 16:49 — Alan Raynaud

~~~textile
Ràf de Pascal :
* aescryptclr : je regarde, mais c'est de toute façon très certainement quelque chose que nous n'utilisons pas
* genericrecorderplugin  et indigovisionplugin : #6017 à faire
* csrplugin : c'est juste que le projet a été fait directement en VS2026, donc l'alias basé sur VS2019 n'arrive pas à le compiler. A basculer en ciblage VS2019 pour le moment ? Je regarde
* snmpmanager : #9076 fait
~~~

### 24/09/2026 15:35 — Fernand Alcatrao

~~~textile
Makefiles modifiés sous linux pour ne plus utiliser le vieux libssl.so.1.0.0.

Il y a un warning sur licensing :
<pre>
g++ -std=c++20 -fPIC -O2 -I. -I../../public/inc -I../../../com.egidium.hash/public/inc -I../../../com.egidium.isap.sdk/public/inc -I/usr/include -o X509Utils.o -c X509Utils.cpp
LicenseVerifierImpl.cpp: In member function ‘void EgidiumLicensingLibrary::LicenseVerifierImpl::validateSignature(LicenseVerificationCallback)’:
LicenseVerifierImpl.cpp:373:39: warning: ‘rsa_st* EVP_PKEY_get1_RSA(EVP_PKEY*)’ is deprecated: Since OpenSSL 3.0 [-Wdeprecated-declarations]
  373 |       RSA *l_rsa = ::EVP_PKEY_get1_RSA(l_ptrPublicKey);
      |                    ~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~
In file included from /usr/include/openssl/x509.h:31,
                 from X509Utils.h:6,
                 from LicenseVerifierImpl.cpp:23:
/usr/include/openssl/evp.h:1398:16: note: declared here
 1398 | struct rsa_st *EVP_PKEY_get1_RSA(EVP_PKEY *pkey);
      |                ^~~~~~~~~~~~~~~~~
LicenseVerifierImpl.cpp:380:45: warning: ‘int RSA_public_decrypt(int, const unsigned char*, unsigned char*, RSA*, int)’ is deprecated: Since OpenSSL 3.0 [-Wdeprecated-declarations]
  380 |       int l_idatasize = ::RSA_public_decrypt(l_iPtrDecodedSignatureSize,l_ptrDecodedSignature,(unsigned char*)l_ptrdata,l_rsa,RSA_PKCS1_PADDING);
      |                         ~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In file included from /usr/include/openssl/x509.h:38:
/usr/include/openssl/rsa.h:298:5: note: declared here
  298 | int RSA_public_decrypt(int flen, const unsigned char *from, unsigned char *to,
      |     ^~~~~~~~~~~~~~~~~~
</pre>

L'IA propose :
<pre><code class=\"diff\">
/c/DEV/EGIDIUM/com.egidium.licensing) cvsdiff
Index: private/EgidiumLicenseGenerator/LicenseGenerator.cpp
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.licensing/private/EgidiumLicenseGenerator/LicenseGenerator.cpp,v
retrieving revision 1.4
diff -b -w -r1.4 LicenseGenerator.cpp
397c397
<    ::RSA* l_rsaEngine = NULL;
---
>    EVP_PKEY* l_ptrPrivateKey = NULL;
399c399
<    if( ::PEM_read_RSAPrivateKey(l_cFileKey,&l_rsaEngine,NULL,NULL) != NULL )
---
>    if( l_cFileKey != NULL )
400a401
>       l_ptrPrivateKey = ::PEM_read_PrivateKey(l_cFileKey, NULL, NULL, NULL);
402,406c403
<       // TODO: verify that the loaded key is actually associated with the used certificate
<
<       size_t encryptedBytesSize = ::RSA_size(l_rsaEngine);
<       (*_outputbuffer) = (unsigned char*) OPENSSL_malloc(encryptedBytesSize*sizeof(unsigned char));
<       memset((void *)(*_outputbuffer), 0x0, encryptedBytesSize);
---
>    }
408,410c405,428
<       l_iSigned = ::RSA_private_encrypt(_data.size(),(const unsigned char*)_data.c_str(),(*_outputbuffer),l_rsaEngine,RSA_PKCS1_PADDING);
<
<       OPENSSL_free(l_rsaEngine);
---
>    if( l_ptrPrivateKey != NULL )
>    {
>       // TODO: verify that the loaded key is actually associated with the used certificate
>       ::EVP_PKEY_CTX* l_ptrCtx = ::EVP_PKEY_CTX_new(l_ptrPrivateKey, NULL);
>       if( l_ptrCtx != NULL )
>       {
>          if( ::EVP_PKEY_encrypt_init(l_ptrCtx) > 0
>             && ::EVP_PKEY_CTX_set_rsa_padding(l_ptrCtx, RSA_PKCS1_PADDING) > 0 )
>          {
>             size_t l_iEncryptedSize = 0;
>             if( ::EVP_PKEY_encrypt(l_ptrCtx, NULL, &l_iEncryptedSize,
>                   (const unsigned char*)_data.c_str(), _data.size()) > 0 )
>             {
>                (*_outputbuffer) = (unsigned char*)OPENSSL_malloc(l_iEncryptedSize);
>                memset((void *)(*_outputbuffer), 0x0, l_iEncryptedSize);
>                l_iSigned = (int)::EVP_PKEY_encrypt(l_ptrCtx, (*_outputbuffer), &l_iEncryptedSize,
>                   (const unsigned char*)_data.c_str(), _data.size());
>                if( l_iSigned > 0 )
>                   l_iSigned = (int)l_iEncryptedSize;
>             }
>          }
>          ::EVP_PKEY_CTX_free(l_ptrCtx);
>       }
>       ::EVP_PKEY_free(l_ptrPrivateKey);
Index: private/EgidiumLicenseVerifier/LicenseVerifierImpl.cpp
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.licensing/private/EgidiumLicenseVerifier/LicenseVerifierImpl.cpp,v
retrieving revision 1.11
diff -b -w -r1.11 LicenseVerifierImpl.cpp
301,303c301,303
<    if (m_Hosts.count(l_currentHostId) == 0) { // Host non trouv dans le fichier de license
< #ifndef _WIN32 // Sous Linux on tente la licence spciale
<       if (m_Hosts.count(\"000000000000\") == 0) { // License spciale non trouve dans le fichier de license
---
>    if (m_Hosts.count(l_currentHostId) == 0) { // Host non trouvé dans le fichier de license
> #ifndef _WIN32 // Sous Linux on tente la licence spéciale
>       if (m_Hosts.count(\"000000000000\") == 0) { // License spéciale non trouvée dans le fichier de license
310c310
<       else if (!m_Hosts[\"000000000000\"].isCurrentlyValid()) { // License expire
---
>       else if (!m_Hosts[\"000000000000\"].isCurrentlyValid()) { // License expirée
326c326
<    else if(!m_Hosts[l_currentHostId].isCurrentlyValid()) { // License expire
---
>    else if(!m_Hosts[l_currentHostId].isCurrentlyValid()) { // License expirée
373d372
<       RSA *l_rsa = ::EVP_PKEY_get1_RSA(l_ptrPublicKey);
377d375
<       EgidDebug() << l_rsa;
379,380c377,392
<       char* l_ptrdata = (char*)OPENSSL_malloc(256*sizeof(char));
<       int l_idatasize = ::RSA_public_decrypt(l_iPtrDecodedSignatureSize,l_ptrDecodedSignature,(unsigned char*)l_ptrdata,l_rsa,RSA_PKCS1_PADDING);
---
>       const size_t l_iBufferSize = 256;
>       char* l_ptrdata = (char*)OPENSSL_malloc(l_iBufferSize + 1);
>       size_t l_idatasize = 0;
>
>       ::EVP_PKEY_CTX* l_ptrCtx = ::EVP_PKEY_CTX_new(l_ptrPublicKey, NULL);
>       if( l_ptrCtx != NULL
>           && ::EVP_PKEY_verify_recover_init(l_ptrCtx) > 0
>           && ::EVP_PKEY_CTX_set_rsa_padding(l_ptrCtx, RSA_PKCS1_PADDING) > 0 )
>       {
>          l_idatasize = l_iBufferSize;
>          if( ::EVP_PKEY_verify_recover(l_ptrCtx,
>                                        (unsigned char*)l_ptrdata, &l_idatasize,
>                                        l_ptrDecodedSignature, (size_t)l_iPtrDecodedSignatureSize) <= 0 )
>             l_idatasize = 0;
>       }
>
394a407,408
>       if( l_ptrCtx != NULL )
>          ::EVP_PKEY_CTX_free(l_ptrCtx);
/c/DEV/EGIDIUM/com.egidium.licensing) 
</code></pre>

Mais je ne touche pas. Je testerais après avoir commité.
~~~

### 25/09/2026 10:31 — Fernand Alcatrao

~~~textile
Pascal,
Suis tombé sur Iris la dessus et du c oup chercher partout :
<pre>
/c/DEV/EGIDIUM) look libeay32.dll
"./com.egidium.iris/public/bin/Win32/libeay32.dll"
"./com.egidium.shared/public/bin/x64/libeay32.dll"
"./com.egidium.zenitel/public/bin/Win32/libeay32.dll"
"./fr.cea.list.isim.navmesh-generator/public/bin/win32/libeay32.dll"
"./fr.cea.list.isim.navmesh-generator/public/bin/x64/libeay32.dll"
/c/DEV/EGIDIUM)
</pre>

Faudrait : 
* Faire le ménage dans com.egidium.shared/public/bin/x64 ?
* Migrer Iris Windows
* Zeintel ?
* Pour cea.list, laisson tomber
~~~

### 25/09/2026 10:33 — Fernand Alcatrao

~~~textile
Mathieu, pourquoi avoir mis les dll openssl 1 à côté des exe ? Normalement on avait les mêmes dans shared.
~~~

### 25/09/2026 11:26 — Mathieu Fournet-Carcopino

~~~textile
Ce ne sont pas les mêmes DLL : Iris n'utilise pas la même version d'OpenSSL que celle présente dans shared. Iris est sur la version 1.0.2o d'openssl (libeay32 / ssleay32). Et les seuls libeay32/ssleay32 de shared sont en x64, alors qu'Iris est en 32 bits.
La cause : libcurl n'existe pas dans shared, et la version de curl que j'utilise est liée aux DLL OpenSSL qui se trouvent à côté des exes.
On peut pousser ces DLL dans shared, mais je pense qu'il vaut mieux que je cherche une version de curl qui s'appuie sur les DLL OpenSSL déjà présentes dans shared.
~~~

### 25/09/2026 11:27 — Pascal Vognin

~~~textile
Zenitel comme UaePlugin dépend de OpcUA, qui vient avec sa version d'openssl.
J'ai supprimé les dll obsolètes

Le répertoire shared/public/bin/x64
Je ne sais pas qui le maintient et à qui il est utile, je ne m'en suis pas occupé du tout durant les compilations et recompilation les 5 dernière années


Iris, j'ai trouvé ça étrange, mais on utilise des packages spécifiques, il me semble que Alan avait suivi ça
<pre>
	Ligne   4:   <Import Project="..\packages\rmt_openssl.1.1.0.3\build\native\rmt_openssl.props" Condition="Exists('..\packages\rmt_openssl.1.1.0.3\build\native\rmt_openssl.props')" />
	Ligne   6:   <Import Project="..\packages\openssl.1.0.1.21\build\native\openssl.props" Condition="Exists('..\packages\openssl.1.0.1.21\build\native\openssl.props')" />
	Ligne 226:     <Import Project="..\packages\openssl.redist.1.0.1.21\build\native\openssl.redist.targets" Condition="Exists('..\packages\openssl.redist.1.0.1.21\build\native\openssl.redist.targets')" />
	Ligne 229:     <Import Project="..\packages\openssl.1.0.1.21\build\native\openssl.targets" Condition="Exists('..\packages\openssl.1.0.1.21\build\native\openssl.targets')" />
	Ligne 232:     <Import Project="..\packages\rmt_openssl.1.1.0.3\build\native\rmt_openssl.targets" Condition="Exists('..\packages\rmt_openssl.1.1.0.3\build\native\rmt_openssl.targets')" />
	Ligne 234:     <Import Project="..\packages\openssl-vc141-static-x86_64.1.0.2\build\native\openssl-vc141-static-x86_64.targets" Condition="Exists('..\packages\openssl-vc141-static-x86_64.1.0.2\build\native\openssl-vc141-static-x86_64.targets')" />
	Ligne 243:     <Error Condition="!Exists('..\packages\openssl.redist.1.0.1.21\build\native\openssl.redist.targets')" Text="$([System.String]::Format('$(ErrorText)', '..\packages\openssl.redist.1.0.1.21\build\native\openssl.redist.targets'))" />
</pre>
~~~

### 25/09/2026 11:30 — Fernand Alcatrao

~~~textile
@mathieu.carcopino : Non la question c'est que désormais dans Shared on a OpenSSL 3.5.8. Du coup on peux migrer pour faire propre ?
Le mieux c'est que ce soit toi qui t'en occupe.
~~~

### 25/09/2026 13:07 — Mathieu Fournet-Carcopino

~~~textile
Je suis entrain de regarder pour migrer. Comme je dois compiler libcurl compatible avec la version 3.5.8 d'openssl, serait-il bien de l'ajouter dans shared ou je le laisse dans iris ?
~~~

### 25/09/2026 13:23 — Pascal Vognin

~~~textile
La version 3.5.8 est livrée ici

"C:\DEV\EGIDIUM\org.openssl\public"

Les lib ont changé de nom depuis la 1.2 d'openssl
C'est maintenant libcrypto.lib et libssl.lib

Attention pour compiler poco "simplement" j'ai dû renommer "C:\DEV\EGIDIUM\org.openssl\public\bin" en "C:\DEV\EGIDIUM\org.openssl\public\lib"
Car il cherche une hierarchie de dossier spécifique.

Alan pour snmp avait besoin de créer un sous répertoire "MD"
~~~

### 25/09/2026 14:19 — Fernand Alcatrao

~~~textile
Pour le moment libcurl ne sert qu'à Iris donc laissons le dans Iris pour le moement.
Mais essayons d'utiliser le SSL 3 qui est dans shared.
~~~

### 25/09/2026 15:20 — Alan Raynaud

~~~textile
Projets que Pascal n'avait pas pu compiler :

|_.Projet|_.Cause|_.Statut|
|aescryptclr|????|={background-color: lightgreen;}. OK|
|genericrecorderplugin|/2. Vieille version de ImageMagick non compatible C++20 (#6017)|={background-color: lightgreen;}. OK|
|indigovisionplugin|={background-color: lightgreen;}. OK|
|csrplugin|Le ciblage était 145 (VS2019) au lieu de 142 (VS2019)|={background-color: lightgreen;}. OK|
|snmpmanager| Vieille version de Net-SNMP non compatible C++20 (#9076)|={background-color: lightgreen;}. OK|
~~~

### 01/10/2026 09:10 — Alan Raynaud

- Assigné à : Pascal Vognin → Alan Raynaud

### 01/10/2026 14:35 — Alan Raynaud

- Assigné à : Alan Raynaud → Pascal Vognin
- Avancement : 50 % → 90 %

~~~textile
OK de mon coté (projets restants)

Est-ce que tout est terminé ?
~~~

### 01/10/2026 14:37 — Pascal Vognin

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %

~~~textile
Pour moi tout est ok
~~~
