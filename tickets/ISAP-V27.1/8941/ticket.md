# #8941 — [WebApp] Droits spécifique pour la vidéo + gestion du plugin en local

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Immédiat |
| Fonction | WebApp - Video |
| Catégorie | com.egidium.isap.gui.web |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Vincent Tellier |
| Avancement | 100 % |
| Créé le | 03/07/2026 10:20 |
| Mis à jour le | 23/07/2026 13:22 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Release notes | Oui |
| Lien Redmine | https://srvfr-redmine/issues/8941 |

## Description

~~~textile
Indispensable pour VGP/Buc.
Le serveur n'est pas sur le réseau vidéo.
Le poste client lui l'est.
Il faut donc installer le plugin sur celui-ci et ne pas faire faire des A/R à la vidéo par le serveur via le routeur. Pour cela on fera comme dans la WinApp avec un proxy en direct sur localhost.
Seul ces postes là auront accès donc à la vidéo, mais en plus seul les utilisateurs autorisés devront voir les vidéos. Il faut donc aussi gérer un droit spécifique à la vidéo :
* Aucun
* Flux
* Dichotomie
* Enregistrements
~~~

## Relations

- Liée à #4910
- Liée à #8968
- Liée à #8984

## Pièces jointes

- [clipboard-202607231012-gz7o6.png](pieces_jointes/clipboard-202607231012-gz7o6.png) — 299 Ko, ajoutée par Fernand Alcatrao le 23/07/2026 10:12

## Historique

### 03/07/2026 10:21 — Fernand Alcatrao

- Priorité : Normal → Immédiat

### 03/07/2026 10:46 — Pascal Vognin

- Relation ajoutée (liée à) : #4910

### 03/07/2026 10:47 — Pascal Vognin

~~~textile
Voici ce qu'on fait pour construire le proxy sans information locator et routeur

https://srvfr-redmine/issues/4910#note-11
~~~

### 09/07/2026 12:00 — Vincent Tellier

- Avancement : 0 % → 90 %

### 10/07/2026 11:58 — Vincent Tellier

- Statut : Nouveau → Résolu
- Avancement : 90 % → 100 %

~~~textile
Utilisation du plugin local a la place du distant fonctionnel, reste a tester si on passe par le routeur
~~~

### 10/07/2026 13:12 — Fernand Alcatrao

- Statut : Résolu → En cours
- Avancement : 100 % → 80 %

~~~textile
J'avais oublié à point à résoudre. Sur la WinApp le proxy est dans chaque MenuBar du poste client et donc différent.
Sur la WebApp le proxy est unique (maincourante.config.js) et donc le le nom Wellknown Object : SecurityCenterVideoPlugin-*FA*

Il faut donc trouvé un astuce pour le rendre spécifique à chaque poste client et donc le War/JS doit être en mesure de récupérer un identifiant unique du poste comme son volID.

Ainsi on mettra dans dans maincourante.config.js un truc du genre SecurityCenterVideoPlugin-*VOLID* et VOLID sera substitué par le volID récupéré par le war.
~~~

### 22/07/2026 14:34 — Fernand Alcatrao

~~~textile
Avec un serveur Smart Shield sur OVH on pourrait même avoir un accès vidéo sur le poste de la garde champêtre :
* Il faut mettre une grid/noeud en localhost sur son poste avec le plugin securitycenter.
* Configurer main courante.config.js avec le mode isLocal sur localhost.

A tester depuis chez nous quand on aura vgp.egidium.fr. Je m'y met du coup.
~~~

### 23/07/2026 10:52 — Fernand Alcatrao

- Relation ajoutée (liée à) : #8968

### 23/07/2026 10:59 — Fernand Alcatrao

- Pièce jointe ajoutée : clipboard-202607231012-gz7o6.png
- Statut : En cours → Résolu
- Avancement : 80 % → 100 %

~~~textile
Ca marche ! A partir d'une machine OVH et plugin sur grille locale sur mon PC :
!clipboard-202607231012-gz7o6.png!

h4. Config serveur :

<pre><code class="diff">
++ diff -bw /var/www/isap/vgp/maincourante.config.js /usr/local/isap/com.egidium.isap.reporting/public/conf/maincourante.config.example.js
9,13c9,13
< this.localStorage.iceMap_video_prx = "SecurityCenterVideoPlugin-Main:ws -p 10059 -h localhost" // "SecurityCenterVideoPlugin-Main"
< this.localStorage.iceMap_useLocalVideo = true
< this.localStorage.iceMap_cctv_prx = "Cctv-Main:ws -p 10059 -h localhost" // "Cctv-Main"
< this.localStorage.iceMap_useLocalCctv = true
< this.localStorage.iceMap_dataProvider_prx = "CountingDataProvider" // "CountingDataProvider"
---
> this.localStorage.iceMap_video_prx = "" // "SecurityCenterVideoPlugin-Main"
> this.localStorage.iceMap_useLocalVideo = false
> this.localStorage.iceMap_cctv_prx = "" // "Cctv-Main"
> this.localStorage.iceMap_useLocalCctv = false
> this.localStorage.iceMap_dataProvider_prx = "" // "CountingDataProvider" "FloodAlertDataProvider"
</code></pre>

h4. Config client :

<pre><code class="diff">
/c/DEV/EGIDIUM) M com.acme.sandbox/public/conf/grid/demo/IsapGrid-ClientNodes.xml
Index: com.acme.sandbox/public/conf/grid/demo/IsapGrid-ClientNodes.xml
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.acme.sandbox/public/conf/grid/demo/IsapGrid-ClientNodes.xml,v
retrieving revision 1.14
diff -b -w -r1.14 IsapGrid-ClientNodes.xml
4c4
< 		<server-instance template="SecurityCenterVideoPlugin"
---
> 		<server-instance template="SecurityCenterVideoPluginRouted"
6c6
< 			interface="${CLIENT_NODE_HOST01}"
---
> 			interface="-h localhost"
17a18
> 			router-endpoint="wss -p 443 -h isap-vgp.egidium.fr"
/c/DEV/EGIDIUM) M com.egidium.node/public/conf/MainClientNode.cfg
Index: com.egidium.node/public/conf/MainClientNode.cfg
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.node/public/conf/MainClientNode.cfg,v
retrieving revision 1.18
diff -b -w -r1.18 MainClientNode.cfg
24c24
< IceGrid.Node.PropertiesOverride='Ice.MessageSizeMax=0' 'Ice.Plugin.IceSSL.cpp=IceSSL:createIceSSL' 'Ice.Plugin.IceSSL.clr=IceSSL.dll:IceSSL.PluginFactory' 'IceSSL.DefaultDir=C:/DEV/EGIDIUM/com.egidium.grid/public/data' 'IceSSL.CertFile=C:/ProgramData/EGIDIUM Technologies/certificats/IsapLocalhostCert.pfx' 'IceSSL.Password=4dm1n/1s4pD3f4ult' 'IceSSL.VerifyPeer=2' 'IceSSL.VerifyDepthMax=4' 'IceSSL.UsePlatformCAs=1' 'IceSSL.CheckCertName=1'
---
> IceGrid.Node.PropertiesOverride='Ice.MessageSizeMax=0' 'Ice.Plugin.IceSSL.cpp=IceSSL:createIceSSL' 'Ice.Plugin.IceSSL.clr=IceSSL.dll:IceSSL.PluginFactory' 'IceSSL.DefaultDir=C:/DEV/EGIDIUM/com.egidium.grid/public/data' 'IceSSL.CertFile=C:/ProgramData/EGIDIUM Technologies/certificats/egidium.pfx' 'IceSSL.Password=4dm1n/1s4pD3f4ult' 'IceSSL.VerifyPeer=0' 'IceSSL.VerifyDepthMax=4' 'IceSSL.UsePlatformCAs=1' 'IceSSL.CheckCertName=0'
/c/DEV/EGIDIUM) M com.egidium.video/public/conf/grid/T-Server-SecurityCenterVideoPlugin.xml
Index: com.egidium.video/public/conf/grid/T-Server-SecurityCenterVideoPlugin.xml
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.video/public/conf/grid/T-Server-SecurityCenterVideoPlugin.xml,v
retrieving revision 1.34
diff -b -w -r1.34 T-Server-SecurityCenterVideoPlugin.xml
132c132
< 			<adapter name="Isap.SecurityCenterVideoPlugin.Adapter" endpoints="tcp -p ${port-number} ${interface}" id="${instance-adapter-id}.${unique-id}">
---
> 			<adapter name="Isap.SecurityCenterVideoPlugin.Adapter" endpoints="ws -p ${port-number} ${interface}" id="${instance-adapter-id}.${unique-id}">
274c274
< 				<property name="Isap.SecurityCenterVideoPlugin.Adapter.Video.Endpoints" value="tcp -p ${port-number} ${interface}" />
---
> 				<property name="Isap.SecurityCenterVideoPlugin.Adapter.Video.Endpoints" value="ws -p ${port-number} ${interface}" />
/c/DEV/EGIDIUM)
</code></pre>

Il a fallut aussi passé le HAProxy en TLS1.2 car Ice 3.6.5 (utilisé par le plugin local) ne supporte pas TLS 1.3.
~~~

### 23/07/2026 11:00 — Fernand Alcatrao

~~~textile
Je vais configurer avignon correctement et indiquer comment s'y connecter.
Ce qui permettra de remettre vgp en "config vgp" ;-)
~~~

### 23/07/2026 13:22 — Fernand Alcatrao

~~~textile
Avignon à jour pour tests :
<pre><code class="diff">
/c/DEV/EGIDIUM) M com.acme.sandbox/public/conf/grid/demo/IsapGrid-ClientNodes.xml
Index: com.acme.sandbox/public/conf/grid/demo/IsapGrid-ClientNodes.xml
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.acme.sandbox/public/conf/grid/demo/IsapGrid-ClientNodes.xml,v
retrieving revision 1.14
diff -b -w -r1.14 IsapGrid-ClientNodes.xml
4,6c4,6
<               <server-instance template="SecurityCenterVideoPlugin"
<                       activation-mode="manual"
<                       interface="${CLIENT_NODE_HOST01}"
---
>               <server-instance template="SecurityCenterVideoPluginRouted"
>                       activation-mode="always"
>                       interface="-h localhost"
17a18
>                       router-endpoint="wss -p 8444 ${ROUTER_NODE_HOST}"
/c/DEV/EGIDIUM) M com.egidium.isap.reporting/public/conf/maincourante.config.example.js
Index: com.egidium.isap.reporting/public/conf/maincourante.config.example.js
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.isap.reporting/public/conf/maincourante.config.example.js,v
retrieving revision 1.105
diff -b -w -r1.105 maincourante.config.example.js
9,12c9,16
< this.localStorage.iceMap_video_prx = "" // "SecurityCenterVideoPlugin-Main"
< this.localStorage.iceMap_useLocalVideo = false
< this.localStorage.iceMap_cctv_prx = "" // "Cctv-Main"
< this.localStorage.iceMap_useLocalCctv = false
---
> this.localStorage.iceMap_video_prx = "SecurityCenterVideoPlugin-Main:ws -p 10059 -h localhost" // "SecurityCenterVideoPlugin-Main"
> this.localStorage.iceMap_useLocalVideo = true
> this.localStorage.iceMap_cctv_prx = "Cctv-Main:ws -p 10059 -h localhost" // "Cctv-Main"
> this.localStorage.iceMap_useLocalCctv = true
/c/DEV/EGIDIUM) M com.egidium.node/public/conf/MainClientNode.cfg
Index: com.egidium.node/public/conf/MainClientNode.cfg
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.node/public/conf/MainClientNode.cfg,v
retrieving revision 1.18
diff -b -w -r1.18 MainClientNode.cfg
4c4
< Ice.Default.Locator=IsapGrid/Locator:ssl -p 4062 -h localhost
---
> Ice.Default.Locator=IsapGrid/Locator:ssl -p 4062 -h dskfr-avignon.egidium.fr
8c8
< IceSSL.CertFile=C:/ProgramData/EGIDIUM Technologies/certificats/IsapLocalhostCert.pfx
---
> IceSSL.CertFile=C:/ProgramData/EGIDIUM Technologies/certificats/egidium.pfx
13,14c13,14
< IceSSL.CheckCertName=1
< # IceSSL.TrustOnly=
---
> IceSSL.CheckCertName=0
> IceSSL.TrustOnly=CN=*.egidium.fr
20c20
< IceGrid.Node.Endpoints=ssl -p 10033 -h localhost
---
> IceGrid.Node.Endpoints=ssl -p 10033 -h dskfr-avignon.egidium.fr
24c24
< IceGrid.Node.PropertiesOverride='Ice.MessageSizeMax=0' 'Ice.Plugin.IceSSL.cpp=IceSSL:createIceSSL' 'Ice.Plugin.IceSSL.clr=IceSSL.dll:IceSSL.PluginFactory' 'IceSSL.DefaultDir=C:/DEV/EGIDIUM/com.egidium.grid/public/data' 'IceSSL.CertFile=C:/ProgramData/EGIDIUM Technologies/certificats/IsapLocalhostCert.pfx' 'IceSSL.Password=4dm1n/1s4pD3f4ult' 'IceSSL.VerifyPeer=2' 'IceSSL.VerifyDepthMax=4' 'IceSSL.UsePlatformCAs=1' 'IceSSL.CheckCertName=1'
---
> IceGrid.Node.PropertiesOverride='Ice.MessageSizeMax=0' 'Ice.Plugin.IceSSL.cpp=IceSSL:createIceSSL' 'Ice.Plugin.IceSSL.clr=IceSSL.dll:IceSSL.PluginFactory' 'IceSSL.DefaultDir=C:/DEV/EGIDIUM/com.egidium.grid/public/data' 'IceSSL.CertFile=C:/ProgramData/EGIDIUM Technologies/certificats/egidium.pfx' 'IceSSL.Password=4dm1n/1s4pD3f4ult' 'IceSSL.VerifyPeer=0' 'IceSSL.VerifyDepthMax=4' 'IceSSL.UsePlatformCAs=1' 'IceSSL.TrustOnly=CN=*.egidium.fr' 'IceSSL.CheckCertName=0'
/c/DEV/EGIDIUM) M com.egidium.video/public/conf/grid/T-Server-SecurityCenterVideoPlugin.xml
Index: com.egidium.video/public/conf/grid/T-Server-SecurityCenterVideoPlugin.xml
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.video/public/conf/grid/T-Server-SecurityCenterVideoPlugin.xml,v
retrieving revision 1.34
diff -b -w -r1.34 T-Server-SecurityCenterVideoPlugin.xml
132c132
<                       <adapter name="Isap.SecurityCenterVideoPlugin.Adapter" endpoints="tcp -p ${port-number} ${interface}" id="${instance-adapter-id}.${unique-id}">
---
>                       <adapter name="Isap.SecurityCenterVideoPlugin.Adapter" endpoints="ws -p ${port-number} ${interface}" id="${instance-adapter-id}.${unique-id}">
274c274
<                               <property name="Isap.SecurityCenterVideoPlugin.Adapter.Video.Endpoints" value="tcp -p ${port-number} ${interface}" />
---
>                               <property name="Isap.SecurityCenterVideoPlugin.Adapter.Video.Endpoints" value="ws -p ${port-number} ${interface}" />
/c/DEV/EGIDIUM)
</code></pre>

h4. Pour tester sur son poste client :

<pre><code class="diff">
/c/DEV/EGIDIUM) M com.acme.sandbox/public/conf/grid/demo/IsapGrid-ClientNodes.xml
Index: com.acme.sandbox/public/conf/grid/demo/IsapGrid-ClientNodes.xml
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.acme.sandbox/public/conf/grid/demo/IsapGrid-ClientNodes.xml,v
retrieving revision 1.14
diff -b -w -r1.14 IsapGrid-ClientNodes.xml
4c4
< 		<server-instance template="SecurityCenterVideoPlugin"
---
> 		<server-instance template="SecurityCenterVideoPluginRouted"
6c6
< 			interface="${CLIENT_NODE_HOST01}"
---
> 			interface="-h localhost"
17a18
> 			router-endpoint="wss -p 8444 -h dskfr-avignon.egidium.fr"
/c/DEV/EGIDIUM) M com.egidium.node/public/conf/MainClientNode.cfg
Index: com.egidium.node/public/conf/MainClientNode.cfg
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.node/public/conf/MainClientNode.cfg,v
retrieving revision 1.18
diff -b -w -r1.18 MainClientNode.cfg
24c24
< IceGrid.Node.PropertiesOverride='Ice.MessageSizeMax=0' 'Ice.Plugin.IceSSL.cpp=IceSSL:createIceSSL' 'Ice.Plugin.IceSSL.clr=IceSSL.dll:IceSSL.PluginFactory' 'IceSSL.DefaultDir=C:/DEV/EGIDIUM/com.egidium.grid/public/data' 'IceSSL.CertFile=C:/ProgramData/EGIDIUM Technologies/certificats/IsapLocalhostCert.pfx' 'IceSSL.Password=4dm1n/1s4pD3f4ult' 'IceSSL.VerifyPeer=2' 'IceSSL.VerifyDepthMax=4' 'IceSSL.UsePlatformCAs=1' 'IceSSL.CheckCertName=1'
---
> IceGrid.Node.PropertiesOverride='Ice.MessageSizeMax=0' 'Ice.Plugin.IceSSL.cpp=IceSSL:createIceSSL' 'Ice.Plugin.IceSSL.clr=IceSSL.dll:IceSSL.PluginFactory' 'IceSSL.DefaultDir=C:/DEV/EGIDIUM/com.egidium.grid/public/data' 'IceSSL.CertFile=C:/ProgramData/EGIDIUM Technologies/certificats/egidium.pfx' 'IceSSL.Password=4dm1n/1s4pD3f4ult' 'IceSSL.VerifyPeer=0' 'IceSSL.VerifyDepthMax=4' 'IceSSL.UsePlatformCAs=1' 'IceSSL.CheckCertName=0'
/c/DEV/EGIDIUM) M com.egidium.video/public/conf/grid/T-Server-SecurityCenterVideoPlugin.xml
Index: com.egidium.video/public/conf/grid/T-Server-SecurityCenterVideoPlugin.xml
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.video/public/conf/grid/T-Server-SecurityCenterVideoPlugin.xml,v
retrieving revision 1.34
diff -b -w -r1.34 T-Server-SecurityCenterVideoPlugin.xml
132c132
< 			<adapter name="Isap.SecurityCenterVideoPlugin.Adapter" endpoints="tcp -p ${port-number} ${interface}" id="${instance-adapter-id}.${unique-id}">
---
> 			<adapter name="Isap.SecurityCenterVideoPlugin.Adapter" endpoints="ws -p ${port-number} ${interface}" id="${instance-adapter-id}.${unique-id}">
274c274
< 				<property name="Isap.SecurityCenterVideoPlugin.Adapter.Video.Endpoints" value="tcp -p ${port-number} ${interface}" />
---
> 				<property name="Isap.SecurityCenterVideoPlugin.Adapter.Video.Endpoints" value="ws -p ${port-number} ${interface}" />
/c/DEV/EGIDIUM)
</code></pre>

J'ai testé la WebApp depuis le navigateur sur mon PC et le navigateur sur Avignon et c'est OK.

OK aussi pour WinApp sur Avignon.
~~~

### 27/07/2026 17:22 — Fernand Alcatrao

- Relation ajoutée (liée à) : #8984
