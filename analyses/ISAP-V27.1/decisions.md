# Décisions à prendre — ISAP-V27.1

Remplir la colonne « Décision » avec l'une des formes suivantes, puis relancer `/analyser-tickets` :
- `valider` : la proposition de l'agent est retenue ;
- `corriger :` suivi de la correction, par exemple `corriger : la procédure doit aussi couvrir le mode Rejeu` ;
- `fiche :` suivi de la fiche à retenir, par exemple `fiche : MC02 Onglet Main Courante` ;
- `réanalyser` : l'agent refait l'analyse complète du ticket ;
- `hors campagne` : le ticket n'est pas testé dans cette campagne ;
- `ignorer` : la question est sans objet.

Toute autre formulation (« Approuvé », « OK », texte libre…) n'est pas appliquée par l'agent : elle reste en attente jusqu'à reformulation.

| Ticket | Question | Proposition de l'agent | Décision | Appliquée le |
|---|---|---|---|---|
| #8844 | Le comptage de véhicules des caméras Hanwha doit-il être réactivé depuis la résolution du ticket #8848 ? | Vérifier et activer le scénario uniquement s'il est prévu pour la démonstration ACME. | corriger : activer les scénarios et plugins nécessaires au comptage de véhicules, et l'ajouter à la procédure | 16/10/2026 |
| #9026 | Quel plan et quelle fiche doivent porter la recette de déploiement serveur Ansible de WebAPI et Iris ? | Créer une procédure de déploiement Ansible dans le plan 12 Update version ou dans le plan d'installation serveur s'il est disponible. | Nouveau Plan |  |
| #9063 | Quel plan et quelle fiche doivent recevoir le contrôle des services serveur en démarrage différé ? | Ajouter le contrôle dans une fiche d'installation serveur ; à défaut, l'ajouter après les options d'installation du plan 11. | Nouveau Plan |  |
| #9089 | Quel identifiant et quel emplacement retenir pour la fiche PlanificationImporter ? | Créer une fiche dédiée dans le plan 14 Planification, avant les contrôles de configuration. | validé |  |
| #9001 | La fiche de déploiement Ansible retenue pour #9026 couvre-t-elle aussi les corrections de mise à jour de #9001 ? | Regrouper les contrôles d'installation et de mise à jour Ansible dans la même fiche. | validé |  |
| #8965 | Faut-il créer une fiche de validation dédiée à la configuration du serveur dans MobileApp ? | Créer une fiche dans le plan 08 Tests spécifiques et soumettre la procédure à relecture humaine. |  |  |
