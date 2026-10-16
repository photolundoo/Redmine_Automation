# #8915 — Mettre à jour les packages maven

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Core - Sécurité IT |
| Catégorie | com.egidium.cyberveille |
| Version cible | ISAP-V27.1 |
| Auteur | Mathieu Fournet-Carcopino |
| Assigné à | Fernand Alcatrao |
| Avancement | 100 % |
| Créé le | 08/06/2026 16:02 |
| Mis à jour le | 06/10/2026 16:53 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/8915 |

## Description

~~~textile
Suite à l'analyse de la CyberVeille, il faudrait mettre à jour les packages maven suivants :
commons_fileuploads = 1.4 (2 vulns) -> 1.6 (0 vulns) 
commons_io = 2.11.0 (1 vulns) -> 2.14.0 (? vulns)  
jakarta_mail = 2.0.1 (1 vulns) -> 2.0.2 (0 vulns) 
commons_lang = 3.12.0 (1 vulns) -> 3.18 (0 vulns)

Cela peut être réalisé en modifiant les fichiers pom.xml ou build.gradle
~~~

## Relations

- Liée à #9033

## Historique

### 06/10/2026 16:48 — Fernand Alcatrao

- Relation ajoutée (liée à) : #9033

### 06/10/2026 16:52 — Fernand Alcatrao

- Statut : Nouveau → Résolu
- Version cible : Candidate for next major release → ISAP-V27.1
- Temps estimé : 5.0 h → 1.0 h
- Evolution majeure : (vide) → 0

~~~textile
Fait durant #9033 :
<pre>
/c/DEV/EGIDIUM) grep -i -A2 -e '<artifact.*commons-fileupload' -e '<artifact.*commons.lang' -e '<artifact.*jakarta.mail'  ./com.egidium.lostpassword/private/pom.xml ./com.egidium.tools.java/private/pom.xml ./com.egidium.webservice/private/pom.xml
./com.egidium.lostpassword/private/pom.xml:	    <artifactId>jakarta.mail</artifactId>
./com.egidium.lostpassword/private/pom.xml-	    <version>2.0.2</version>
./com.egidium.lostpassword/private/pom.xml-	    <exclusions>
--
./com.egidium.tools.java/private/pom.xml:        <artifactId>commons-fileupload</artifactId>
./com.egidium.tools.java/private/pom.xml-        <version>1.6.0</version>
./com.egidium.tools.java/private/pom.xml-    </dependency>
--
./com.egidium.tools.java/private/pom.xml:        <artifactId>commons-lang3</artifactId>
./com.egidium.tools.java/private/pom.xml-        <version>3.20.0</version>
./com.egidium.tools.java/private/pom.xml-    </dependency>
/c/DEV/EGIDIUM)
</pre>

Par contre plus de référence à commons_io.
~~~

### 06/10/2026 16:53 — Fernand Alcatrao

- Avancement : 0 % → 100 %
