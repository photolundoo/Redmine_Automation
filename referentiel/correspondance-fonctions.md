# Correspondance Fonction Redmine → plan de validation

Table de départ pour orienter l'analyse d'un ticket. Elle indique où chercher l'existant ; elle ne dispense pas de vérifier dans le plan. Version de travail du 16/10/2026, à valider.

## Règles d'application

1. Le sujet du ticket prime sur la Fonction pour déterminer l'application : un préfixe `[WebApp]` ou `WebApp :` désigne la WebApp ; `[DesktopApp]`, `[IHM]` ou une mention de la 3D désigne la WinApp ; `[MobileApp]` ou `[IsapMobile]` désigne l'application mobile.
2. Quand plusieurs plans sont proposés, chercher d'abord le numéro du ticket (`#NNNN`) dans tous les plans, puis les mots-clés du sujet dans les plans proposés, dans l'ordre de la colonne.
3. Une Fonction absente de cette table, ou un ticket qu'aucun plan ne couvre, donne lieu à une proposition de l'agent et à une ligne dans `decisions.md`.
4. Les tickets de tracker « Configuration » (Fonction souvent vide) décrivent la mise en place d'un environnement ou d'un site. Ils relèvent en général de la nature « Configuration d'environnement » : vérifier la mise en place, sans créer de fiche, sauf si le ticket décrit un comportement nouveau. La recherche dans les plans reste obligatoire : une fiche existante peut citer le composant concerné (version d’un logiciel tiers, machine de test, procédure d’installation) et devoir être mise à jour. Exemple : un ticket d’installation de Security Center se compare à la section « Genetec – SecurityCenter Video Plugin » du plan 03.
5.Les migrations de bibliothèques et mises à jour de dépendances (Ice, POCO, OpenSSL, cryptopp, ImageMagick, net-snmp, maven, Tomcat, compilation) relèvent de la nature « Non-régression technique ». Elles se rattachent à la fiche NRT01 — Passe de non-régression technique du plan 12, chacune sous un sous-titre portant le nom du composant. Elles ne créent pas de fiche par ticket.

## Table

| Fonction Redmine | Application | Plans à consulter (dans l'ordre) | Fiches candidates | Remarques |
|---|---|---|---|---|
| (vide) | Selon le sujet | Selon le sujet | — | Souvent tracker « Configuration » : voir règle 4. |
| ISAP Core - Administration | Serveur / outils d'administration | 11 Installation client sur PC ; 12 Update version ; 13 Outils externes ; 14 Planification | INS01, INS04, INS05 ; UPD01, UPD02 ; WIN15 (plan 13) | Outils d'installation, de déploiement (Ansible, ServerSetup), d'affectation et d'import. Import de planification : plan 14. |
| ISAP Core - Configuration | Serveur / grille | 12 Update version ; 11 Installation client sur PC ; 02 WinApp ; 01 WebApp | UPD01, UPD02 ; INS01 ; CONF01 à CONF04, CONF014 ; MC12 « Configuration Grille & droits » | Configurateur serveur, grille, IsapGridGUI. |
| ISAP Core - Gestion des capteurs | Serveur (processeurs) | 06 Intrusion ; 02 WinApp | INT01, INT03 ; CONF014, WIN15 (ActionManager) | IntrusionProcessor, ActionManager, inhibitions et désinhibitions. |
| ISAP Core - Gestion mobilité | Mobile | 08 Tests spécifiques ; 02 WinApp | SPE (géolocalisation) ; WIN06 Ressources | Création d'une fiche à effectuer. Soumise à relecture Humaine avant validation. |
| ISAP Core - Main Courante | WebApp / SDK Python | 01 WebApp | MC13 « Manipulation des fichiers » (SDK Python) ; MC10 « Export de données » ; MC11 | Scripts SDK autour de la Main Courante (notifications, exports, création d'incidents). |
| ISAP Core - Navigation 3D | WinApp ou WebApp selon le sujet (règle 1) | 02 WinApp ; 03 WinApp Vidéo ; 01 WebApp | WIN02 ; WVID01, WVID03 ; MC04 (labels), MC05 | Affichage 3D, cônes caméras, labels. |
| ISAP Core - SDK | Transverse | Selon le sujet ; 13 Outils externes ; 02 WinApp ; 11 et 12 | WIN15 (plan 13, API) ; « ISAP API Server » (plan 02) | Migrations : règle 5. API (SmartShieldWebAPI) : fiches API existantes. Licences : installation et mise à jour. |
| ISAP Core - Sécurité IT | Transverse | — | — | Mises à jour de dépendances : règle 5. |
| ISAP Fonctions - Iris | Serveur | 13 Outils externes | WIN15 (API) | Aucune fiche Iris identifiée : Création d'une fiche à effectuer. Soumise à relecture Humaine avant validation. |
| ISAP Fonctions mobiles - Gestion mobile d'incidents | Mobile | 08 Tests spécifiques | — | Aucun plan mobile dédié : Création d'une fiche à effectuer. Soumise à relecture Humaine avant validation. |
| ISAP Fonctions mobiles - Tracking mobile des positions | Mobile | 08 Tests spécifiques ; 02 WinApp | SPE (géolocalisation) ; WIN06 Ressources | |
| ISAP Plugins - Cameras & Encodeurs | WinApp Vidéo | 03 WinApp Vidéo | WVID01, WVID08, CONF05 | Plugins caméras, encodage d'images. |
| ISAP Plugins - Capteurs experts | Plugins et simulateurs | 06 Intrusion ; 08 Tests spécifiques | INT01, INT03 ; SPE | Simulateurs SIA, PAV, SNMP. |
| ISAP Plugins - Contrôle d'Accès | Plugins et simulateurs | 10 Contrôle d'accès | ACS01 à ACS04 | ACS04 Genetec non exécuté faute de matériel. |
| ISAP Plugins - Détection Incendie | WinApp | 05 Incendie ; 02 WinApp | INC01 à INC03 ; CONF03 (symboles des capteurs) | |
| ISAP Plugins - Détection Intrusion | Plugins | 06 Intrusion | INT01, INT03 | |
| ISAP Plugins - Géolocalisation | Plugins | 08 Tests spécifiques ; 09 3D multisites | SPE (géolocalisation) ; HMU01 | Positionnement intérieur, gestion d'étages. |
| WebApp - Accès & Ressources | WebApp | 01 WebApp | MC01 (connexion) ; MC02 (paramètres, CGU) ; MC06 (plugin vidéo local) | |
| WebApp - Administration | WebApp | 01 WebApp | MC10 « Onglet Administration » | |
| WebApp - Main Courante | WebApp | 01 WebApp | MC02 ; MC11 ; MC13 | Tableau de bord : pas de fiche dédiée identifiée, Création d'une fiche à effectuer. Soumise à relecture Humaine avant validation. Doit s'appuyer sur la documentation "Tableau de bord" indiqué dans le .env |
| WebApp - Mobile | WebApp (client léger mobile) | 01 WebApp | MC02 | Pas de fiche mobile : Création d'une fiche à effectuer. Soumise à relecture Humaine avant validation. |
| WebApp - Runsheet | WebApp | 01 WebApp ; 14 Planification | MC07 « Événements planifiés » ; MC08 (plan 14) | |
| WebApp - Situation | WebApp | 01 WebApp | MC04 « Situation » ; MC05 « Situation 3D » | |
| WebApp - Statistiques | WebApp | 01 WebApp | MC03 | |
| WebApp - Video | WebApp | 01 WebApp | MC06 « Onglet Vidéo » | |

## Particularités des plans à connaître

1. Plan 01 WebApp : les identifiants de fiche ne suivent pas toujours les titres. Il existe deux fiches MC10 (« Onglet Administration » et « Export de données ») et deux fiches MC12 (« Tests à plusieurs personnes » et « Configuration Grille & droits »). La fiche MC09 renvoie au plan 14 Planification. Toujours désigner une fiche par son identifiant suivi de son titre.
2. Plan 02 WinApp : WIN15 existe aussi dans le plan 13.
3. Plan 03 WinApp Vidéo : WVID06 et WVID07 sont utilisés trois fois chacun.
4. Plan 05 Incendie : INC02 est utilisé deux fois.
5. Plan 11 Installation : INS01 est utilisé quatre fois.
