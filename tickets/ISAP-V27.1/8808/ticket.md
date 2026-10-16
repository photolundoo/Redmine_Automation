# #8808 — Plugin WhatsApp

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Normal |
| Fonction | WebApp - Main Courante |
| Catégorie | com.egidium.isap.gui.web |
| Version cible | ISAP-V27.1 |
| Ticket parent | #8843 |
| Auteur | Mickael Boual |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 11/03/2026 15:12 |
| Mis à jour le | 17/07/2026 09:53 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | VIPARIS |
| Projet 2 à livrer | Produit |
| Release notes | Oui |
| Lien Redmine | https://srvfr-redmine/issues/8808 |

## Description

~~~textile
Fonctions attendues :
* Envoi automatique de message sur Incident et PoliceLog
** Filtrage en fonction du type d'incident / policelog
** Envoi vers l'agent correspondant au "Pris en charge par" 
** Envoi vers une liste d'agents pour un SecurityCompany prédéfinies
* Saisie dans la MCE des messages remontés par les agents
** Dont PJ
~~~

## Relations

- Bloquée par #8852
- Bloquée par #8851

## Pièces jointes

- [clipboard-202603121129-dag7w.png](pieces_jointes/clipboard-202603121129-dag7w.png) — 243 Ko, ajoutée par Alan Raynaud le 12/03/2026 11:29
- [TestWhatsApp.py](pieces_jointes/TestWhatsApp.py) — 3 Ko, ajoutée par Alan Raynaud le 12/03/2026 11:30
- [clipboard-202604071634-hq21u.png](pieces_jointes/clipboard-202604071634-hq21u.png) — 59 Ko, ajoutée par Alan Raynaud le 07/04/2026 16:34
- [clipboard-202604071650-czpuq.png](pieces_jointes/clipboard-202604071650-czpuq.png) — 467 Ko, ajoutée par Alan Raynaud le 07/04/2026 16:50
- [clipboard-202607161339-anb7a.png](pieces_jointes/clipboard-202607161339-anb7a.png) — 133 Ko, ajoutée par Guillaume Lemaitre le 16/07/2026 13:39
- [clipboard-202607161341-5nhhm.png](pieces_jointes/clipboard-202607161341-5nhhm.png) — 20 Ko, ajoutée par Guillaume Lemaitre le 16/07/2026 13:41
- [clipboard-202607161342-fj1yl.png](pieces_jointes/clipboard-202607161342-fj1yl.png) — 101 Ko, ajoutée par Guillaume Lemaitre le 16/07/2026 13:42

## Historique

### 11/03/2026 15:12 — Alan Raynaud

~~~textile
A regarder : https://developers.facebook.com/documentation/business-messaging/whatsapp/overview
~~~

### 12/03/2026 10:00 — Alan Raynaud

- Début : (vide) → 12/03/2026

~~~textile
Pour analyser faisabilité
~~~

### 12/03/2026 10:39 — Alan Raynaud

~~~textile
L'API WhatsApp existe, mais :
* L'envoi à des personnes devrait être OK (POC à faire pour valider)
* L'envoi à des groupes est techniquement possible, MAIS est reservé aux entreprises que Meta a approuvé pour le programme OBA, ce qui est très, très restrictif
~~~

### 12/03/2026 10:40 — Alan Raynaud

~~~textile
> L’éligibilité au statut de compte professionnel officiel est soumise au respect des critères suivants :
> * [...]
> * L’entreprise doit être enregistrée sur la plateforme WhatsApp Business depuis au moins 30 jours.
> * L’entreprise doit représenter une entreprise, marque ou entité bénéficiant d’une certaine notoriété, bien connue et faisant l’objet de nombreuses recherches.
> * Le portefeuille business auquel appartient le numéro doit avoir fait l’objet d’une vérification de l’entreprise.
> * [...]
> 
> 
> La notoriété nécessite qu’une entreprise représente +une marque ou une entité connue faisant l’objet de recherches fréquentes+. Cela ne doit pas être compris comme un signe d’authenticité de l’entreprise.
> La notoriété reflète également une présence importante dans les articles de presse en ligne. La notoriété est évaluée sur la base de la +présence d’un compte dans les articles de presse issus de publications ayant des audiences importantes+. Les contenus rémunérés ou promotionnels, y compris les annonces professionnelles ou d’application, ne sont pas considérés comme des sources à examiner.
~~~

### 12/03/2026 11:18 — Alan Raynaud

~~~textile
Remarque : il n'est pas possible d'envoyer de texte libres. Les messages doivent utiliser des templates qui doivent être manuellement approuvés par Meta.
~~~

### 12/03/2026 11:30 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202603121129-dag7w.png
- Pièce jointe ajoutée : TestWhatsApp.py

~~~textile
Faisabilité technique OK

!clipboard-202603121129-dag7w.png!
~~~

### 12/03/2026 11:39 — Alan Raynaud

~~~textile
Tout a été fait avec un compte perso pour le moment.

Pour pouvoir passer en prod, il faudra :
* Créer un "Portefeuille business" officiel pour Egidium technologies (j'en ai fait un provisoire pour mes test, je peux peut-être le transférer pour qu'il soit compléter puis deviennent officiel)
* Faire vérifier l'entreprise (prouver que c'est bien Egidium qui administre ce portefeuille business)
* Dans ce portefeuille Business, créer une application
* Associer des développeurs à cette application
* Configurer cette application (dont lien avec un numéro de téléphone emetteur)
* Publier l'application
~~~

### 07/04/2026 15:24 — Alan Raynaud

~~~textile
Je fais pour l'instant mes tests en mode dev, mais il faudra régler les éléments suivants pour passer en prod :
* Business Manager Vérifié : Requiert de fournir des documents administratifs (KBis, etc.) dans "Paramètres de l'entreprise / Informations sur l'entreprise"
* Application en mode "Live" (la doc dit de basculer l'interrupteur en haut du tableau de bord Meta de "Développement" à "Live", mais j'ai pas trouvé. Peut-être parce qu'on est pas envore vérifiés)
* Token d'accès Permanent : ne plus utiliser le token temporaire mais créer un "Système User" dans le Business Manager, lui donner les accès à l'App, et générer un token avec les permissions whatsapp_business_messaging et whatsapp_business_management.
* Définition d'un numéro "source" : on peut utiliser un numéro OVH ? Le numéro *ne doit pas être lié à un compte whatsapp existant*
* Enregistrement du numéro : Enregistrer le numéro dans WhatsApp > Configuration de l'API et valider par SMS ou appel vocal. 
* Méthode de Paiement : Associer une carte bancair au compte WhatsApp Business dans le Business Manager (le "WhatsApp Business Account").
* Validation des templates : faire valider tous les template de message à utiliser (doivent être "Approved")
* Preuve d'Opt-in : WhatsApp est très strict, *on doit pouvoir prouver que les agents ont accepté de recevoir des alertes sur leur WhatsApp personnel* 
~~~

### 07/04/2026 16:56 — Alan Raynaud

- Pièce jointe ajoutée : clipboard-202604071634-hq21u.png
- Pièce jointe ajoutée : clipboard-202604071650-czpuq.png

~~~textile
POC validé :

!clipboard-202604071650-czpuq.png!

!clipboard-202604071634-hq21u.png!
~~~

### 08/04/2026 14:19 — Alan Raynaud

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)
- Statut : Nouveau → En cours
- Version cible : Candidate for next major release → ISAP-V27.1
- Ticket parent : (vide) → #8843
- Projet 1 à livrer : Autres (POC ...) → VIPARIS

### 08/04/2026 14:19 — Alan Raynaud

- Avancement : 0 % → 30 %
- Temps estimé : (vide) → 30.0 h

### 08/04/2026 14:40 — Alan Raynaud

- Sujet : « [WebApp] -  Ajouter l'envoi d'un incident sur WhatsApp en fonction de critère(s) (niveau de gravité atteint, en fonction d'un type ou autre) » → « Plugin WhatsApp »

### 08/04/2026 14:41 — Alan Raynaud

- Relation ajoutée (bloquée par) : #8852

### 08/04/2026 14:41 — Alan Raynaud

- Relation ajoutée (bloquée par) : #8851

### 08/04/2026 16:40 — Alan Raynaud

- Avancement : 30 % → 50 %

### 23/04/2026 11:37 — Alan Raynaud

~~~textile
Nous avons désormais un numéro WhatsApp dédié : +33 9 72 55 78 50 (c'est le numéro d'astreinte)
~~~

### 27/04/2026 15:38 — Alan Raynaud

~~~textile
Architecture :
* Service de reception webhook sur DMZ 
** Basé sur flask (idem reception agnet)
** En test manuel actuellement sur tacticplan
** A déployer avec démarrage auto sur(ex: agnet.egidium.fr). Attention au certificat (ajouter à PRTG pour surveillance)
** URL retenue à configurer sur https://developers.facebook.com/ (Cas d'usage WhatsApp / Configuration de base / Configuration de la prod / Configure Webhooks)
* Plugin WhatsApp
** Déployable sur réseau sécurisé à condition d'avoir des accès sortant vers meta (envoi de message) et la DMZ (récupération des messages)
** A mettre dans la grille



Eléments de configuration :
* WHATSAPP_APP_SECRET
** Secret de "l'app", pour vérifier la signature des messages
** A récupérer sur https://developers.facebook.com/ (Paramètres de l'app / Général / Clef secrètes) et configurer sur le service de reception des webhook
* WHATSAPP_VERIFY_TOKEN
** Authentification du whatsapp auprès du service de reception des webhook
** À configurer sur https://developers.facebook.com/ (Cas d'usage WhatsApp / Configuration de base / Configuration de la prod / Configure Webhooks) et sur le service de reception des webhook
* SMARTSHIELD_API_TOKEN
** Clef d'authentification du plugin auprès du service de reception des webhook
** À configurer sur le plugin et sur le service de reception des webhook
* WABA_ID (WhatsApp Business Account ID)
** "Compte Egidium" chez Meta
** À configurer sur le plugin
* PHONE_NUMBER_ID 
** Numéro de téléphone "émetteur". Doit être un numéro de téléphone enregistré sur notre compte.
** À configurer sur le plugin
* ACCESS_TOKEN 
** Token de connexion à l'API
** TODO : A générer sur l'interface whatspp (où???)
** À configurer sur le plugin
~~~

### 27/04/2026 15:40 — Alan Raynaud

~~~textile
Actions restantes (hors dev) :
* Mettre l'URL de Politique de Confidentialité
* Générer un token d'accès API permanent
* Passer l'application en mode live
* Déployer l'outils de réception webhook sur agnet.egidium.fr
* Définir les modèles de message
~~~

### 28/04/2026 15:13 — Alan Raynaud

~~~textile
Déployé sur agnet.egidium.fr:8443 + ajouté à PRTG pour surveillance
~~~

### 29/04/2026 16:45 — Alan Raynaud

- Avancement : 50 % → 70 %

~~~textile
Dev : 
* la partie PoliceLog
* grille
* utiliser IsapLogging
* Gérer le multiple pris en charge par
* Permettre de prendre TOUS les types d'incidents
~~~

### 21/05/2026 16:12 — Alan Raynaud

- Statut : En cours → Résolu
- Avancement : 70 % → 100 %
- Release notes : (vide) → Oui

~~~textile
Livré sur srvfr-dijon
~~~

### 04/06/2026 16:00 — Alan Raynaud

~~~textile
Corrigé : envoi de message dans le cas des incident dont le type n'a pas de catégorie.
~~~

### 16/07/2026 13:43 — Guillaume Lemaitre

- Pièce jointe ajoutée : clipboard-202607161339-anb7a.png
- Pièce jointe ajoutée : clipboard-202607161341-5nhhm.png
- Pièce jointe ajoutée : clipboard-202607161342-fj1yl.png

~~~textile
Réalisé depuis téléphone personnel

!clipboard-202607161339-anb7a.png!

Ce qu'on peut noter : 
* Mon nom d'affichage est le bon (sur téléphone perso)
* Les messages envoyé (dans la même minute) sont tous compacté dans le commentaire de la mention
!clipboard-202607161341-5nhhm.png!

Si pas dans la même minute, les messages envoyés créer des mention distinctes
!clipboard-202607161342-fj1yl.png!

Ce comportement est-il celui attendu ?
~~~

### 16/07/2026 13:58 — Guillaume Lemaitre

~~~textile
Test validé
~~~

### 17/07/2026 09:53 — Guillaume Lemaitre

~~~textile
Documenté dans le plan de validation 13_Plan de validation 26.1 - Outils Externes
~~~
