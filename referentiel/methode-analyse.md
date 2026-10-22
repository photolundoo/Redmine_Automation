# Méthode d'analyse d'un ticket

Méthode en 5 étapes du pôle QA, appliquée par l'agent « Analyste ticket ». Elle complète `.github/copilot-instructions.md` et `referentiel/modele-analyse.md`. Dans ce document, `<version>` désigne le dossier de version (par exemple `ISAP-V27.1`) et `<n>` le numéro du ticket : toujours les remplacer par les valeurs réelles.

## a. Lire le ticket

1. Partir de la sortie de `python analyses.py contexte --ticket <n>` : mode, décisions du ticket, ligne de correspondance, occurrences de `#<n>` dans les plans, fiches candidates.
2. Lire `tickets/<version>/<n>/ticket.md` en entier : en-tête, description et tout l'historique.
3. Quand un commentaire renvoie à une capture (`!nom.png!`), l'ouvrir dans `tickets/<version>/<n>/pieces_jointes/` si les images sont lisibles.
4. Repérer dans l'historique les commentaires de test du pôle QA (« Test non validé », « NOK », « Ajouté au plan de validation »…) et les changements de statut qui les accompagnent.

## b. Situer le ticket dans les plans

Cette recherche est obligatoire pour tous les tickets, y compris de configuration ou de migration : une fiche existante peut devoir être mise à jour (version d'un logiciel tiers, procédure d'installation, machine de test), même quand aucune fiche n'est à créer.

1. Déterminer l'application et les plans à consulter avec `referentiel/correspondance-fonctions.md`, en appliquant ses règles. `contexte` affiche la ligne de la table qui correspond à la Fonction du ticket.
2. Reprendre les occurrences de `#<n>` données par `contexte` (plans et tests Playwright) et les vérifier dans les plans.
3. Lire les fiches candidates proposées par `contexte`, en commençant par les premières. Cette liste vient d'une recherche par mots-clés : elle oriente, elle ne décide pas. Chercher aussi les mots-clés propres au ticket (nom du composant, du logiciel tiers, du paramètre) dans les plans proposés, puis lire en entier la ou les sections pertinentes.
4. Ouvrir la section 3 de l'analyse par un paragraphe « **Recherche dans les plans.** » qui rapporte chaque recherche et son résultat : `#<n>` d'abord, puis chaque mot-clé, avec le plan, la fiche et le sous-titre trouvés, ou « aucune occurrence ». Quand une fiche candidate placée en tête par `contexte` est écartée, dire pourquoi.
5. Ne citer dans « Sources » que les plans réellement lus et dont la section 3 rapporte le contenu. Ajouter un plan aux sources sans l'avoir exploité est une faute, même si le vérificateur le réclame.

## c. Qualifier le ticket

Chaque champ contrôlé de la fiche signalétique prend une seule des valeurs ci-dessous. Environnement peut en combiner plusieurs avec « + », la principale en premier. Aucune autre valeur n'est acceptée par `python analyses.py verifier`.

| Champ | Valeurs autorisées |
|---|---|
| Application | WebApp · WinApp · Application mobile · Serveur et services · Transverse |
| Nature du test | Nouveau test · Re-test ciblé · Non-régression technique · Configuration d'environnement · Relecture documentaire · Hors campagne |
| Automatisabilité | Automatisable · Difficile · Impossible sans script externe · Hors outillage actuel · Non applicable |
| Environnement | WebApp · WinApp · Serveur / grille · Simulateur · Matériel · Mobile · Aucun |
| Confiance | Élevée · Moyenne · Faible |
| Décision humaine requise | Oui · Non |
| Issue | A — Reproduire l'existant · B — Adapter l'existant · C — Nouvelle procédure automatisable · D — Nouvelle procédure manuelle · Sans objet |

Repères :
1. **Application** : « Serveur et services » couvre les serveurs, processeurs, plugins, outils d'installation et de configuration ; « Transverse » couvre les bibliothèques et dépendances communes à plusieurs applications.
2. **Re-test ciblé** : le ticket a déjà été testé (commentaire QA dans l'historique ou `#<n>` présent au plan) et revient résolu. La procédure couvre en priorité les points signalés en échec, puis une vérification rapide du reste.
3. **Non-régression technique** et **Configuration d'environnement** : voir les règles 4 et 5 de la table de correspondance. La procédure vérifie le point précis corrigé ou mis en place par le ticket (par exemple l'erreur de démarrage décrite dans l'historique), pas seulement un fonctionnement général.
4. **Automatisabilité**, selon la grille du pôle QA et l'outillage actuel (Playwright, WebApp seulement) :
   - Automatisable : tout se fait dans le navigateur (WebApp), par un seul utilisateur. Un ticket serveur, WinApp ou mobile n'est jamais « Automatisable » ni « Difficile » ni « Impossible sans script externe » : il est « Hors outillage actuel ».
   - Difficile : plusieurs utilisateurs simultanés, attentes longues, données à préparer.
   - Impossible sans script externe : une étape sort du navigateur (fichier de configuration, grille, simulateur, IsapReporting).
   - Hors outillage actuel : WinApp, application mobile, serveur ou matériel, y compris les tickets de configuration et de non-régression technique.
   - Un ticket dont l'environnement comprend WebApp n'est jamais « Hors outillage actuel ». Si une étape sort du navigateur (attribut modifié dans IsapReporting, licence, script), il est « Impossible sans script externe ». Si rien ne se passe dans le navigateur (script SDK, envoi de courriel), l'environnement n'est pas WebApp.
   - Non applicable : relecture documentaire ou ticket hors campagne.
5. **Confiance** : Élevée seulement si le ticket dit clairement ce qui a été livré et comment l'observer. Moyenne si la procédure repose en partie sur des hypothèses. Faible si le ticket ne permet pas de savoir ce qui a été livré.

## c bis. Choisir l'issue

L'issue décide de ce que contient la section 4. Elle se choisit dans cet ordre, à partir de la recherche de l'étape b :

1. **Une fiche existante couvre la fonctionnalité du ticket ?** La lire en entier, puis écrire en section 3 le paragraphe « **Comparaison des procédures.** » : même parcours, mêmes données, même résultat observé que ce que demande le ticket ? Point par point.
   - **Elle teste exactement la même chose : issue A — Reproduire l'existant.** Pas de nouvelle procédure. La section 4 s'ouvre par « **Procédure existante à rejouer.** », cite la fiche, le sous-titre et les étapes du plan, puis reprend ces étapes en lignes « - … Résultat attendu : … (#<n>) ». La section 5 indique seulement d'ajouter `#<n>` aux étapes rejouées.
   - **Elle couvre la fonctionnalité, mais pas de la même manière : issue B — Adapter l'existant.** La section 4 s'ouvre par « **Écarts avec la procédure existante.** » (étapes conservées, modifiées, ajoutées), puis donne la procédure adaptée.
2. **Aucune fiche ne couvre la fonctionnalité :** une nouvelle procédure est écrite à partir des prérequis du test.
   - **Tout se joue dans le navigateur (WebApp) : issue C — Nouvelle procédure automatisable.** La procédure est écrite pour être transcrite en test Playwright sans réinterprétation : une action par étape (clic, saisie, navigation), un résultat attendu vérifiable à l'écran (texte, élément, état).
   - **Une partie sort du navigateur : issue D — Nouvelle procédure manuelle.** La section 4 contient en plus le bloc « ### Prérequis et moyens » : matériel, simulateur, machine, accès, données, personne à solliciter.
3. **Relecture documentaire ou hors campagne : « Sans objet ».**

Pour toute procédure automatisable (issue C, et issue B quand l'automatisabilité est « Automatisable » ou « Difficile »), ajouter en fin de section 4 le bloc « ### Spécification Playwright », destiné au projet de campagne Playwright :

```
### Spécification Playwright

- Type : @lecture, @ecriture ou @perturbateur
- Compte : compte utilisé (Playwright, Operator, AA…)
- Dossier : dossier de travail (racine, A, AA…)
- Référentiel : données qui doivent exister avant le test, ou « Aucun »
- Données créées : ce que le test crée et devra supprimer, ou « Aucune »
```

`@lecture` ne modifie rien ; `@ecriture` crée ses propres données et les supprime ; `@perturbateur` modifie un état partagé (droits, options, mot de passe, alerte, hors ligne, purge serveur).

Le vérificateur contrôle la cohérence : A et B exigent une fiche existante et le paragraphe de comparaison ; C exige l'environnement WebApp et une automatisabilité « Automatisable » ou « Difficile » ; D l'interdit ; les blocs obligatoires doivent être présents et remplis.

## c ter. Désigner la fiche cible

« Fiche cible » reprend l'identifiant et le titre exacts de la fiche, tels qu'ils figurent dans le plan, sous la forme `INT03 — Tests avec simulateur`. Ne jamais prendre la description de la fiche pour son titre. Pour une fiche sans identifiant, recopier son titre. Valeurs possibles sinon : « À décider » (question inscrite dans `decisions.md`), « À créer » ou « Aucune ». Le vérificateur contrôle que l'identifiant existe dans le plan cible, que le titre est le bon, que la section 5 nomme la fiche exactement de la même façon, et qu'aucune autre fiche du plan n'est présentée comme cible dans les sections 3 et 5.

## d. Respecter les décisions déjà prises

`contexte` liste les décisions du ticket. Celles marquées « appliquée » ou « À APPLIQUER » s'imposent à l'analyse, y compris quand elle est entièrement réécrite : une fiche retenue par l'humain reste la fiche cible, une correction reste appliquée. Celles « en attente » ou « à reformuler » ne s'appliquent pas.

## e. Rédiger l'analyse

Écrire `analyses/<version>/<n>.md` en suivant la forme de `referentiel/modele-analyse.md`. Le modèle montre la forme attendue avec un exemple : toutes les valeurs sont à établir pour chaque ticket, rien n'est à recopier.

1. Première ligne : `<!-- ticket: <n> | mis à jour : … -->`, avec la valeur exacte donnée par `contexte` (champ `updated_on` de `ticket.json`).
2. Les cinq sections numérotées suivent la méthode : étude du sujet, compte rendu de la situation, comparaison avec l'existant, procédure de test, intégration proposée.
3. Chaque étape de la procédure est une ligne commençant par « - », décrit une action, précise « Résultat attendu : » et se termine par `(#<n>)`. Une étape propre à un autre ticket appartient à l'analyse de cet autre ticket. Aucun identifiant ni mot de passe.
4. Une procédure établit le résultat : elle compte assez d'étapes pour mettre le système dans l'état voulu, provoquer le comportement du ticket et l'observer. Une procédure à une seule étape n'est acceptable que pour un contrôle réellement unique.
5. Chaque affirmation de la procédure vient du ticket ou du plan. Ce qui n'y figure pas est une hypothèse : l'écrire comme telle en section 2 et, si elle change la procédure, la reporter en question (étape f).
6. « Sources » liste les fichiers lus, dont au moins un plan de `referentiel/plans/` avec la section concernée.

## f. Reporter les questions

Pour chaque point ouvert, mettre « Décision humaine requise » à « Oui ». Si la même question figure déjà dans `decisions.md` pour ce ticket, ne pas la répéter. Sinon, l'inscrire avec le script, jamais en écrivant soi-même dans `decisions.md` :

```
python analyses.py question --ticket <n> --question "Question fermée ?" --proposition "Réponse proposée, en une phrase."
```

La proposition est une réponse unique et concrète, même provisoire : une fiche, une valeur, un comportement attendu, que l'humain pourra valider telle quelle ou corriger. Le script refuse une proposition qui contient une alternative (« ou », « soit », « à défaut ») ou qui renvoie la question (« faire valider », « à confirmer », « sous réserve », « par le responsable »). Exemple : au lieu de « Faire valider une durée par le responsable », proposer « Maintien en arrière-plan pendant 30 minutes ; perte de connexion provoquée en coupant le Wi-Fi ».

## g. Contrôler et journaliser

1. Lancer `python analyses.py verifier --ticket <n>` et corriger l'analyse sur le fond jusqu'à obtenir « Aucun écart ».
2. Inscrire une ligne au journal : `python analyses.py journal --ticket <n> --texte "analysé — nature du test, fiche cible"`.
