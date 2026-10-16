# #8816 — Plugin CSR SIA (Central Station Receiver) - Plan de validation officiel du standard DC-09

| Champ | Valeur |
|---|---|
| Tracker | Documentation |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | ISAP Plugins - Détection Intrusion |
| Catégorie | com.egidium.sia |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8812 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 12/03/2026 18:08 |
| Mis à jour le | 08/04/2026 16:45 |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Lien Redmine | https://srvfr-redmine/issues/8816 |

## Description

~~~textile
L'annexe C prévoit un plan de validation officiel.

Le but de ce case est de générer un ensemble de test qui permettent de valider que le plugin est bien conforme.
~~~

## Historique

### 19/03/2026 17:03 — Alan Raynaud

- Début : (vide) → 23/03/2026

### 25/03/2026 15:50 — Alan Raynaud

- Tracker : Configuration → Documentation
- Sujet : « Plugin CSR SIA (Central Station Receiver) - Validation » → « Plugin CSR SIA (Central Station Receiver) - Plan de validation officiel du standard »
- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)
- Catégorie : (vide) → com.egidium.sia
- Champ personnalisé 1 : Interne → (vide)
- Champ personnalisé 2 : RD → (vide)
- Fonction : (vide) → ISAP Plugins - Détection Intrusion

~~~textile
Test de la partie DC-09

Procédure de test extraite du standard DC-09, annexe C.2

Le "PE simulator" à utiliser est : "C:\DEV\EGIDIUM\com.egidium.sia\public\tools\SIA_Simulator.bat"

La configuration à utiliser les ACME, le plugin "Plugin SIA CSR" doit être présent et lancé dans la grille, avec sa configuration par défaut.


|_.Element de validation|_.Description issue de la spec|_.Comment valider chez nous|Etat actuel|
|/2.C.2.3.1 Marking|confirm that the equipment is marked with only one of the following: "SIA IP Reporting (UDP-2006)", "SIA IP Reporting (TCP-2006)" or "SIA IP Reporting (UDP/TCP-2006)"|Vérifier dans le documentation du plugin (https://support.egidium.fr/projects/common/wiki/CSRPlugin)|={background-color: lightgreen;}.OK|
|use the PE simulator to confirm that the CSR will accept messages using the supported IP protocol (TCP and/or UDP)|Envoyer un message (ex: Test/armements - Envoyer RP) et constater dans le journal d'activité qu'il n'y a pas d'erreur d'envoi de message et que l'on reçoit une réponse. Faire cela pour tous les modes (TCP/UDP) indiqués sur la page du plugin|={background-color: lightgreen;}.OK|
|C.2.3.2 IP Addresses (ref 5.2)|verify that the IP address of the CSR can be manually programmed|Vérifier que l'on peut choisir l'IP que doit utiliser le plugin via un paramètre et que ce paramètre a bien un effet (ex: en utilisant ProcessExplorer)|={background-color: lightgreen;}.OK|
|/4.C.2.3.3 Encryption (ref 5.4)|set the PE simulator and CSR with matching encryption keys|Vérifier que l'on peut configurer une clef de chiffrement pour le plugin et pour le simulateur|={background-color: lightgreen;}.OK|
|for each DC-07 message type, transmit an encrypted message and ensure that the receiver simulator can decrypt it correctly|Envoyer un message RP depuis le simulateur, et constater qu'un SecurityEvent RP est créé dans Smart Shield|={background-color: lightgreen;}.OK|
|change the encryption key at the PE simulator and ensure that a message is not decrypted correctly|Mettre une clef différente dans le simulateur, et constater que le plugin renvoie un message d'erreur à la reception d'un message|={background-color: lightgreen;}.OK|
|repeat a subset the encryption tests (10%) for each supported encryption key length|Faire les tests de chiffrement avec une clef 128 bit, 192 bits et 256 bits|={background-color: lightgreen;}.OK|
|C.2.3.4 Cipher Block Chaining (ref. 5.4.6)|use the PE simulator to generate a message consisting of 3 encrypted blocks (length over 32 bytes) and observe that the CSR will correctly decrypt the message|Envoyer un message contenant beaucoup de données. Par exemple un événement avec un texte de plus de 32 caractères|={background-color: lightgreen;}.OK|
|C.2.3.5 CRC (ref. 5.5.1.2)|transmit a message to the CSR with an incorrect CRC and confirm that it does not respond to the message|Utiliser le simulateur : bouton "RP - CRC erroné" et constater dans le journal d'activité que le plugin ne répond pas|={background-color: lightgreen;}.OK|
|C.2.3.6 ID Token (ref. 5.5.1.4)|for each DC-07 message type, transmit an unencrypted message and ensure that the receiver simulator can decode it correctly|Faire un test RP avec les format SIA-DCS et ADM-CID et constater que le plugin renvoit un ACK à chaque fois|={background-color: lightgreen;}.OK|
|/3.C.2.3.7 Sequence Number (ref. 5.5.1.5)|cause the PE simulator to transmit a 3-block message with an extra block included in a sequence like the following: 1, 2, 1, 3 - confirm that the CSR can assemble and decode the proper message|Après pas mal de recherche, ce point semble être un mauvais copié/collé hérité de DC-07, car DC-09 ne gère pas les découpage de messages (géré niveau TCP/IP)|={background-color: lightgrey;}.Rien à tester|
|cause the PE simulator to transmit 3 single block messages with an extra block included in the sequence like the following: 9995, 9996, 9995 (extra), 9997 - confirm that all three messages are 
received only once|Forcer un sequence number et vérifier l'absence de doublon (ex: pas de SecurityEvent créé à nouveau)
L'onglet Test contient une fonction spécifique pour faire cela avec des messages RP|={background-color: lightgreen;}.OK|
|send reports from the PE simulator to confirm that the CSR sequence number properly increments through the sequence 9998, 9999, 0001, 0002|Un bouton de l'onglet Test permet de déclencher cette séquence|={background-color: lightgreen;}.OK|
|C.2.3.8 Account Identification (ref. 5.5.1.6)|Transmit reports from the PE simulator to confirm correct reception by the CSR when the following account ID parameters are included: 
* rcvr = 0 
* rcvr = 1234 
* rcvr = FFFFFF 
* no "R" field provided (no receiver number) 
* pref = 0 
* pref = 1234 
* pref = FFFFFF 
* acct = 0 
* acct = 123456 
* acct = 01234567879ABCDEF (may be truncated by some DC-04 reporting methods) 
* acct = FEDCBA9876543210 (may be truncated by some DC-04 reporting methods)|Tester avec ces valeurs. rcvr = "Receiver Number", pref = "Account Prefix", acct = "Account ID". Dans tous les cas, les messages doivent bien être traités (réponse ACK + SecurityEvent). Si les prefix ou account number sont différents, les objets créés doivent être reliés à des centrales différentes|={background-color: lightgreen;}.OK|
|/2.C.2.3.9 Message Data (ref. 5.5.1.7)|(using encryption, if supported) for each DC-07 message type, use the PE simulator to transmit 5 sample messages in which the event code and other parameters are varied, observe no transmission failures which may indicate a data-sensitive encryption failure|(Chiffrement activé) Envoyer plusieurs messages différents depuis le simulateur et constater que le plugin répond toujours correctement (ACK + création de SecurityEvent)|={background-color: lightgreen;}.OK|
|if the previous test was run with encryption, repeat the test with encryption disabled|Idem, mais en désactivant le chiffrment|={background-color: lightgreen;}.OK|
|C.2.3.10 MAC Address Data (ref. 5.5.1.8)|transmit a message with MAC address data included
* observe that all data elements of the message are correctly decoded 
* document the handling of the MAC data by the CSR|Avec le simulateur, envoyer un message qui contient l'adresse MAC (options) et constater qu'elle est bien dans les logs du plugin|={background-color: lightgreen;}.OK|
|C.2.3.10A  Network Address Data (ref. 5.5.1.8)|transmit a message with network address data included 
* observe that all data elements of the message are correctly decoded 
* document the handling of the network data by the CSR|Avec le simulateur, envoyer un message qui contient l'adresse IP (options) et constater qu'elle est bien dans les logs du plugin|={background-color: lightgreen;}.OK|
|C.2.3.11 Verification Data (ref. 5.5.1.8)|transmit a message to the CSR that includes arbitrary verification data and observe that all required (excludes verification data) data elements of the message are correctly decoded|Ajouter une URL vers une image (même fictive) dans le champs Verification Data du simulateur et vérifier que le plugin arrive tout de même à traiter les messages|={background-color: lightgreen;}.OK|
|C.2.3.12 Programming Data (ref. 5.5.1.8)|transmit a message to the CSR that includes arbitrary programming data and observe that all required (excludes programming data) data elements of the message are correctly decoded|Idem que précédent avec avec @P-DATA:VAR1=VAL1;VAR2=VAL2;EXTRA="!!//\\//!!"@ dans Programming Data|={background-color: lightgreen;}.OK|
|/2.C.2.3.13 Timestamp (ref. 5.5.1.9)|use the PE simulator to transmit an encrypted message with a timestamp that is 25 seconds greater than the time in the CSR - observe that the CSR rejects the message with a NAK including the CSR's time|/2.Fonction dédiée dans l'onglet test du simulateur|={background-color: lightgreen;}.OK|
|use the PE simulator to transmit an encrypted message with a timestamp that is 45 seconds less than the time in the CSR - observe that the CSR rejects the message with a NAK including the CSR's time|={background-color: lightgreen;}.OK|
|/5.C.2.3.14 Supervision Message (ref. 5.5.2) (when supported)|set the PE simulator to generate supervision messages every 50 seconds and the CSR to require them every minute - observe no supervision failures over 24 hours of testing|Sur une machine de test, configurer le plugin et le simulateur comme indiqué, et constater après 24h qu'aucun incident de perte de centrale n'a été créé|={background-color: yellow;}.A tester|
|disconnect the PE simulator and observe a supervision failure reported by the CSR within 60 seconds|Couper la supervision coté simulateur et constater la création d'incident|={background-color: lightgreen;}.OK|
|verify that the supervision interval at the CSR can be programmed in the range 10 seconds to 3600 seconds, and 1 hour to 1080 hours|Vérifier que le plugin accepte de 10 secondes à 1080 heures|={background-color: lightgreen;}.OK|
|verify by code inspection or other means that the supervision interval is correctly implemented in the CSR |Regarder ce qui est annoncé par les logs au lancement du programme, et vérifier que c'est cohérent avec quelques tests sur des durées courtes (programmer 10s, voir que le plugin annonce 10s, tester que ça déclenche bien après 10s. Programmer 10h et voir que le plugin annonce 10h)|={background-color: lightgreen;}.OK|
|verify supervision using both encrypted and unencrypted messages|Après avoir fait ces tests en non-chiffré, les refaire en chiffré|={background-color: lightgreen;}.OK|
|C.2.3.15 DUH Message (ref. 5.5.3.3)|cause the PE simulator to transmit a correctly formatted message with an invalid DC-07 message type - observe that the CSR returns the DUH response|Choisir un format de message incorrect, et constater que le plugin répond "DUH"|={background-color: lightgreen;}.OK|
|C.2.3.16 RSP Message (ref. 5.5.3.4)|If the CSR supports a RSP message: 
• cause the PE simulator to transmit a message that will elicit the RSP message 
• observe that the CSR returns a correctly formatted RSP response|Requiert la gestion des commandes (#8814), et que la supervision soit active coté simulateur. Faire une action sur un objet géré par le plugin, et constater le message RSP envoyé au simulateur|={background-color: red;}.Pas implementé coté plugin|
|C.2.3.17 No Response (ref. 5.6.1.1)|prevent the receiver simulator from responding to transmitted messages from the PE, and observe that at least one retry attempt occurs within 5 - 60 seconds|Ce test est un copié/collé erroné venant de la section sur le test de PE. Il n'a rien à faire ici car l'absence de réponse n'est pas à gérer par le plugin CSR|={background-color: lightgrey;}.Rien à tester|
~~~

### 25/03/2026 16:43 — Alan Raynaud

- Sujet : « Plugin CSR SIA (Central Station Receiver) - Plan de validation officiel du standard » → « Plugin CSR SIA (Central Station Receiver) - Plan de validation officiel du standard DC-09 »

~~~textile
Le plan de test du DC-03 n'est pas vraiment exploitable en l'état, car la plupart des tests sont du type "The event is processed, and the receiver returns a positive acknowledgement".

Ce case va donc conserner la compatibilité avec DC-09. Les fonctionnalités (liées au DC-03) seront testées dans les cases associés.
~~~

### 27/03/2026 14:21 — Alan Raynaud

- Statut : Nouveau → En cours
- Avancement : 0 % → 60 %

### 08/04/2026 16:45 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 60 % → 100 %
