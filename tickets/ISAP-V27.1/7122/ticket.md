# #7122 — [IsapReporting] Migration vers tomcat 11

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Urgent |
| Fonction | ISAP Core - Reporting |
| Catégorie | com.egidium.tools.java |
| Version cible | ISAP-V27.1 |
| Auteur | Fernand Alcatrao |
| Assigné à | Fernand Alcatrao |
| Avancement | 100 % |
| Créé le | 01/09/2022 10:35 |
| Mis à jour le | 16/10/2026 13:43 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Release notes | Oui |
| Description release notes | Nous ne supportons plus Tomcat 9. Il faut migrer en Tomcat 11.  Par ailleurs cela implique qu'il faut aussi migrer vers Geoserver 3.0.  Nos applications Servlet (dont IsapReporting) et Geoserver 3 nécessitent désormais un serveur Web Servlet 6.0 comme Tomcat 11. |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/7122 |

## Description

~~~textile
Idem avec :
* Java SDK
* com.egidium.isap.gui.web/public/bin/consignes.war"
* com.egidium.isap.reporting/public/bin/IsapReporting.war
* com.egidium.s2icr.gui.web/public/bin/s2icr.war
* com.egidium.s2icr.new.gui.web/public/bin/s2icrNew.war
* com.egidium.sitairsoft/public/bin/sitairsoft.war
* com.egidium.tools.java/public/bin/IsapReporting.war
* com.egidium.webservice/public/bin/EgidiumWebServices.war
* Configurateur serveur ?

En lien avec #7120
~~~

## Relations

- Liée à #7120
- Liée à #7159
- Liée à #7078
- Liée à #7960
- Liée à #8366
- Liée à #8377
- Liée à #8392

## Pièces jointes

- [clipboard-202503311049-ducum.png](pieces_jointes/clipboard-202503311049-ducum.png) — 66 Ko, ajoutée par Fernand Alcatrao le 31/03/2025 10:49
- [clipboard-202504291818-1b3th.png](pieces_jointes/clipboard-202504291818-1b3th.png) — 72 Ko, ajoutée par Fernand Alcatrao le 29/04/2025 18:18
- [clipboard-202504291819-yixgz.png](pieces_jointes/clipboard-202504291819-yixgz.png) — 29 Ko, ajoutée par Fernand Alcatrao le 29/04/2025 18:19
- [clipboard-202508261353-um4gd.png](pieces_jointes/clipboard-202508261353-um4gd.png) — 91 Ko, ajoutée par Fernand Alcatrao le 26/08/2025 13:53

## Historique

### 01/09/2022 10:35 — Fernand Alcatrao

- Relation ajoutée (liée à) : #7120

### 01/09/2022 10:35 — Fernand Alcatrao

- Référence support : (vide) → 993

### 26/09/2022 14:21 — Alan Raynaud

- Version cible : ISAP-V5.5.1 → ISAP-V5.6.0

### 28/09/2022 16:34 — Fernand Alcatrao

- Avancement : 0 % → 10 %

~~~textile
h1. Préparation de réponse que j'amenderais au fur et à mesure ici

h2. Tomcat

Dans le cadre Passdef, 2 war sont déployés sous Tomcat :
* *com.egidium.tools.java/public/bin/IsapReporting.war* : nécessite un serveur web compatible *"Servlet 4.0"* comme Tomcat (voir https://tomcat.apache.org/tomcat-9.0-doc/index.html). Codé en Java avec des pages JSP (Java Servlet Pages).
* *com.egidium.isap.reporting/public/bin/IsapReporting.war* : pas de prérequis, tout serveur web comme Apache suffit. Codé sous forme de pages html incluant du JS.

La documentation a été mise à jour pour être plus claires sur ces points.

Tomcat 10 a migré vers l'architecture *"Servlet 5.0"* (voir https://tomcat.apache.org/tomcat-10.0-doc/index.html) et *"Servlet 6.0"* en cours dans la version beta 10.1.0 (voir https://tomcat.apache.org/tomcat-10.1-doc/index.html).
En particulier le nom des classes servlet passe de javax.servlet à jakarta.servlet. Le war actuel ne peut donc fonctionner sous Tomcat 10 même en mettant à jour les jar servlet.
Mais tout autre serveur web compatible *"Servlet 4.0"* fera l'affaire.
La migration va donc être un peu plus compliquée que prévu et ne pourra pas être incluse dans la version Smart Shield 5.5.1.0 en cours de validation.

Au sujet des vulnérabilités, Tomcat 9 en compte effectivement un certain nombre :
* https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=tomcat+9
* https://www.cvedetails.com/vulnerability-list/vendor_id-45/product_id-887/Apache-Tomcat.html

Mais le produit est toujours maintenu et les vulnérabilités sont régulièrement corrigées tout comme dans Tomcat 10 :
* https://tomcat.apache.org/security-9.html
* https://tomcat.apache.org/security-10.html

%{background:orange}Question : Mais comment savoir ce qu'il reste en 9.0.67 ? Alan, Mathieu une idée ?%

Tomcat 9 est l'outil utilisé en interne pour déployer ces 2 war et supporté par le configurateur. Rien n'empêche l'intégrateur d'en utiliser un autre compatible avec la norme *"Servlet 4.0"* et en y déployant les 2 war.

h2. Java

Des tests ont aussi été effectués avec *java 19* et la version actuelle de com.egidium.tools.java/public/bin/IsapReporting.war (5.5.0.0) et cela fonctionne correctement.
Par contre le raccourci IsapGridGUI doit être modifié en :
<pre>
javaw --add-exports=java.desktop/com.sun.java.swing.plaf.windows=ALL-UNNAMED -jar "C:\Program Files (x86)\EGIDIUM Technologies\com.egidium.grid\public\bin\IsapGridGUI.jar"
</pre>

h2. Python

Concernant Python, nous livrons un distribuable que nous ne mettons pas systématiquement à jour. Libre à l'intégrateur d'en utiliser un autre. Les librairies nécessaires sont décrites ici : https://support.egidium.fr/redmine/projects/common/wiki/PythonSDK.

De votre côté quel Tomcat et quel Java aviez-vous testé ?
~~~

### 28/09/2022 16:57 — Fernand Alcatrao

- Statut : Nouveau → En cours

### 29/09/2022 19:29 — Fernand Alcatrao

~~~textile
Pour IceGridGUI, j'ai trouvé 1 site (et 1 seul) donnant la solution en tapant l'erreur retourné par Java 17 : zeroc java.lang.IllegalAccessError: superclass access check failed: class "com.jgoodies.looks.windows.WindowsLookAndFeel"
https://community.axonivy.com/u/Christian_Strebel

Il faut lancer avec :
<pre>
javaw --add-exports=java.desktop/com.sun.java.swing.plaf.windows=ALL-UNNAMED -jar IsapGridGUI.jar
</pre>

Je vais essayer avec Java 19. Mais de mémoire Java 19 ne donnait même pas de message d'erreur. Ça sortait sans rien faire.
~~~

### 29/09/2022 19:31 — Fernand Alcatrao

~~~textile
Par contre l'option n'est pas disponible en Java 1.8 :
<pre>
/c/DEV/EGIDIUM/com.egidium.grid/public/bin) javaw --add-exports=java.desktop/com.sun.java.swing.plaf.windows=ALL-UNNAMED -jar IsapGridGUI.jar
Unrecognized option: --add-exports=java.desktop/com.sun.java.swing.plaf.windows=ALL-UNNAMED
/c/DEV/EGIDIUM/com.egidium.grid/public/bin)
</pre>

Faudra configurer le raccourci en fonction du Java présent sur la machine.
~~~

### 29/09/2022 19:38 — Fernand Alcatrao

- Avancement : 10 % → 50 %

~~~textile
Top ! Ca marche aussi en Java 19. Le @--add-exports@ doit être placé avant le @-jar file.jar@

On va pouvoir répondre à GTD.
~~~

### 30/09/2022 10:43 — Fernand Alcatrao

~~~textile
Laurent préfère quelque chose de plus simple :

Dans le cadre Passdef, 2 war (Web Application Archive) sont déployés sous Tomcat : 
# Les outils Tomcat et Java ne pas parti des livrables Egidium. Bien qu’Egidium ne soit pas tenu d'alerter sur d’éventuelles failles de sécurité en dehors de ses livrables, nous faisons nos meilleurs efforts pour alerter sur d’éventuelles failles sur les composants externes.
# Les prérequis pour l'utilisation des 2 war, sont d'utiliser un serveur web compatible "Serlvet 4.0" comme Tomcat 9.
# Notre recommandation est d'être à jour pour Java et le serveur web que vous choisissez. Tomcat 9 par exemple, est régulièrement mis à jour.
# Nous avons testé avec Java 19 et nous n'avons pas rencontré de problème.

Afin d’optimiser encore la sécurité, l’architecture suivante peut être retenue pour les deux composants web :
# Le module IsapReporting nécessite un serveur web compatible "Serlvet 4.0" pour permettre la configuration depuis le serveur (ports non ouverts vers l’extérieur)
# Le nouveau module web (main courante, statistiques ...) est du pur HTML/JS et peut  être déployée sur n’importe quel serveur web.

Concernant python, nous livrons effectivement un interpréteur python sur le CD pour faciliter son utilisation mais il peut être remplacé facilement par l'intégrateur comme indiquer dans le wiki : https://support.egidium.fr/redmine/projects/common/wiki/PythonSDK

PI, l'utilisation de Java 19 nécessite de changer la façon de lancer IsapGridGUi:
<pre>
javaw --add-exports=java.desktop/com.sun.java.swing.plaf.windows=ALL-UNNAMED -jar IsapGridGUI.jar
</pre>
~~~

### 30/09/2022 10:47 — Fernand Alcatrao

~~~textile
Je mets ici aussi une proposition pour le case externe https://support.egidium.fr/redmine/issues/956 :

Nous sommes abonné au flux RSS de l'ANSSI : https://www.cert.ssi.gouv.fr/alerte/feed
La liste des failles importante peut-être consulté ici : https://www.cert.ssi.gouv.fr

Nous utilisons également le site CVE qui regroupe l'ensemble des failles de sécurité des librairies utilisées : https://cve.mitre.org
~~~

### 30/09/2022 13:01 — Fernand Alcatrao

- Relation ajoutée (liée à) : #7159

### 30/09/2022 13:02 — Fernand Alcatrao

~~~textile
J'ai mis à jour 00-Prerequis.docx et 01_Installation_AppliWeb.doc
~~~

### 05/10/2022 18:21 — Fernand Alcatrao

- Relation ajoutée (liée à) : #7078

### 07/10/2022 17:43 — Fernand Alcatrao

- Origine : Interne → Client

### 13/01/2023 16:29 — Alan Raynaud

- Projet 1 à livrer : Produit → PASSDEF

### 13/01/2023 16:39 — Alan Raynaud

- Version cible : ISAP-V5.6.0 → Candidate for next major release

### 14/03/2025 12:46 — Fernand Alcatrao

- Origine : Client → Interne
- Projet 1 à livrer : PASSDEF → Produit
- Référence support : 993 → (vide)

~~~textile
Le case externe n'avait rien à voir finalement. Il a été fermé mais ce case interne reste d'actualité
~~~

### 31/03/2025 10:47 — Fernand Alcatrao

- Relation ajoutée (liée à) : #7960

### 31/03/2025 10:55 — Fernand Alcatrao

- Pièce jointe ajoutée : clipboard-202503311049-ducum.png
- Avancement : 50 % → 60 %
- Temps estimé : 16.0 h → 40.0 h

~~~textile
J'ai repris les travaux fait il y a plus 2 ans et j'y suis presque :
* Passage en tomcat 11
* Projet plus moderne en maven (permet de récupérer automatiquement les paquets de dépendances).
* Tous les jars ont été mis à jour vers leur dernières versions dans le projets.
* Reste un warning (à voir si bloquant lors de l’exécution) :
!clipboard-202503311049-ducum.png!

Maven permet aussi de récupérer les dépendances JS sous forme de Webjars mais j'arrive pas à le faire fonctionner.
D'ailleurs est-ce vraiment utile ? Car il pourrait y avoir un gros impact sur le code d'IsapReporting : par exemple on utilise 2 jquery (1.9.1 et 2.1.4), pourquoi ? Sans doute pour ne pas revenir sur le code et sans doute jamais mis à jour ?

Faudra aussi refaire :
* com.egidium.webservice/public/bin/EgidiumWebServices.war
* ./com.egidium.lostpassword/public/bin/LostPassword.war

Les autres projets sont obsolètes.
~~~

### 03/04/2025 17:46 — Alan Raynaud

- Avancement : 60 % → 70 %

### 03/04/2025 17:46 — Alan Raynaud

- Avancement : 70 % → 60 %

~~~textile
J'avais modifié le mauvais case
~~~

### 07/04/2025 11:05 — Fernand Alcatrao

- Relation ajoutée (liée à) : #8366

### 07/04/2025 11:17 — Fernand Alcatrao

- Avancement : 60 % → 90 %

~~~textile
Les 3 projets ont été migrés :
* com.egidium.tools.java/public/bin/IsapReporting.war
* com.egidium.webservice/public/bin/EgidiumWebServices.war
* com.egidium.lostpassword/public/bin/LostPassword.war

Reste à tester un peu plus et commiter.

Tous le monde devra migrer son tomcat :
* Tout effacer dans C:\Program Files\Java\apache-tomcat sauf :
** webapps\ROOT\maincourante.config.js pour ne pas perdre le lien symbolique qu'il faut créer en mode admin.
* Copier le contenu de ce que je mettrais dans "T:\apache-tomcat-11.0.5-do-mklink.zip"
~~~

### 07/04/2025 11:19 — Fernand Alcatrao

- Version cible : Candidate for next major release → ISAP-V25.1

### 09/04/2025 18:34 — Fernand Alcatrao

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %

~~~textile
Reste à faire dans : #8377
~~~

### 09/04/2025 18:34 — Fernand Alcatrao

- Relation ajoutée (liée à) : #8377

### 17/04/2025 14:06 — Fernand Alcatrao

- Relation ajoutée (liée à) : #8392

### 22/04/2025 10:05 — Fernand Alcatrao

- Relation supprimée (liée à) : #8392

### 22/04/2025 10:06 — Fernand Alcatrao

- Relation ajoutée (bloquée par) : #8392

### 22/04/2025 10:06 — Fernand Alcatrao

- Statut : Résolu → Bloqué
- Avancement : 100 % → 80 %

### 22/04/2025 10:06 — Fernand Alcatrao

- Version cible : ISAP-V25.1 → Candidate for next major release
- Début : 02/09/2022 → (vide)

### 29/04/2025 18:19 — Fernand Alcatrao

- Pièce jointe ajoutée : clipboard-202504291818-1b3th.png
- Pièce jointe ajoutée : clipboard-202504291819-yixgz.png

~~~textile
PI voici comment générer le war :
!clipboard-202504291818-1b3th.png!

!clipboard-202504291819-yixgz.png!
~~~

### 26/08/2025 13:54 — Fernand Alcatrao

- Pièce jointe ajoutée : clipboard-202508261353-um4gd.png

~~~textile
Et pour lancer en mode debug (stop IsapReporting dans la grille avant) :
!clipboard-202508261353-um4gd.png!

S'il n'y a pas de serveur, Eclipse vous proposera d'en créer un.
~~~

### 16/10/2026 13:38 — Fernand Alcatrao

- Relation supprimée (bloquée par) : #8392

### 16/10/2026 13:39 — Fernand Alcatrao

- Relation ajoutée (liée à) : #8392

### 16/10/2026 13:43 — Fernand Alcatrao

- Sujet : « [IsapReporting] Support d'un java et tomcat plus récent » → « [IsapReporting] Migration vers tomcat 11 »
- Statut : Bloqué → Résolu
- Version cible : Candidate for next major release → ISAP-V27.1
- Avancement : 80 % → 100 %
- Description release notes : (vide) → Nous ne supportons plus Tomcat 9. Il faut migrer en Tomcat 11.
Par ailleurs cela implique qu'il faut aussi migrer vers Geoserver 3.0.
Nos applications Servlet (dont IsapReporting) et Geoserver 3 nécessitent désormais un serveur Web Servlet 6.0 comme Tomcat 11.
- Evolution majeure : (vide) → 0

~~~textile
Désormais Tomcat 3.0.1 est sorti et compatible avec Tomcat 11
~~~
