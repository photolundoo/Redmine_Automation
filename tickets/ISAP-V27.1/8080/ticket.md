# #8080 — Compilation linux sur un environnement récent (Debian 13)

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - SDK |
| Catégorie | com.egidium.isap |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Fernand Alcatrao |
| Avancement | 100 % |
| Créé le | 05/08/2024 14:31 |
| Mis à jour le | 25/09/2026 15:44 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8080 |

## Description

~~~textile
La compilation linux se fait aujourd’hui sur un ubuntu 16.04 (vmlfr-jenkins) qui commence à dater.
Il faudrait avoir une nouvelle VM (vmlfr-ubuntu24) pour faire cette compilation.

Les instructions se trouvent ici :
"M:\DEVELOPPEMENTS\Documentation interne\Linux\02_Compilation_Linux.docx"

C'est un peu brouillon et j'ai commencé à MàJ. Faudra bien le mettre au propre.
~~~

## Relations

- Liée à #8309
- Liée à #9052

## Historique

### 05/08/2024 14:33 — Fernand Alcatrao

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 05/08/2024 18:06 — Fernand Alcatrao

- Avancement : 0 % → 30 %

~~~textile
h2. Projets à faire 1 fois (comme indiqué dans 02_Compilation_Linux.docx)

h3. Ice 3.7.10 : génère un segmentation fault dans IsapServer

J'ai tenté de prendre la dernière version de Ice 3.7.10. Tout "ISAP" compile mais Segmentation fault (core dumped) en lançant IsapServer :
<pre>
vmlfr-ubuntu24:/usr/local/isap/com.egidium.bb.events/public/bin/linux) sudo su isap -c "gdb /usr/local/isap/com.egidium.bb.events/public/bin/linux/IsapServer"                                                              GNU gdb (Ubuntu 15.0.50.20240403-0ubuntu1) 15.0.50.20240403-git
Copyright (C) 2024 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from /usr/local/isap/com.egidium.bb.events/public/bin/linux/IsapServer...
(gdb) run --Ice.Config='/var/lib/isap/data/isapgrid/data_node/servers/ISAP Server/config/config'
Starting program: /c/DEV/EGIDIUM/com.egidium.bb.events/public/bin/linux/IsapServer --Ice.Config='/var/lib/isap/data/isapgrid/data_node/servers/ISAP Server/config/config'
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
warning: could not find '.gnu_debugaltlink' file for /lib/x86_64-linux-gnu/libcap.so.2

Program received signal SIGSEGV, Segmentation fault.
0x00007ffff77571dc in Ice::upCast(Ice::ValueFactory*) () from /lib/x86_64-linux-gnu/libIce.so.37
(gdb)
</pre>

Du coup retour arrière avec Ice 3.6.5 avant de poursuivre avec Ice 3.7.10.

PI les Makefile utilisent $EGIDIUM_HOME et non ce qui est dans /usr/lib.
Donc "facile de switcher" entre les 2.

h3. SQLAPI : OK

Pas de nécessité de migrer du coup, j'ai pas touché. Ca a juste été recompilé.

h3. POCO : ne compile plus

Une erreur et plein de warnings en plus:
<pre>
/home/egidium/tmp/tmp/poco/Crypto/src/RSACipherImpl.cpp: In function ‘int Poco::Crypto::{anonymous}::mapPaddingMode(RSAPaddingMode)’:
/home/egidium/tmp/tmp/poco/Crypto/src/RSACipherImpl.cpp:54:32: error: ‘RSA_SSLV23_PADDING’ was not declared in this scope; did you mean ‘RSA_NO_PADDING’?
   54 |                         return RSA_SSLV23_PADDING;
      |                                ^~~~~~~~~~~~~~~~~~
      |                                RSA_NO_PADDING

...
In file included from /home/egidium/tmp/tmp/poco/Foundation/src/DirectoryIteratorStrategy.cpp:15:
/home/egidium/tmp/tmp/poco/Foundation/include/Poco/DirectoryIteratorStrategy.h:35:22: warning: ‘template<class _Arg, class _Result> class std::pointer_to_unary_function’ is deprecated [-Wdeprecated-declarations]
   35 |         typedef std::pointer_to_unary_function<const Stack&, UInt16> DepthFunPtr;
      |                      ^~~~~~~~~~~~~~~~~~~~~~~~~
In file included from /usr/include/c++/13/string:49,
                 from /home/egidium/tmp/tmp/poco/Foundation/include/Poco/Bugcheck.h:22,
                 from /home/egidium/tmp/tmp/poco/Foundation/include/Poco/Foundation.h:163,
                 from /home/egidium/tmp/tmp/poco/Foundation/include/Poco/DirectoryIteratorStrategy.h:21:
/usr/include/c++/13/bits/stl_function.h:1105:11: note: declared here
 1105 |     class pointer_to_unary_function : public unary_function<_Arg, _Result>
      |           ^~~~~~~~~~~~~~~~~~~~~~~~~
...
In file included from /home/egidium/tmp/tmp/poco/Crypto/include/Poco/Crypto/RSAKeyImpl.h:22,
                 from /home/egidium/tmp/tmp/poco/Crypto/include/Poco/Crypto/RSAKey.h:23,
                 from /home/egidium/tmp/tmp/poco/Crypto/src/CipherFactory.cpp:18:
/home/egidium/tmp/tmp/poco/Crypto/include/Poco/Crypto/EVPPKey.h: In member function ‘bool Poco::Crypto::EVPPKey::operator==(const Poco::Crypto::EVPPKey&) const’:
/home/egidium/tmp/tmp/poco/Crypto/include/Poco/Crypto/EVPPKey.h:295:34: warning: ‘int EVP_PKEY_cmp(const EVP_PKEY*, const EVP_PKEY*)’ is deprecated: Since OpenSSL 3.0 [-Wdeprecated-declarations]
  295 |         return (1 == EVP_PKEY_cmp(_pEVPPKey, other._pEVPPKey));
      |                      ~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~
...
</pre>

La dernière version poco-1.13.3-release compile bien mais n'est pas compatible avec notre code (c++17 et les .h ne sont pas compatibles et du coup plein d'erreurs avec nos compilations "ISAP").

Du coup j'ai pris la poco-1.12.5p2-release, la dernière en c++14, qui compile bien et ne provoque pas d'erreur de compilation chez nous. Il y a juste 2 warnings pas grave du tout :
[ 74%] Building CXX object JWT/CMakeFiles/JWT.dir/src/Token.cpp.o
<pre>
/home/egidium/tmp/tmp/poco/Net/src/PollSet.cpp: In member function ‘Poco::Net::PollSet::SocketModeMap Poco::Net::PollSetImpl::poll(const Poco::Timespan&)’:
/home/egidium/tmp/tmp/poco/Net/src/PollSet.cpp:224:37: warning: ignoring return value of ‘ssize_t read(int, void*, size_t)’ declared with attribute ‘warn_unused_result’ [-Wunused-result]
  224 |                                 read(_eventfd, &val, sizeof(val));
      |                                 ~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
/home/egidium/tmp/tmp/poco/Net/src/PollSet.cpp: In member function ‘void Poco::Net::PollSetImpl::wakeUp()’:
/home/egidium/tmp/tmp/poco/Net/src/PollSet.cpp:241:22: warning: ignoring return value of ‘ssize_t write(int, const void*, size_t)’ declared with attribute ‘warn_unused_result’ [-Wunused-result]
  241 |                 write(_eventfd, &val, sizeof(val));
      |                 ~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~
</pre>

PI, on peut mélanger les niveaux de c++ dans les so (dll) utilisés donc mélanger du c++11 avec du c++14 ne devrait pas poser de problème.

D'ailleurs Ice est à priori compilé en c++98.

h2. Compilation ISAP

h3. com.cryptopp : le premier projet ne compile plus

Ca commence mal ... Il y a plein d'erreurs et il y a aussi plein de warnings :
<pre>
In file included from filters.h:11,
                 from basecode.h:4,
                 from basecode.cpp:7:
algparam.h: In destructor ‘virtual CryptoPP::AlgorithmParametersBase::~AlgorithmParametersBase()’:
algparam.h:271:45: warning: ‘bool std::uncaught_exception()’ is deprecated: use 'std::uncaught_exceptions()' instead [-Wdeprecated-declarations]
  271 |                 if (!std::uncaught_exception())
...
asn.cpp: In function ‘size_t CryptoPP::DERLengthEncode(BufferedTransformation&, lword)’:
asn.cpp:21:24: error: reference to ‘byte’ is ambiguous
   21 |                 bt.Put(byte(length));
      |                        ^~~~
In file included from /usr/include/c++/13/bits/memory_resource.h:38,
                 from /usr/include/c++/13/string:58,
                 from stdcpp.h:15:
/usr/include/c++/13/cstddef:69:14: note: candidates are: ‘enum class std::byte’
   69 |   enum class byte : unsigned char {};
      |              ^~~~
In file included from pch.h:10,
                 from asn.cpp:3:
config.h:95:23: note:                 ‘typedef unsigned char byte’
   95 | typedef unsigned char byte;             // put in global namespace to avoid ambiguity with other byte typedefs
      |                       ^~~~
...
</pre>

Du coup j'ai pris la dernière version (8.9.0 au lieu de 5.6.2) et plus d'erreurs. A tester une fois que tout tournera.

%{background:orange}Ce n'est pas à nous, ça mériterait d'être aussi retiré de notre compilation et mis dans 02_Compilation_Linux.docx comme à faire une fois.%

h3. com.egidium.hash : RAS

h3. com.egidium.isap.sdk : quelques fix à faire

Du style :
<pre><code class="diff">
- throw iceEx;
+ throw;

...

+++ b/com.egidium.isap.sdk.icesslplugin/cpp/inc/IsapPasswordPrompt.h
@@ -9,6 +9,7 @@
 #endif

 #include <IceSSL/Plugin.h>
+#include <Ice/Communicator.h>

...
-#include <CoreIsap/AbstractEntityPlugin.h>
+#include <CoreIsap/AbstractEntityPlugIn.h>

...
-#include <PovManager/PointOfView.h>
-#include <PovManager/PovGroup.h>
+#include <PoVManager/PointOfView.h>
+#include <PoVManager/PovGroup.h>
</code></pre>

h3. com.egidium.tools.cpp

* IsapUserUtil : RAS

* CustomParsers : Gros soucis

On y a passé quelques heures et on a fini par en venir à bout avec l'aide d'Alan :
<pre><code class="diff">
Index: private/CustomParsers/evalToBool.l
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.tools.cpp/private/CustomParsers/evalToBool.l,v
retrieving revision 1.4
diff -b -w -r1.4 evalToBool.l
13a14
> #define YY_DECL extern "C" int yylex(YYSTYPE * yylval_param, void* yyscanner)
Index: private/CustomParsers/evalToBool.y
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.tools.cpp/private/CustomParsers/evalToBool.y,v
retrieving revision 1.3
diff -b -w -r1.3 evalToBool.y
12,13c12
< int yylex ( YYSTYPE * lvalp, void* scanner );
<
---
> extern "C" int yylex ( YYSTYPE * lvalp, void* scanner );
16c15
< %pure-parser
---
> %define api.pure
Index: public/bin/linux/libCustomParsers.so
</code></pre>

-A vérifier si ça passe bien sous Windows.-


h3. com.egidium.licensing : 1 erreur

<pre><code class="diff">
Index: private/EgidiumLicenseVerifier/LicenseVerifierImpl.cpp
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.licensing/private/EgidiumLicenseVerifier/LicenseVerifierImpl.cpp,v
retrieving revision 1.7
diff -b -w -r1.7 LicenseVerifierImpl.cpp
12c12
<
---
> #include <limits>
</code></pre>

h3. org.geographiclib.cpplibs : RAS

h3. com.egidium.node : RAS

h3. com.egidium.bb.events : 1 gros BUG détecté !!!

Merci à gcc (bug en double et du coup on écrase 2 octets) :
<pre><code class="diff">
Index: private/IsapServer/IsapServer.cpp
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.bb.events/private/IsapServer/IsapServer.cpp,v
retrieving revision 1.113
diff -b -w -r1.113 IsapServer.cpp
124c124
<               ::Ice::Identity l_identity = communicator()->stringToIdentity(
---
>               ::Ice::Identity l_identity = Ice::stringToIdentity(
439c439
<               DWORD l_size = UNLEN+1;
---
>               DWORD l_size = UNLEN;
448c448
<               uint32_t l_size = UNLEN+1;
---
>               uint32_t l_size = UNLEN;
458c458
<               l_username[l_size+1] = '\0';
---
>               l_username[l_size] = '\0';
</code></pre>


Quelques warning du style celui ci-dessus.

h3. com.egidium.isap.reporting : 2 erreurs

<pre><code class="diff">
--- a/IsapReportingServer/ChatProcImpl.cpp
+++ b/IsapReportingServer/ChatProcImpl.cpp
@@ -1,4 +1,4 @@
-#include "ChatprocImpl.h"
+#include "ChatProcImpl.h"

--- a/IsapReportingServer/Commons.h
+++ b/IsapReportingServer/Commons.h
@@ -285,7 +285,7 @@
-#define pi 3.14159265358979323846
+//#define pi 3.14159265358979323846
</code></pre>

Et quelques warnings :
<pre>
[  4%] Building CXX object CMakeFiles/IsapReportingServer.dir/BinaryMimeParser.cpp.o
/usr/local/isap/com.egidium.isap.reporting/private/IsapReportingServer/BinaryMimeParser.cpp: In member function ‘std::__cxx11::list<MimeDefinition> BinaryMimeParser::getAuthorizedMimeDefinitions()’:
/usr/local/isap/com.egidium.isap.reporting/private/IsapReportingServer/BinaryMimeParser.cpp:258:1: warning: no return statement in function returning non-void [-Wreturn-type]
  258 | }
      | ^
[ 44%] Building CXX object CMakeFiles/IsapReportingServer.dir/LicenseRightManager.cpp.o
/usr/local/isap/com.egidium.isap.reporting/private/IsapReportingServer/IsapReportingServer.cpp: In member function ‘virtual int IsapReportingServerManager::IsapReportingServerManager::run(int, char**, int)’:

/usr/local/isap/com.egidium.isap.reporting/private/IsapReportingServer/IsapReportingServer.cpp:1112:71: warning: ‘this’ pointer is null [-Wnonnull]
 1112 |                                         l_planificationIListener->stop();
      |                                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~
In file included from /usr/local/isap/com.egidium.isap.reporting/private/IsapReportingServer/IsapReportingServer.cpp:9:
/usr/local/isap/com.egidium.isap.reporting/private/IsapReportingServer/PlanificationIListener.h:42:14: note: in a call to non-static member function ‘void PlanificationIListener::stop()’
   42 |         void stop();
      |              ^~~~
</pre>

%{background:orange}Il y a aussi des warning dans un fichier d'ITF avec Ice 3.7% :
<pre>
slice2cpp /usr/local/isap/com.egidium.pr.counting/public/itf/itfcounting.ice
/c/DEV/EGIDIUM/com.egidium.pr.counting/public/itf/itfcounting.ice:7: warning: referencing enumerator `PEDESTRIAN' in its enumeration's enclosing scope is deprecated
/c/DEV/EGIDIUM/com.egidium.pr.counting/public/itf/itfcounting.ice:17: warning: referencing enumerator `PEDESTRIAN' in its enumeration's enclosing scope is deprecated
/c/DEV/EGIDIUM/com.egidium.pr.counting/public/itf/itfcounting.ice:19: warning: referencing enumerator `LOW' in its enumeration's enclosing scope is deprecated
</pre>

Sinon à cause de Poco c++14, il faut également compiler IsapReportingServer en c++14 sinon erreurs avec les .h de Poco non compatibles.
~~~

### 08/08/2024 14:38 — Fernand Alcatrao

- Statut : Nouveau → En cours
- Avancement : 30 % → 80 %

~~~textile
Finalement, je suis revenu sur Ice 3.6.5 avec ce qu'il y a sous CVS et ça a fonctionné. Ça tourne ici : https://vmlfr-ubuntu24.egidium.fr

A propos, il faut faire attention à ce qui est utilisé sous CVS vs installé dans le système avec les apt install en particulier sur :
* Ice
* log4cxx

Log4cxx CVS ne permettait de compiler le SDK ISAP donc utilisation du nouveau log4cxx installé dans le système et qui nécessite de remplacer :
<pre><code class="diff">
Index: system.cfg
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.bb.events/public/bin/linux/system.cfg,v
retrieving revision 1.6
diff -b -w -r1.6 system.cfg
9c9,10
< log4j.appender.AllLogs.layout=TTCCLayout
---
> log4j.appender.AllLogs.layout=org.apache.log4j.PatternLayout
> log4j.appender.AllLogs.layout.ConversionPattern=%d [%t] %p %c - %m%n
19c20,21
< log4j.appender.Errors.layout=TTCCLayout
---
> log4j.appender.Errors.layout=org.apache.log4j.PatternLayout
> log4j.appender.Errors.layout.ConversionPattern=%d [%t] %p %c - %m%n
</code></pre>

%{background:orange}Ca fonctionne déjà avec la version sous CVS donc on peut anticiper la modification.%

Reste à mettre au propre ("M:\DEVELOPPEMENTS\Documentation interne\Linux\02_Compilation_Linux.docx", Makefile, ...) et commiter ce qui est compatible.

Faudra aussi déployer les nouveaux binaires sur du debian 11 12 ubuntu 22 pour voir si bien compatible.
~~~

### 08/08/2024 14:40 — Fernand Alcatrao

~~~textile
PI la modif dans les fichiers lex et yacc compile bien sous Windows et fonctionne :
<pre>
$ eventstring 1077 Status IST
Executing: eventstring 1077 Status IST ... (dtime=1723120787.48557)
==============================================================================
std::exception: Outgoing.cpp:531: Ice::UnknownException:
unknown exception:
std::exception: Outgoing.cpp:531: Ice::UnknownException:
unknown exception:
std::exception: Constraints on attribute not satisfied.
==============================================================================
$
</pre>

Je commiterais.
~~~

### 08/08/2024 14:42 — Fernand Alcatrao

~~~textile
Il y a aussi ce warning à analyser :
%{background:orange}/usr/bin/ld: warning: libcrypto.so.1.0.0, needed by /usr/local/isap/com.egidium.shared/public/bin/linux/libIceUtil++11.so.36, may conflict with libcrypto.so.3%
~~~

### 08/08/2024 16:47 — Fernand Alcatrao

~~~textile
%{background:orange}IsapMobileServer ne se lance pas (dû à Poco)% :
<pre>
2024-08-08 16:43:42,163 [0x7a0cda200180] ERROR ISAP.Server.Mobility.UdpIncomingServer - connectFromProperties (#223) Unable to open incoming endpoint: Address family mismatch: localhost
2024-08-08 16:43:42,163 [0x7a0cda200180] ERROR ISAP.Utility.Application - CRITICAL - doMain (#204) Unhandled user exception during execution: Address family mismatch: localhost
</pre>

Code :
<pre><code class="cpp">
::Poco::Net::SocketAddress l_endpoint(Poco::Net::SocketAddress::IPv4, l_strIPAddress,l_usPort);
</code></pre>
~~~

### 08/08/2024 16:49 — Fernand Alcatrao

- Avancement : 80 % → 50 %

### 04/09/2024 15:59 — Fernand Alcatrao

~~~textile
Layout appender log4cxx modifié et commité sous CVS pour tout les fichiers de configuration des logs :
<pre>
grepalllogconf -l TTCCLayout | while read file ; do
   echo "Processing $file"
   awk -F= '
/TTCCLayout/ {
   print $1 "=org.apache.log4j.PatternLayout"
   print $1 ".ConversionPattern=%d [%t] %p %c - %m%n"
}
!/TTCCLayout/ {print $0}
' $file > $file.new
      unix2dos $file.new 2> /dev/null
      diffbw $file $file.new
      mv $file $file.bak
      mv $file.new $file
done

grepalllogconf -l appender | xargs cvs commit -m "#8080-Compilation linux sur un environnement recent (Ubuntu24) -> Layout appender log4cxx"
</pre>
~~~

### 11/03/2025 12:42 — Fernand Alcatrao

- Relation ajoutée (liée à) : #8309

### 11/03/2025 12:51 — Fernand Alcatrao

~~~textile
Sur la machine ubuntu24, on a (utilisation des packages installés) :
<pre>
vmlfr-ubuntu24:~) sudo dpkg --get-selections | grep log4cxx
liblog4cxx-dev:amd64                            install
liblog4cxx15:amd64                              install
vmlfr-ubuntu24:~) cgrep log4cxx.so
/c/DEV/EGIDIUM/com.egidium.shared/public/bin/linux/liblog4cxx.so.10.old
/usr/lib/x86_64-linux-gnu/liblog4cxx.so.15.1.0
/usr/lib/x86_64-linux-gnu/liblog4cxx.so.15
/usr/lib/x86_64-linux-gnu/liblog4cxx.so
vmlfr-ubuntu24:~)
</pre>

A priori installé comme ça :
<pre>
  435  08/08/2024-12:55:26 -> sudo apt-get install liblog4cxx10v5-dev
  436  08/08/2024-12:55:29 -> sudo apt-get install liblog4cxx10-dev
  437  08/08/2024-12:55:34 -> sudo apt-get install liblog4cxx-dev
</pre>
~~~

### 11/09/2026 13:40 — Fernand Alcatrao

- Relation ajoutée (liée à) : #9052

### 11/09/2026 17:57 — Fernand Alcatrao

- Evolution majeure : (vide) → 0

### 16/09/2026 14:59 — Fernand Alcatrao

- Avancement : 50 % → 90 %

~~~textile
Il reste 2 warnings qui n'empêchent pas de fonctionner correctement au moins sur la machine vmlfr-jenkins2.egidium.fr :
<pre>
[100%] Linking CXX executable /usr/local/isap/com.egidium.pr.incident/public/bin/linux/IncidentProcessor
/usr/bin/ld : warning : libcrypto.so.1.0.0, requis par /usr/local/isap/com.egidium.shared/public/bin/linux/libPocoNetSSL.so.64, peut être en conflit avec libcrypto.so.3

[100%] Linking CXX executable /usr/local/isap/com.egidium.isap.reporting/public/bin/linux/IsapReportingServer
/usr/bin/ld : warning : libcrypto.so.1.0.0, requis par /usr/local/isap/com.egidium.shared/public/bin/linux/libPocoNetSSL.so.64, peut être en conflit avec libcrypto.so.3
</pre>

Sera corrigé par la màj d'Openssl (#8805) et Poco (#6918).

En attente aussi MàJ d'Ansible (en particulier #9001) pour déployer sur notre machine de test debian13.

J'hésite encore à livrer les so ice dans shared/bin/linux ou d'utiliser apt get runtime ice sur machines cibles lors de l'installation avec Ansible.
~~~

### 17/09/2026 10:12 — Fernand Alcatrao

- Sujet : « Compilation linux sur un environnement récent (Ubuntu24) » → « Compilation linux sur un environnement récent (Debian 13) »

### 17/09/2026 10:46 — Fernand Alcatrao

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %

~~~textile
Commité.

Finalement j'ai choisi de ne pas livrer Ice dans shared. Cela permettra de bénéficier des màj ice 3.7 s'il y en a sur les déploiements.

Voir détail ici : #9052#note-4
~~~

### 25/09/2026 15:36 — Fernand Alcatrao

~~~textile
PI les 2 machines jenkins (linux/windows) ont été migrées sur srvfr-dijon plus performante et avec disques SSD.
vmlfr-jenkins2 (nouvelle machine) a été renommée en vmlfr-jenkins tout court et l'ancienne vmlfr-jenkins a disparue.
Les IP sont identiques, donc warning à nettoyé dans known_hosts.
~~~

### 25/09/2026 15:44 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V27.1
