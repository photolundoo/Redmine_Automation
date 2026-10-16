# Synthèse des analyses — ISAP-V27.1

Générée le 16/10/2026 17:56 par `python analyses.py synthese`. Ne pas modifier à la main : le fichier est régénéré à chaque passage.

- Tickets dans la sélection : 58
- Analysés : 58 (dont 0 à reprendre : ticket modifié ou analyse non conforme)
- Non analysés : 0
- Décisions en attente dans `decisions.md` : 18

## Répartition — Issue

| Issue | Tickets |
|---|---|
| B — Adapter l'existant | 38 |
| D — Nouvelle procédure manuelle | 18 |
| C — Nouvelle procédure automatisable | 2 |

## Répartition — Nature du test

| Nature du test | Tickets |
|---|---|
| Re-test ciblé | 22 |
| Nouveau test | 20 |
| Non-régression technique | 13 |
| Configuration d'environnement | 3 |

## Répartition — Environnement

| Environnement | Tickets |
|---|---|
| Serveur / grille | 24 |
| WebApp | 15 |
| WebApp + Serveur / grille | 4 |
| WinApp | 4 |
| Mobile | 4 |
| Simulateur | 3 |
| WinApp + Serveur / grille | 1 |
| Serveur / grille + Matériel | 1 |
| Serveur / grille + WinApp + Matériel | 1 |
| Serveur / grille + Simulateur | 1 |

## Répartition — Automatisabilité

| Automatisabilité | Tickets |
|---|---|
| Hors outillage actuel | 39 |
| Difficile | 11 |
| Impossible sans script externe | 6 |
| Automatisable | 2 |

## Ordre de campagne

Tickets regroupés par environnement, puis par plan et par fiche, pour limiter les changements de configuration.

| Ticket | Sujet | Environnement | Plan | Fiche | Issue | Test Playwright existant | Décision requise |
|---|---|---|---|---|---|---|---|
| [#8982](8982.md) | [WebApp] Timeout important sur les postes ne disposant pas du plugin vidéo en local | WebApp | 01 WebApp | MC01 — Généraux | B — Adapter l'existant | fiche couverte (9 tests) | Non |
| [#7812](7812.md) | [Main Courante] Client léger spécifique à l'utilisation sur mobile V2 | WebApp | 01 WebApp | MC02 — Onglet Main Courante | B — Adapter l'existant | fiche couverte (159 tests) | Oui |
| [#8206](8206.md) | [WebApp][MainCourante] Gestion des incidents sur capteurs | WebApp | 01 WebApp | MC02 — Onglet Main Courante | B — Adapter l'existant | fiche couverte (159 tests) | Oui |
| [#8992](8992.md) | [WebApp] Impossible de se connecter après avoir accepté les CGU | WebApp | 01 WebApp | MC02 — Onglet Main Courante | B — Adapter l'existant | fiche couverte (159 tests) | Non |
| [#8977](8977.md) | [WebApp] Mauvaise gestion par dossiers des ressources/instances | WebApp | 01 WebApp | MC04 — Onglet Situation | B — Adapter l'existant | fiche couverte (35 tests) | Oui |
| [#9030](9030.md) | WebApp : Paramètre permettant de masquer les labels de certaines caméras | WebApp + Serveur / grille | 01 WebApp | MC04 — Onglet Situation | B — Adapter l'existant | fiche couverte (35 tests) | Non |
| [#9090](9090.md) | [WebApp] Vision NOK dans le cas d'incident ayant pour source un capteur relié à une place | WebApp | 01 WebApp | MC04 — Onglet Situation | B — Adapter l'existant | fiche couverte (35 tests) | Non |
| [#8887](8887.md) | WebApp : Permettre une utilisation de la vidéo sans Joystick | WebApp | 01 WebApp | MC05 — Onglet Vidéo | B — Adapter l'existant | ticket cité dans 7 test(s) ; fiche couverte (26 tests) | Non |
| [#8941](8941.md) | [WebApp] Droits spécifique pour la vidéo + gestion du plugin en local | WebApp | 01 WebApp | MC05 — Onglet Vidéo | B — Adapter l'existant | fiche couverte (26 tests) | Oui |
| [#9108](9108.md) | [WebApp][Runsheet] Changement non désiré des temps Durée et Pré-Affichage | WebApp | 01 WebApp | MC06 — Onglet Evénements | B — Adapter l'existant | fiche couverte (16 tests) | Non |
| [#8465](8465.md) | [WebApp/Administration] Bugs constatés dans la configuration d'un compte | WebApp | 01 WebApp | MC10 — Onglet Administration | B — Adapter l'existant | fiche couverte (67 tests) | Non |
| [#8577](8577.md) | Le paramètre propagateRejectedActions n'est pas correctement pris en compte | WebApp | 01 WebApp | MC12 — Tests à plusieurs personnes | B — Adapter l'existant | fiche couverte (16 tests) | Oui |
| [#8947](8947.md) | Evolution du modèle de licence : une licence par app WebApp | WebApp + Serveur / grille | 01 WebApp | À créer — Licences WebApp | D — Nouvelle procédure manuelle | — | Non |
| [#8838](8838.md) | [WebApp] Base du dashboard | WebApp | 01 WebApp | À créer — Tableau de bord WebApp | C — Nouvelle procédure automatisable | — | Oui |
| [#9035](9035.md) | [WebApp/Dashboard] Affichage des capteurs en fonction de leur type et de leur état | WebApp | 01 WebApp | À créer — Tableau de bord des capteurs | C — Nouvelle procédure automatisable | — | Oui |
| [#9091](9091.md) | Migration Ice 3.7.11 - Javascript | WebApp | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#9087](9087.md) | AffectationTool v2 | WebApp + Serveur / grille | 13 Outils externes | Affectation Types / Places | B — Adapter l'existant | — | Non |
| [#8808](8808.md) | Plugin WhatsApp | WebApp | 13 Outils externes | À créer — Plugin WhatsApp | D — Nouvelle procédure manuelle | — | Oui |
| [#8898](8898.md) | Le script SendMailOnIncident.py n'envoi pas la cartographie dans le mail | WebApp + Serveur / grille | À créer — Test script python - Envoi de mail | À créer — Notification mail avec cartographie | D — Nouvelle procédure manuelle | — | Non |
| [#8183](8183.md) | Pictogrammes des Sensor de type Sprinkler | WinApp | 02 WinApp | CONF03 — Configurations des labels | B — Adapter l'existant | — | Non |
| [#7987](7987.md) | [DesktopApp] Lenteur d'affichage des cônes caméras sur ville de Paris | WinApp + Serveur / grille | 07 Performances / charges | PERF01 — Robustesse | B — Adapter l'existant | — | Non |
| [#8787](8787.md) | Maquette Polestar : gestion d'étage | WinApp | 08 Tests spécifiques | À créer — Polestar — Gestion d'étage | D — Nouvelle procédure manuelle | — | Oui |
| [#6017](6017.md) | Migrer vers ImageMagick++ 7.1.2 | WinApp | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#9039](9039.md) | Migration Ice 3.7 : C++ - Slice2VT | WinApp | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#9006](9006.md) | Installation et configuration de SecurityCenter 5.14 | Serveur / grille + Matériel | 03 Plan de validation WINAPP_VIDEO | Genetec – SecurityCenter Video Plugin | B — Adapter l'existant | — | Non |
| [#8844](8844.md) | Configurer le site ACME avec les caméra Hanwha | Serveur / grille + WinApp + Matériel | 03 Plan de validation WINAPP_VIDEO | WVID07 — Comptage | B — Adapter l'existant | — | Non |
| [#8717](8717.md) | [IntrusionProcessor] Inhibition avec temporisation | Serveur / grille + Simulateur | 06 Intrusion | INT03 — Tests avec simulateur | B — Adapter l'existant | — | Non |
| [#9014](9014.md) | [ActionManager] Erreur de traitement pour les desinhibitions automatiques | Serveur / grille | 06 Intrusion | INT03 — Tests avec simulateur | B — Adapter l'existant | — | Non |
| [#9094](9094.md) | [PAVPlugin] PAV en doublons | Serveur / grille | 08 Tests spécifiques | À créer — PAVPlugin — Configuration et dédoublonnage | D — Nouvelle procédure manuelle | — | Non |
| [#9093](9093.md) | [PAVPlugin] Pouvoir désactiver la création d'alarme indépendamment du seuil | Serveur / grille | 08 Tests spécifiques | À créer — PAVPlugin — État du capteur et création d'incident | D — Nouvelle procédure manuelle | — | Oui |
| [#8939](8939.md) | Tomcat ne fonctionne plus en mode non https | Serveur / grille | 11 Installation client sur PC | INS04 — Installation complète d’un serveur-client | B — Adapter l'existant | — | Non |
| [#9049](9049.md) | [ServerConfiguration] Lors du remplissage initial de la base, le configurateur cherche des fichiers dans le dossier Fingerprint | Serveur / grille | 11 Installation client sur PC | INS04 — Installation complète d’un serveur-client | B — Adapter l'existant | — | Non |
| [#6918](6918.md) | Migration POCO 1.15.3 | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#7122](7122.md) | [IsapReporting] Migration vers tomcat 11 | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#8080](8080.md) | Compilation linux sur un environnement récent (Debian 13) | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#8805](8805.md) | Mise à jour openSSL 3.5.8 | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#8915](8915.md) | Mettre à jour les packages maven | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#8990](8990.md) | Crash applicatif si la licence contient une limite non reconnue | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#9033](9033.md) | Migration Ice 3.7 : Java | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Oui |
| [#9064](9064.md) | Migration cryptopp en 890 | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#9076](9076.md) | Migration net-snmp 5.9.5.2 | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#9079](9079.md) | Migration Ice 3.7 : IsapGridGUI | Serveur / grille | 12 Update version | NRT01 — Passe de non-régression technique | B — Adapter l'existant | — | Non |
| [#8772](8772.md) | Outils d'ajout de plugin | Serveur / grille | 13 Outils externes | PluginWizard | B — Adapter l'existant | — | Non |
| [#8970](8970.md) | SmartShieldWebAPI : Pouvoir demander la création d'un incident à partir de l'entityid de l'IncidentType | Serveur / grille | 13 Outils Externes | SmartShieldWebAPI | B — Adapter l'existant | — | Non |
| [#9016](9016.md) | [SmartShieldWebAPI] Erreur HTTP 500 si le mot de passe du compte API contient un caractère "deux-points" | Serveur / grille | 13 Outils Externes | SmartShieldWebAPI | B — Adapter l'existant | — | Non |
| [#8971](8971.md) | Iris/MCP : créer les incident à partir de l'entityid du type d'incident | Serveur / grille | 13 Outils externes | À créer — Iris — Création d’incident par entityId | D — Nouvelle procédure manuelle | — | Oui |
| [#8966](8966.md) | Iris : Lecture de mail HS pour curl < 7.62 | Serveur / grille | 13 Outils externes | À créer — Iris — Lecture de courriels | D — Nouvelle procédure manuelle | — | Oui |
| [#9089](9089.md) | Amélioration de l'outils d'import de planification | Serveur / grille | 14 Planification | À créer — PlanificationImporter | D — Nouvelle procédure manuelle | — | Non |
| [#9063](9063.md) | [ServerSetup] L'option "début différé" n'est pas prise en compte pour tous les services | Serveur / grille | À créer — Installation serveur | À créer — Démarrage différé des services | D — Nouvelle procédure manuelle | — | Non |
| [#9001](9001.md) | [Ansible] Anomalies constatés dont templates non à jours | Serveur / grille | À créer — Installation serveur | À créer — Déploiement Ansible WebAPI et Iris | D — Nouvelle procédure manuelle | — | Non |
| [#9026](9026.md) | [Ansible] Prendre en compte WebAPI/Iris | Serveur / grille | À créer — Installation serveur | À créer — Déploiement Ansible WebAPI et Iris | D — Nouvelle procédure manuelle | — | Non |
| [#8816](8816.md) | Plugin CSR SIA (Central Station Receiver) - Plan de validation officiel du standard DC-09 | Simulateur | 06 Intrusion | À créer — Plugin CSR SIA — Conformité DC-09 | D — Nouvelle procédure manuelle | — | Oui |
| [#9075](9075.md) | Simulateur SIA : envoyer les messages vers un recepteur secondaire | Simulateur | 06 Intrusion | À créer — Plugin CSR SIA — Conformité DC-09 | D — Nouvelle procédure manuelle | — | Oui |
| [#9082](9082.md) | Simulateur AEOS | Simulateur | 10 Contrôle d'accès | ACS02 — Tests avec simulateur | B — Adapter l'existant | — | Non |
| [#9084](9084.md) | [MobileApp] Score DEX inférieur au score minimum Playstore | Mobile | 08 Tests spécifiques | À créer — Application mobile : contrôle du score DEX | D — Nouvelle procédure manuelle | — | Oui |
| [#8765](8765.md) | [MobileApp] Éxécution de tâche en arrière plan | Mobile | 08 Tests spécifiques | À créer — Application mobile — Exécution en arrière-plan | D — Nouvelle procédure manuelle | — | Oui |
| [#8780](8780.md) | [IsapMobile] Les fonctionnalités utilisant des liens FTP(S) ne fonctionnent plus | Mobile | 08 Tests spécifiques | À créer — Application mobile — Transfert de fichiers | D — Nouvelle procédure manuelle | — | Oui |
| [#8965](8965.md) | [MobileApp] Permettre de configurer son serveur au lancement | Mobile | 08 Tests spécifiques | À créer — Configuration du serveur dans MobileApp | D — Nouvelle procédure manuelle | — | Non |
