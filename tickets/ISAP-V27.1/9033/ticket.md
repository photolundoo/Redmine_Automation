# #9033 — Migration Ice 3.7 : Java

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - SDK |
| Catégorie | com.egidium.isap |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8842 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 14/08/2026 17:20 |
| Mis à jour le | 23/09/2026 17:59 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9033 |

## Description

~~~textile
https://archive.zeroc.com/ice/3.7/release-notes/upgrading-your-application-from-ice-3-6#id-.UpgradingyourApplicationfromIce3.6v3.7-JavaChanges
~~~

## Relations

- Liée à #8915

## Historique

### 23/09/2026 15:32 — Fernand Alcatrao

- Statut : Nouveau → En cours
- Avancement : 0 % → 90 %
- Temps estimé : (vide) → 4.0 h

~~~textile
Pas grand chose à faire grâce aux jar ICE "compat" ;-) ...
La prochaine fois, il y aura beaucoup de boulot.

Pris en compte :
* LostPassword
* IsapReporting
* WebServices

Exemple sur LostPassword :
<pre><code class="diff">
/c/DEV/EGIDIUM/com.egidium.lostpassword/private) cvsdiff
Index: pom.xml
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.lostpassword/private/pom.xml,v
retrieving revision 1.4
diff -b -w -r1.4 pom.xml
23c23
<     <!-- https://mvnrepository.com/artifact/com.zeroc/ice -->
---
>     <!-- https://mvnrepository.com/artifact/com.zeroc/ice-compat -->
26,27c26,27
<         <artifactId>ice</artifactId>
<         <version>3.6.5</version>
---
>         <artifactId>ice-compat</artifactId>
>         <version>3.7.11</version>
29c29
<     <!-- https://mvnrepository.com/artifact/com.zeroc/icestorm -->
---
>     <!-- https://mvnrepository.com/artifact/com.zeroc/icestorm-compat -->
32,33c32,33
<         <artifactId>icestorm</artifactId>
<         <version>3.6.5</version>
---
>         <artifactId>icestorm-compat</artifactId>
>         <version>3.7.11</version>
35c35
< 	<!-- https://mvnrepository.com/artifact/com.zeroc/glacier2 -->
---
> 	<!-- https://mvnrepository.com/artifact/com.zeroc/glacier2-compat -->
38,39c38,39
< 	    <artifactId>glacier2</artifactId>
< 	    <version>3.6.5</version>
---
> 	    <artifactId>glacier2-compat</artifactId>
> 	    <version>3.7.11</version>
Index: .settings/com.zeroc.IceBuilderPlugin.prefs
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.lostpassword/private/.settings/com.zeroc.IceBuilderPlugin.prefs,v
retrieving revision 1.1
diff -b -w -r1.1 com.zeroc.IceBuilderPlugin.prefs
3a4
> extraArguments=--compat
Index: src/main/webapp/WEB-INF/web.xml
===================================================================
RCS file: /CVS_Repositories/EGIDIUM/com.egidium.lostpassword/private/src/main/webapp/WEB-INF/web.xml,v
retrieving revision 1.4
diff -b -w -r1.4 web.xml
2c2
< <web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="https://jakarta.ee/xml/ns/jakartaee" xmlns:web="http://xmlns.jcp.org/xml/ns/javaee" xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee https://jakarta.ee/xml/ns/jakartaee/web-app_5_0.xsd" id="WebApp_ID" version="5.0">
---
> <web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://xmlns.jcp.org/xml/ns/javaee" xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd" id="WebApp_ID" version="4.0">
/c/DEV/EGIDIUM/com.egidium.lostpassword/private)
</code></pre>

Le web.xml était faux depuis longtemps car pointait sur Servlets 5.0. Or tomcat 9 est Servlet 4.0.

J'attends avant de commiter de voir si je termine le travail en cours sur SSO (jamais livré sous CVS). Et profiter aussi de voir si màj à faire des packages dans les pom.xml.
~~~

### 23/09/2026 17:58 — Fernand Alcatrao

- Statut : En cours → Résolu
- Avancement : 90 % → 100 %

~~~textile
MàJ des packages faite sauf pour ceux qui produisait des erreurs avec les versions les plus récentes (TODO mis dans les pom.xml).
Commit sous CVS.
~~~

### 23/09/2026 17:59 — Fernand Alcatrao

~~~textile
Du coup SSO livré en parti mais à vérifier. J'ai l'impression que j'ai commenté du code utile mais ça date de fin 2025 ...
~~~

### 06/10/2026 16:48 — Fernand Alcatrao

- Relation ajoutée (liée à) : #8915
