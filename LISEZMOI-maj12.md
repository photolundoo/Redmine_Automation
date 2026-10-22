# Mise à jour 12 — passage autonome par sous-agents

## Ce qui change

1. `/analyser-tickets` lance désormais l'agent « Coordinateur tickets ». Il confie chaque ticket à un sous-agent qui part d'un contexte vierge : « Analyste ticket » pour analyser ou reprendre, « Applicateur décision » pour appliquer une décision, « Relecteur analyse » pour relire.
2. Le passage n'est plus limité à un lot : il traite toute la file, puis fait relire les analyses du passage, puis fait le bilan. Le paramètre `lot=` reste disponible pour limiter un passage.
3. Le script décide de tout ce qui est mécanique : `prochain` donne la file et le mode de chaque ticket, `contexte` ouvre le travail sur un ticket, `bilan` refuse de conclure s'il reste du travail.
4. `contexte` présélectionne les fiches candidates par mots-clés et rappelle les décisions déjà prises sur le ticket, qui s'imposent même en cas de réécriture complète.
5. Un ticket n'est proposé que deux fois par passage. Au-delà, il est laissé à l'humain : le passage ne peut pas tourner en boucle.
6. Les propositions qui renvoient la question (« faire valider », « à confirmer », « sous réserve », « par le responsable ») ou qui contiennent une alternative sont refusées à l'inscription, et `valider` est refusé sur elles.
7. `python analyses.py trancher`, à lancer soi-même dans un terminal, présente chaque décision en attente et l'enregistre au bon format. Les agents ne peuvent pas la lancer.
8. Les écritures dans `decisions.md` et le journal sont protégées : plusieurs sous-agents peuvent travailler en même temps sans perdre de question.

## Installation

1. Dans Fork, commite l'état actuel.
2. Décompresse l'archive à la racine de `Redmine_Automation` en écrasant les fichiers existants.
3. Dans VS Code, vérifie la version (Aide > À propos) : il faut la 1.109 ou plus récente pour les sous-agents.
4. Ouvre le sélecteur d'agents du chat : « Coordinateur tickets » doit y figurer. Les trois autres agents n'y apparaissent pas, c'est voulu.
5. Dans `.github/agents/relecteur-analyse.agent.md`, remplace la ligne `# model: ['Nom exact du modèle']` par le nom exact d'un autre modèle que celui du chat, recopié depuis le sélecteur, sans le `#`. Choisis un modèle de même niveau ou d'un niveau inférieur : sinon le relecteur refuse de démarrer.
6. `.vscode/settings.json` autorise sans confirmation les commandes `python analyses.py`, sauf `trancher`. Si VS Code demande quand même une confirmation à chaque commande, recopie le bloc `chat.tools.terminal.autoApprove` dans tes paramètres utilisateur.

## Premier passage

1. Ajoute dans `decisions.md` une ligne de relecture pour #8765, #8780 et #8787, validés sans réponse, par exemple : `| #8765 | Relecture | — | corriger : maintien en arrière-plan pendant 30 minutes ; couper le Wi-Fi pour provoquer la perte de connexion |  |`.
2. Lance `/analyser-tickets parallele=1`. Garde VS Code ouvert pendant le passage.
3. À la fin, lance `python analyses.py trancher` dans un terminal, puis commite.
4. Relance `/analyser-tickets` pour faire appliquer tes décisions.

## Paramètres de /analyser-tickets

| Paramètre | Effet | Défaut |
|---|---|---|
| `lot=` | Nombre maximal de tickets ouverts pendant le passage | Aucune limite |
| `ticket=` | Un seul ticket, même si son analyse est à jour | — |
| `relecture=` | `passage`, `tout` ou `non` | `passage` |
| `relire=` | Nombre maximal d'analyses relues | 20 |
| `parallele=` | Sous-agents lancés en même temps, de 1 à 3 | 1 |

`/relire-analyses` fait relire les analyses conformes qui ne l'ont jamais été, sans rien analyser.
