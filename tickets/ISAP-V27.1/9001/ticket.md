# #9001 — [Ansible] Anomalies constatés dont templates non à jours

| Champ | Valeur |
|---|---|
| Tracker | Anomalie |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Core - Configuration |
| Catégorie | com.egidium.installer |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Mathieu Fournet-Carcopino |
| Avancement | 100 % |
| Créé le | 10/08/2026 11:48 |
| Mis à jour le | 07/10/2026 13:34 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Version source | ISAP-V25.1 |
| Lien Redmine | https://srvfr-redmine/issues/9001 |

## Description

~~~textile
En vrac ci-dessous les anomalies constatées sur déploiement machines vgp et letouquet.

Le plus important c'est les "templates" du style "maincourante.config.example.js" qui ont évolués et non maintenus dans Ansible.
Gros impact sur maincourante.config.js qui devra être revu sur toutes les machines, par exemple :
<pre><code class="diff">
< this.localStorage.iceMap_addressManagerFieldLinked = ['CustomReport6'] // ['CustomReport1', 'CustomReport2', 'CustomReport3', 'CustomReport4', 'CustomReport5', 'CustomReport6', 'CustomReport7', 'CustomReport8', 'CustomReport9', 'CustomReport10']
---
> this.localStorage.iceMap_addressManagerFieldLinked = JSON.stringify(['CustomReport6']) // JSON.stringify(['type', 'entityID', 'status', 'description', 'handledBy', 'notifiedBy'])
</code></pre>

Du coup, est-ce une bonne idée de garder ces templates ???

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : mercredi 29 juillet 2026 14:22
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : RE: Install Ansible

Et ça c’est quoi ?
<pre>
"./com.egidium.logical/public/Ansible/install_and_update/check_maincourante.py"
</pre>

C’est « check » mais ça écrase :
<pre>
    with open("/var/www/isap/vgp/maincourante.config.js", "w") as nfile:
</pre>

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : mercredi 29 juillet 2026 13:00
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : RE: Install Ansible

Pas la peine de changer ça :
<pre><code class="diff">
23c22
<                               tls-cert-file-path="${EGIDIUM_DATA}/certificats/egidium.pfx"
---
>                               tls-cert-file-path="/var/lib/isap/certificats/egidium.pfx"
</code></pre>

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : jeudi 23 juillet 2026 17:56
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : RE: Install Ansible

<pre>
~ -> debian
</pre>

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : jeudi 23 juillet 2026 17:56
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : RE: Install Ansible

Ajoutez ça aussi après l’installation d’emacs :
<pre>
sudo DEBIAN_FRONTEND=noninteractive apt-get install emacs-nox -y > /dev/null
cat > ~/.emacs <<!
(global-set-key (kbd "<f9>")   'compile)
(global-set-key (kbd "<f4>")   'next-error)
(global-set-key (kbd "S-<f4>") 'previous-error)
(setq create-lockfiles nil)
!
</pre>

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : jeudi 23 juillet 2026 17:52
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : RE: Install Ansible

A ajouter dans ansible :
<pre>
sudo DEBIAN_FRONTEND=noninteractive apt-get install python3-utm -y > /dev/null
</pre>

Pour les templates, il y aura un gros travail pour vérifier les machines précédentes.
Faudra me donner la liste des « templates ».

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : jeudi 23 juillet 2026 16:35
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : RE: Install Ansible

En fait tes templates ne sont pas maintenu, ce qui est très problématique, surtout sur des machines en mode « dev /beta » ou maincourante.config.example.js bouge souvent.
Du coup pas bonne idée les templates.

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : jeudi 23 juillet 2026 10:20
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : RE: Install Ansible

Et pourquoi ces différences ?
<pre><code class="diff">
diffbw /var/www/isap/vgp/maincourante.config.js /usr/local/isap/com.egidium.isap.reporting/public/conf/maincourante.config.example.js
…
18c18
< this.localStorage.iceMap_itfgeocoder_prx = "Geocoder"
---
> this.localStorage.iceMap_itfgeocoder_prx = "GeocoderWeb"
28c28
< this.localStorage.iceMap_enableIncidentWithoutPositionOnCreation = false
---
> this.localStorage.iceMap_enableIncidentWithoutPositionOnCreation = true
44c44
< this.localStorage.iceMap_satellitePublicUrl = 'https://igngp.geoapi.fr/tile.php/orthos/{z}/{x}/{y}.png'
---
> this.localStorage.iceMap_satellitePublicUrl = 'https://data.geopf.fr/wmts'
76,78c76,78
< this.localStorage.iceMap_expertLink = "https://vgp.egidium.fr:8443/IsapReporting"
< this.localStorage.iceMap_resetPWDLink = "https://vgp.egidium.fr"
< this.localStorage.iceMap_tableColumnDefaultFocus = 'description'
---
> this.localStorage.iceMap_expertLink = "https://localhost/IsapReporting"
> this.localStorage.iceMap_resetPWDLink = "https://localhost"
> this.localStorage.iceMap_tableColumnDefaultFocus = 'Description'
88c88
< this.localStorage.iceMap_consigneDataProvider = [] // ex: ['source1', 'source2']
---
> this.localStorage.iceMap_consigneDataProvider = [] // ex: ["FloodReport:7", "FloodReport:9"]
95c95
< this.localStorage.iceMap_showCredits = true
---
> this.localStorage.iceMap_showCredits = false

…
</code></pre>

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : jeudi 23 juillet 2026 10:14
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : RE: Install Ansible

Pas bon :
<pre>
vgp:~/tmp/tmp) ll "/usr/local/isap/com.egidium.til/public/bin/*.dll"
lrwxrwxrwx 1 isap isap 58 Jul 22 16:03 '/usr/local/isap/com.egidium.til/public/bin/*.dll' -> '/usr/local/isap//com.egidium.shared/public/bin/linux/*.dll'
vgp:~/tmp/tmp) ll "/usr/local/isap/com.egidium.video/public/bin/MetaMat/*.dll"
lrwxrwxrwx 1 isap isap 58 Jul 22 16:03 '/usr/local/isap/com.egidium.video/public/bin/MetaMat/*.dll' -> '/usr/local/isap//com.egidium.shared/public/bin/linux/*.dll'
vgp:~/tmp/tmp)
</pre>

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : mercredi 22 juillet 2026 15:51
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : RE: Install Ansible

Je me suis méfiez et j’ai bien ça sinon ça échouait encore …
<pre>
-rw-r--r-- 1 isap adm 6019 Jul 22 15:12 /var/lib/isap/certificats/egidium.pfx
-rw------- 1 isap adm 6019 Jul 22 15:12 /var/lib/isap/certificats/egidium.pfx
-rw------- 1 isap adm 6019 Jul 22 15:12 /var/lib/isap/certificats/egidium.pfx
-rw------- 1 isap adm 6019 Jul 22 15:12 /var/lib/isap/certificats/egidium.pfx
-rw------- 1 isap adm 6019 Jul 22 15:12 /var/lib/isap/certificats/egidium.pfx
-rw------- 1 isap adm 6019 Jul 22 15:12 /var/lib/isap/certificats/egidium.pfx
^C
vgp:/usr/local/isap) sudo chmod 644 /var/lib/isap/certificats/egidium.pfx
vgp:/usr/local/isap) while : ; do ll /var/lib/isap/certificats/egidium.pfx ; sleep 1 ; done
-rw-r--r-- 1 isap adm 6019 Jul 22 15:12 /var/lib/isap/certificats/egidium.pfx
-rw-r--r-- 1 isap adm 6019 Jul 22 15:12 /var/lib/isap/certificats/egidium.pfx
-rw-r--r-- 1 isap adm 6019 Jul 22 15:12 /var/lib/isap/certificats/egidium.pfx
</pre>

PI, ça a passé 10 bonnes minutes à changer les droits dans /var/www/isap/vgp … un script sh aurait été immédiat

Ca a aussi replanté à cause de la licence :
<pre>
./tmp/IsapLicense-Linux-Priv.lic
</pre>

Il faudrait par précaution faire un dos2unix avant de l’utiliser.

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : mercredi 22 juillet 2026 15:32
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : RE: Install Ansible

Pour la « reprise sur erreur », j’ai fait comme ça :
<pre>
vgp:/usr/local/isap) rm INSTALLED_26.1.00_ON
vgp:/usr/local/isap)
</pre>

C’est bien ça ?

__________________________________________________________
De : Fernand Alcatrao 
Envoyé : mercredi 22 juillet 2026 15:30
À : Mathieu Fournet Carcopino <mathieu.fournet-carcopino@egidium-technologies.com>
Objet : Install Ansible

Bonjour Mathieu,

J’installe une nouvelle machine. J’ai dû faire ça :
<pre>
sudo chmod 644 /var/lib/isap/certificats/egidium.pfx
</pre>

Il faudrait aussi ajouter le fichier de licence dans les paramètres pour penser à le MàJ …

Pour le nom du CD, mettre le chemin relatif comme pour le fichier licence. Comme ça on saura où c’est plutôt que d’avoir à chercher.
~~~

## Relations

- Dupliquée par #8993

## Historique

### 10/08/2026 11:52 — Fernand Alcatrao

- Relation ajoutée (dupliquée par) : #8993

### 10/08/2026 18:38 — Fernand Alcatrao

~~~textile
Faudra aussi en profiter pour ajouter ce paquet :
<pre>
sudo DEBIAN_FRONTEND=noninteractive apt-get install python3-socketio-client -y  > /dev/null
</pre>

Alan en a eu besoin pour instavox sur machine letouquet.
~~~

### 22/09/2026 12:20 — Mathieu Fournet-Carcopino

~~~textile
Les droits du certificat sont corrects : 
<pre>
vmlfr-debian13:~) ll /var/lib/isap/certificats/egidium.pfx
-rw-r--r-- 1 isap adm 8355 22 sept. 11:02 /var/lib/isap/certificats/egidium.pfx
</pre>__________________________________________________
Les droits dans /var/www/isap/[MACHINE] sont maintenant fait via des commandes linux et donc sont plus rapide
__________________________________________________
Les liens symbolique des dll sont corrigés : 
<pre>
vmlfr-debian13:~) ll "/usr/local/isap/com.egidium.til/public/bin/"
total 1676
drwxrwxr-x 2 isap isap   4096 22 sept. 10:55 .
drwxrwxr-x 5 isap isap   4096 22 sept. 10:55 ..
lrwxrwxrwx 1 isap isap     70 22 sept. 10:55 AccessControlSDKNet.dll -> /usr/local/isap//com.egidium.shared/public/bin/AccessControlSDKNet.dll
lrwxrwxrwx 1 isap isap     63 22 sept. 10:55 ConfigParser.dll -> /usr/local/isap//com.egidium.shared/public/bin/ConfigParser.dll
lrwxrwxrwx 1 isap isap     59 22 sept. 10:55 CoreIsap.dll -> /usr/local/isap//com.egidium.shared/public/bin/CoreIsap.dll
lrwxrwxrwx 1 isap isap     75 22 sept. 10:55 EgidiumLoggingUtilityNET.dll -> /usr/local/isap//com.egidium.shared/public/bin/EgidiumLoggingUtilityNET.dll
lrwxrwxrwx 1 isap isap     75 22 sept. 10:55 EgidiumNetworkUtilityNET.dll -> /usr/local/isap//com.egidium.shared/public/bin/EgidiumNetworkUtilityNET.dll
lrwxrwxrwx 1 isap isap     70 22 sept. 10:55 EgidiumUtilitiesNET.dll -> /usr/local/isap//com.egidium.shared/public/bin/EgidiumUtilitiesNET.dll
lrwxrwxrwx 1 isap isap     59 22 sept. 10:55 Glacier2.dll -> /usr/local/isap//com.egidium.shared/public/bin/Glacier2.dll
lrwxrwxrwx 1 isap isap     57 22 sept. 10:55 IceBox.dll -> /usr/local/isap//com.egidium.shared/public/bin/IceBox.dll
lrwxrwxrwx 1 isap isap     63 22 sept. 10:55 IceDiscovery.dll -> /usr/local/isap//com.egidium.shared/public/bin/IceDiscovery.dll
-rwxrwxr-x 1 isap isap 802304 21 mars   2025 Ice.dll
[...]
lrwxrwxrwx 1 isap isap     60 22 sept. 10:55 SnowFlake.dll -> /usr/local/isap//com.egidium.shared/public/bin/SnowFlake.dll
lrwxrwxrwx 1 isap isap     62 22 sept. 10:55 VideoSource.dll -> /usr/local/isap//com.egidium.shared/public/bin/VideoSource.dll
lrwxrwxrwx 1 isap isap     61 22 sept. 10:55 XMLManager.dll -> /usr/local/isap//com.egidium.shared/public/bin/XMLManager.dll
</pre>
<pre>
vmlfr-debian13:~) ll "/usr/local/isap/com.egidium.video/public/bin/MetaMat/"
total 19968
drwxrwxr-x 3 isap isap     4096 22 sept. 10:55 .
drwxrwxr-x 3 isap isap     4096 22 sept. 10:55 ..
lrwxrwxrwx 1 isap isap       70 22 sept. 10:55 AccessControlSDKNet.dll -> /usr/local/isap//com.egidium.shared/public/bin/AccessControlSDKNet.dll
drwxrwxr-x 5 isap isap     4096 22 mars   2025 cards
-rw-rw-r-- 1 isap isap      800  1 sept.  2021 config.cfg
lrwxrwxrwx 1 isap isap       63 22 sept. 10:55 ConfigParser.dll -> /usr/local/isap//com.egidium.shared/public/bin/ConfigParser.dll
-rwxrwxr-x 1 isap isap   498176  5 sept.  2024 CoreIsap.dll
-rwxrwxr-x 1 isap isap     7168  5 sept.  2024 EgidiumLoggingUtilityNET.dll
-rwxrwxr-x 1 isap isap    45056 31 janv.  2025 EgidiumNetworkUtilityNET.dll
-rwxrwxr-x 1 isap isap    13824  5 sept.  2024 EgidiumUtilitiesNET.dll
[...]
-rw-rw-r-- 1 isap isap     2220 27 sept.  2016 policy.xml
lrwxrwxrwx 1 isap isap       58 22 sept. 10:55 ProjNet.dll -> /usr/local/isap//com.egidium.shared/public/bin/ProjNet.dll
lrwxrwxrwx 1 isap isap       70 22 sept. 10:55 SharedMemoryManager.dll -> /usr/local/isap//com.egidium.shared/public/bin/SharedMemoryManager.dll
lrwxrwxrwx 1 isap isap       60 22 sept. 10:55 SnowFlake.dll -> /usr/local/isap//com.egidium.shared/public/bin/SnowFlake.dll
-rwxrwxr-x 1 isap isap  7444664  6 févr.  2025 VideoGrabberNET.dll
lrwxrwxrwx 1 isap isap       62 22 sept. 10:55 VideoSource.dll -> /usr/local/isap//com.egidium.shared/public/bin/VideoSource.dll
lrwxrwxrwx 1 isap isap       61 22 sept. 10:55 XMLManager.dll -> /usr/local/isap//com.egidium.shared/public/bin/XMLManager.dll
</pre>__________________________________________________
Les différences pour maincourante.config.js ne sont que les modifications essentielles à savoir : 
<pre>
vmlfr-debian13:~) diffbw /var/www/isap/vmlfr-debian13/maincourante.config.js /usr/local/isap/com.egidium.isap.reporting/public/conf/maincourante.config.example.js
++ diff -bw /var/www/isap/vmlfr-debian13/maincourante.config.js /usr/local/isap/com.egidium.isap.reporting/public/conf/maincourante.config.example.js
12c12
< this.localStorage.iceMap_locator = "EgidiumRouter/router:wss -p 443 -h isap-vmlfr-debian13.egidium.fr"
---
> this.localStorage.iceMap_locator = "EgidiumRouter/router:wss -p 8444 -h localhost"
72,73c72,73
< this.localStorage.iceMap_expertLink = "https://vmlfr-debian13.egidium.fr:8443/IsapReporting"
< this.localStorage.iceMap_resetPWDLink = "https://vmlfr-debian13.egidium.fr"
---
> this.localStorage.iceMap_expertLink = "https://localhost/IsapReporting"
> this.localStorage.iceMap_resetPWDLink = "https://localhost"
</pre>__________________________________________________
Les templates on étés remplacés par des regex seulement sur les éléments à modifier. Exemple: 
<pre>
      - name: Configuration avancée de maincourante.config.js avec regex
        block:

        - name: Appliquer les remplacements regex à maincourante.config.js
          block:

            - name: Modifier la ligne pour iceMap_locator
              replace:
                path: "{{ isap_reporting_war_dest }}/maincourante.config.js"
                regexp: '^this\.localStorage\.iceMap_locator.*$'
                replace: 'this.localStorage.iceMap_locator = "EgidiumRouter/router:wss -p {{ install_haproxy | ternary(443, routeur_port) }} -h {{ isap_server }}.egidium.fr"'

            - name: Modifier la ligne pour iceMap_expertLink
              replace:
                path: "{{ isap_reporting_war_dest }}/maincourante.config.js"
                regexp: '^this\.localStorage\.iceMap_expertLink.*$'
                replace: 'this.localStorage.iceMap_expertLink = "https://{{ isap_server_short }}.egidium.fr:8443/IsapReporting"'
              
            - name: Modifier la ligne pour iceMap_resetPWDLink
              replace:
                path: "{{ isap_reporting_war_dest }}/maincourante.config.js"
                regexp: '^this\.localStorage\.iceMap_resetPWDLink.*$'
                replace: 'this.localStorage.iceMap_resetPWDLink = "https://{{ isap_server_short }}.egidium.fr"'
</pre>
Les packages python ont été ajouté à l'installation : 
<pre>
python_dependencies:
  - python3-flask
[...]
  - python3-socketio-client
  - python3-utm
[...]
</pre>__________________________________________________
La configuration .emacs a été ajouté : 
<pre>
vmlfr-debian13:~) cat .emacs
(global-set-key (kbd "<f9>")   'compile)
(global-set-key (kbd "<f4>")   'next-error)
(global-set-key (kbd "S-<f4>") 'previous-error)
(setq create-lockfiles nil)

</pre>__________________________________________________

<pre>
vmlfr-debian13:~) cat /usr/local/isap/com.acme.sandbox/public/conf/grid/linux/IsapGrid-Application.xml | grep  tls-cert-file-path
                                tls-cert-file-path="${EGIDIUM_DATA}/certificats/egidium.pfx"
                                tls-cert-file-path="${EGIDIUM_DATA}/certificats/egidium.pfx"

</pre>__________________________________________________
Le check_maincourante a été retiré, il me reste à vérifier que l'ajout/modification de clef dans le fichier maincourante.config.js fonctionne.
~~~

### 22/09/2026 12:21 — Mathieu Fournet-Carcopino

- Avancement : 0 % → 60 %

### 22/09/2026 14:09 — Fernand Alcatrao

~~~textile
Faudra mettre à jour les inventories. En particulier stats_webapp pas à jour :
<pre>
./inventory/ocpr.yaml:      stats_webapp: 0
./inventory/sport.yaml:      stats_webapp: 0
./inventory/viparis.yaml:      stats_webapp: 0
</pre>

et :
<pre>
./inventory/ALL.yaml:      stats_webapp: 0
</pre>

Le ALL semble dupliquer. On ne peut pas faire d'include ?
~~~

### 22/09/2026 14:14 — Mathieu Fournet-Carcopino

~~~textile
Voir le ticket #8934 pour ça
~~~

### 25/09/2026 15:45 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 25/09/2026 16:51 — Alan Raynaud

- Version cible : Candidate for next major release → ISAP-V27.1

### 07/10/2026 13:34 — Mathieu Fournet-Carcopino

- Avancement : 60 % → 100 %

### 07/10/2026 13:34 — Mathieu Fournet-Carcopino

- Statut : En cours → Résolu
