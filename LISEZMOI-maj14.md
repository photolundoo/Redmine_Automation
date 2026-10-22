# Mise à jour 14 — mode direct quand les sous-agents ne sont pas disponibles

Le journal du premier passage réel montre un agent unique, sans sous-agent : les prompts renvoyaient à « tes instructions », que cet agent n'avait pas chargées, et il improvisait (`preparer` avant chaque ticket, lecture des tickets, boîte « Ask User » à la place de `trancher`).

1. `/analyser-tickets` et `/relire-analyses` sont désormais autonomes. Avec le Coordinateur et l'outil de sous-agents, ils suivent le Coordinateur. Sinon, en mode direct, l'agent lit les fichiers de procédure, lance `preparer` une seule fois, puis traite les tickets de `prochain` un par un.
2. Le mode direct interdit `trancher`, `preparer --nouveau`, les tubes et toute décision simulée dans une boîte de dialogue.
3. Installation : décompresser sur `Redmine_Automation` en écrasant (avec la maj13 déjà installée), puis commiter via Fork.
