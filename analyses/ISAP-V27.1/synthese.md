# Synthèse des analyses — ISAP-V27.1

Générée le 16/10/2026 16:47 par `python analyses.py synthese`. Ne pas modifier à la main : le fichier est régénéré à chaque passage.

- Tickets dans la sélection : 58
- Analysés : 27 (dont 12 à reprendre : ticket modifié ou analyse non conforme)
- Non analysés : 31
- Décisions en attente dans `decisions.md` : 0

## Répartition — Issue

| Issue | Tickets |
|---|---|
| (non renseigné) | 12 |
| B — Adapter l'existant | 8 |
| D — Nouvelle procédure manuelle | 7 |

## Répartition — Nature du test

| Nature du test | Tickets |
|---|---|
| Nouveau test | 11 |
| Re-test ciblé | 9 |
| Non-régression technique | 4 |
| Configuration d'environnement | 3 |

## Répartition — Environnement

| Environnement | Tickets |
|---|---|
| Serveur / grille | 19 |
| WebApp | 2 |
| WebApp + Serveur / grille | 2 |
| WinApp | 1 |
| Serveur / grille + WinApp + Matériel | 1 |
| Serveur / grille + WinApp | 1 |
| Mobile | 1 |

## Répartition — Automatisabilité

| Automatisabilité | Tickets |
|---|---|
| Hors outillage actuel | 25 |
| Impossible sans script externe | 2 |

## Ordre de campagne

Tickets regroupés par environnement, puis par plan et par fiche, pour limiter les changements de configuration.

| Ticket | Sujet | Environnement | Plan | Fiche | Issue | Test Playwright existant | Décision requise |
|---|---|---|---|---|---|---|---|
| [#9030](9030.md) (à reprendre) | WebApp : Paramètre permettant de masquer les labels de certaines caméras | WebApp | 01 WebApp | MC04 — Onglet Situation |  | fiche couverte (35 tests) | Non |
| [#8898](8898.md) (à reprendre) | Le script SendMailOnIncident.py n'envoi pas la cartographie dans le mail | WebApp | 01 WebApp | MC13 — Manipulation des fichiers |  | fiche couverte (13 tests) | Non |
| [#8947](8947.md) | Evolution du modèle de licence : une licence par app WebApp | WebApp + Serveur / grille | 01 WebApp | À créer — Licences WebApp | D — Nouvelle procédure manuelle | — | Non |
| [#9087](9087.md) | AffectationTool v2 | WebApp + Serveur / grille | 13 Outils externes | Affectation Types / Places | B — Adapter l'existant | — | Non |
| [#7987](7987.md) (à reprendre) | [DesktopApp] Lenteur d'affichage des cônes caméras sur ville de Paris | WinApp | 03 WinApp Vidéo | WVID03 — Couverture vidéo |  | — | Non |
| [#8844](8844.md) | Configurer le site ACME avec les caméra Hanwha | Serveur / grille + WinApp + Matériel | 03 Plan de validation WINAPP_VIDEO | WVID07 — Comptage | B — Adapter l'existant | — | Non |
| [#9006](9006.md) | Installation et configuration de SecurityCenter 5.14 | Serveur / grille + WinApp | 03 WinApp Vidéo | WVID01 — Module Vidéo WinApp | B — Adapter l'existant | — | Non |
| [#8717](8717.md) | [IntrusionProcessor] Inhibition avec temporisation | Serveur / grille | 06 Intrusion | INT03 — Tests avec simulateur | B — Adapter l'existant | — | Non |
| [#9014](9014.md) | [ActionManager] Erreur de traitement pour les desinhibitions automatiques | Serveur / grille | 06 Intrusion | INT03 — Tests avec simulateur | B — Adapter l'existant | — | Non |
| [#9094](9094.md) | [PAVPlugin] PAV en doublons | Serveur / grille | 08 Tests spécifiques | À créer — PAVPlugin — Configuration et dédoublonnage | D — Nouvelle procédure manuelle | — | Non |
| [#7122](7122.md) (à reprendre) | [IsapReporting] Migration vers tomcat 11 | Serveur / grille | 11 Installation client sur PC | INS04 — Configuration serveur |  | — | Non |
| [#8939](8939.md) (à reprendre) | Tomcat ne fonctionne plus en mode non https | Serveur / grille | 11 Installation client sur PC | INS04 — Configuration serveur |  | — | Non |
| [#9049](9049.md) | [ServerConfiguration] Lors du remplissage initial de la base, le configurateur cherche des fichiers dans le dossier Fingerprint | Serveur / grille | 11 Installation client sur PC | INS04 — Installation complète d’un serveur-client | B — Adapter l'existant | — | Non |
| [#6918](6918.md) (à reprendre) | Migration POCO 1.15.3 | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique |  | — | Non |
| [#8080](8080.md) (à reprendre) | Compilation linux sur un environnement récent (Debian 13) | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique |  | — | Non |
| [#8805](8805.md) (à reprendre) | Mise à jour openSSL 3.5.8 | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique |  | — | Non |
| [#9033](9033.md) (à reprendre) | Migration Ice 3.7 : Java | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique |  | — | Non |
| [#9079](9079.md) | Migration Ice 3.7 : IsapGridGUI | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#8990](8990.md) (à reprendre) | Crash applicatif si la licence contient une limite non reconnue | Serveur / grille | 12 Update version | UPD02 — Monter de version |  | — | Non |
| [#8772](8772.md) | Outils d'ajout de plugin | Serveur / grille | 13 Outils externes | PluginWizard | B — Adapter l'existant | — | Non |
| [#8970](8970.md) (à reprendre) | SmartShieldWebAPI : Pouvoir demander la création d'un incident à partir de l'entityid de l'IncidentType | Serveur / grille | 13 Outils externes | SmartShieldWebAPI |  | — | Non |
| [#9016](9016.md) (à reprendre) | [SmartShieldWebAPI] Erreur HTTP 500 si le mot de passe du compte API contient un caractère "deux-points" | Serveur / grille | 13 Outils externes | SmartShieldWebAPI |  | — | Non |
| [#9089](9089.md) | Amélioration de l'outils d'import de planification | Serveur / grille | 14 Planification | À créer — PlanificationImporter | D — Nouvelle procédure manuelle | — | Non |
| [#9063](9063.md) | [ServerSetup] L'option "début différé" n'est pas prise en compte pour tous les services | Serveur / grille | À créer — Installation serveur | À créer — Démarrage différé des services | D — Nouvelle procédure manuelle | — | Non |
| [#9001](9001.md) | [Ansible] Anomalies constatés dont templates non à jours | Serveur / grille | À créer — Installation serveur | À créer — Déploiement Ansible WebAPI et Iris | D — Nouvelle procédure manuelle | — | Non |
| [#9026](9026.md) | [Ansible] Prendre en compte WebAPI/Iris | Serveur / grille | À créer — Installation serveur | À créer — Déploiement Ansible WebAPI et Iris | D — Nouvelle procédure manuelle | — | Non |
| [#8965](8965.md) | [MobileApp] Permettre de configurer son serveur au lancement | Mobile | 08 Tests spécifiques | À créer — Configuration du serveur dans MobileApp | D — Nouvelle procédure manuelle | — | Non |

## Tickets non encore analysés

- #9039 — ISAP Core - SDK — Migration Ice 3.7 : C++ - Slice2VT
- #9064 — ISAP Core - SDK — Migration cryptopp en 890
- #8915 — ISAP Core - Sécurité IT — Mettre à jour les packages maven
- #8966 — ISAP Fonctions - Iris — Iris : Lecture de mail HS pour curl < 7.62
- #8971 — ISAP Fonctions - Iris — Iris/MCP : créer les incident à partir de l'entityid du type d'incident
- #8765 — ISAP Fonctions mobiles - Gestion mobile d'incidents — [MobileApp] Éxécution de tâche en arrière plan
- #8780 — ISAP Fonctions mobiles - Tracking mobile des positions — [IsapMobile] Les fonctionnalités utilisant des liens FTP(S) ne fonctionnent plus
- #6017 — ISAP Plugins - Cameras & Encodeurs — Migrer vers ImageMagick++ 7.1.2
- #9075 — ISAP Plugins - Capteurs experts — Simulateur SIA : envoyer les messages vers un recepteur secondaire
- #9076 — ISAP Plugins - Capteurs experts — Migration net-snmp 5.9.5.2
- #9093 — ISAP Plugins - Capteurs experts — [PAVPlugin] Pouvoir désactiver la création d'alarme indépendamment du seuil
- #9082 — ISAP Plugins - Contrôle d'Accès — Simulateur AEOS
- #8183 — ISAP Plugins - Détection Incendie — Pictogrammes des Sensor de type Sprinkler
- #8816 — ISAP Plugins - Détection Intrusion — Plugin CSR SIA (Central Station Receiver) - Plan de validation officiel du standard DC-09
- #8787 — ISAP Plugins - Géolocalisation — Maquette Polestar : gestion d'étage
- #8982 — WebApp - Accès & Ressources — [WebApp] Timeout important sur les postes ne disposant pas du plugin vidéo en local
- #8992 — WebApp - Accès & Ressources — [WebApp] Impossible de se connecter après avoir accepté les CGU
- #8465 — WebApp - Administration — [WebApp/Administration] Bugs constatés dans la configuration d'un compte
- #8206 — WebApp - Main Courante — [WebApp][MainCourante] Gestion des incidents sur capteurs
- #8808 — WebApp - Main Courante — Plugin WhatsApp
- #9035 — WebApp - Main Courante — [WebApp/Dashboard] Affichage des capteurs en fonction de leur type et de leur état
- #9091 — WebApp - Main Courante — Migration Ice 3.7.11 - Javascript
- #7812 — WebApp - Mobile — [Main Courante] Client léger spécifique à l'utilisation sur mobile V2
- #9084 — WebApp - Mobile — [MobileApp] Score DEX inférieur au score minimum Playstore
- #8577 — WebApp - Runsheet — Le paramètre propagateRejectedActions n'est pas correctement pris en compte
- #9108 — WebApp - Runsheet — [WebApp][Runsheet] Changement non désiré des temps Durée et Pré-Affichage
- #8977 — WebApp - Situation — [WebApp] Mauvaise gestion par dossiers des ressources/instances
- #8838 — WebApp - Statistiques — [WebApp] Base du dashboard
- #8887 — WebApp - Video — WebApp : Permettre une utilisation de la vidéo sans Joystick
- #8941 — WebApp - Video — [WebApp] Droits spécifique pour la vidéo + gestion du plugin en local
- #9090 — WebApp - Video — [WebApp] Vision NOK dans le cas d'incident ayant pour source un capteur relié à une place
