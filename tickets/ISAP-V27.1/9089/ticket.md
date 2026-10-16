# #9089 — Amélioration de l'outils d'import de planification

| Champ | Valeur |
|---|---|
| Tracker | Evolution |
| Statut | Résolu |
| Priorité | Haut |
| Fonction | ISAP Core - Administration |
| Catégorie | com.egidium.isap.reporting |
| Version cible | ISAP-V27.1 |
| Auteur | Alan Raynaud |
| Assigné à | Alan Raynaud |
| Avancement | 100 % |
| Créé le | 25/09/2026 17:38 |
| Mis à jour le | 07/10/2026 13:52 |
| Origine | Interne |
| Phase | RD |
| Projet 1 à livrer | Produit |
| Projet 2 à livrer | Produit |
| Release notes | Non |
| Evolution majeure | 0 |
| Lien Redmine | https://srvfr-redmine/issues/9089 |

## Description

~~~textile
* Prendre en compte le changement du type sur les N° de poste : int --> string
* Vérifier la gestion des dossier 
** Cas constaté : nouvel import sur un dossier parallèle, avec des prestataires en commun : ils ne sont pas sur le nouveau dossier --> il faut s'assurer que les entités réutilisées (ex: prestataire) soient bien reliées au dossier cible (ajouter la relation si elle manque)
* Initialisation des tarification à 0
** Pour chaque couple Lot/PostType
*** Pour chaque couple [day, night] X [Week, Sunday, Holiday, SundayOff] (8 en tout)
**** Créer une entité @Tarification@
**** Attributs :
***** Base : 2
***** DayType (1, 2, 3 ou 4 : Week, Sunday, Holiday, SundayOff)
***** DisplayName et Name : hourly_DAYTYPE_TIME_POSTTYPEENTITYID_LOTENTITYID (ex: hourly_Weekday_night_53107_53559 )
***** Night : true si nuit
***** Price : 0.0
***** Specific : False
**** Parents (1/2)
***** Lot
***** Entreprise
***** PostType
***** PLanification
**** Enfant @Calendar@ à créer (relation 1/2)
***** Name identique au parent
***** BeginTimestamp et EndTimestamp : 01/01/1970 07:00:00 et 01/01/1970 22:00:00 selon si jour ou nuit 

Outils dans C:\DEV\EGIDIUM\com.egidium.isap.reporting\public\tools\PlanificationImporter

Definition de Tarification:
<pre>
$tarification_tid= createtemplate 'Tarification' 5 $planification_tid 1 2
eventtemplateattr $tarification_tid 'DisplayName' 'ATTR_ISTRING' 0 0 1
eventtemplateattr $tarification_tid 'Price' 'ATTR_DOUBLE' 0 0.01 1
eventtemplateattr $tarification_tid 'Base' 'ATTR_INT' 0 0 1
eventtemplateattr $tarification_tid 'DayType' 'ATTR_INT' 0 0 1
eventtemplateattr $tarification_tid 'Specific' 'ATTR_BOOLEAN' 0 0 1
eventtemplateattr $tarification_tid 'Nuit' 'ATTR_BOOLEAN' 0 0 1
eventtemplaterelation $tarification_tid $poste_tid 1
eventtemplaterelation $tarification_tid $entreprise_tid 1
eventtemplaterelation $tarification_tid $lot_tid 1
eventtemplaterelation $tarification_tid $postetype_tid 1

$calendar_tid= createtemplate 'Calendar' 5 $evenement_tid 1 2
eventtemplateattr $calendar_tid 'BeginTimestamp' 'ATTR_TIMESTAMP' 0 0 1
eventtemplateattr $calendar_tid 'EndTimestamp' 'ATTR_TIMESTAMP' 0 0 1
eventtemplaterelation $calendar_tid $tarification_tid 1
eventtemplaterelation $calendar_tid $detailPoste_tid 1
</pre>
~~~

## Historique

### 07/10/2026 11:48 — Alan Raynaud

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)
- Catégorie : com.egidium.pr.python → com.egidium.isap.reporting

### 07/10/2026 12:59 — Alan Raynaud

- Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)

### 07/10/2026 13:52 — Alan Raynaud

- Statut : Nouveau → Résolu
- Avancement : 0 % → 100 %
