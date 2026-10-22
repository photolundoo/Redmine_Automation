---
description: Passage complet sur les tickets de la version — décisions appliquées, analyses, relecture, bilan
agent: Coordinateur tickets
---

Conduis un passage complet avec les paramètres donnés à la suite de la commande (`lot=`, `ticket=`, `relecture=`, `relire=`, `parallele=`). Sans paramètre, utilise les valeurs par défaut.

## Si tu es le Coordinateur tickets avec l'outil de sous-agents

Lis et suis `.github/agents/coordinateur-tickets.agent.md` à la lettre.

## Sinon : mode direct (un seul agent, sans sous-agents)

Cette partie s'applique dès que le Coordinateur tickets n'est pas l'agent actif ou que tu n'as pas d'outil de sous-agents. Tu fais alors toi-même le travail des trois sous-agents, un ticket à la fois, avec la même discipline.

1. Lis d'abord `.github/copilot-instructions.md`, puis `.github/agents/coordinateur-tickets.agent.md` (déroulé et paramètres), puis le fichier du sous-agent correspondant au mode de chaque ticket : `analyste-ticket.agent.md` (modes `analyser` et `reprendre`), `applicateur-decision.agent.md` (mode `appliquer`), `relecteur-analyse.agent.md` (relecture). Ces fichiers sont ta procédure : ne l'improvise pas.
2. Lance `python analyses.py preparer` UNE SEULE FOIS, au début, avec `--lot <lot>` seulement si le paramètre est donné. Ne le relance jamais ensuite, ni avant un ticket ni après une erreur.
3. Lance `python analyses.py prochain`. Traite uniquement les tickets listés, dans l'ordre. Pour chaque ticket : `python analyses.py contexte --ticket <n>`, puis la procédure du mode, puis `verifier --ticket <n>` et `journal`.
4. N'ouvre pas un ticket, une analyse ou un plan avant `contexte` sur ce ticket. Ne lis jamais `analyses.py`. Ne filtre jamais la sortie d'une commande.
5. Ne lance jamais `python analyses.py trancher` ni `preparer --nouveau`, et n'en simule pas l'effet (pas de tube, pas de boîte de dialogue « Ask User » pour décider à la place de l'humain). Une décision en attente reste en attente : écris l'analyse sans l'avoir tranchée seulement si la procédure du mode le prévoit, et signale-le dans la ligne de fin.
6. Quand `prochain` ne liste plus rien, fais la relecture (`prochain --relecture`) sauf `relecture=non`, puis `python analyses.py bilan`.
7. Termine par le message de fin décrit dans le fichier du Coordinateur, sans conclure « terminé » s'il reste des décisions en attente.
