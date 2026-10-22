# Mise à jour 13 — correctifs après le premier passage réel

1. `preparer` ne remet plus les compteurs à zéro : relancé dans les 12 h, il poursuit le passage ouvert (essais, tickets ouverts, relectures conservés). Le plafond de deux essais par ticket tient donc même si l'agent relance `preparer`. Un nouveau passage s'ouvre après 12 h, ou à ta demande avec `python analyses.py preparer --nouveau` (réservé à l'humain, confirmation exigée par VS Code).
2. Les consignes interdisent aux agents `preparer --nouveau`, comme `trancher`.
3. `verifier --tout` est accepté (sans ticket, `verifier` contrôle déjà toutes les analyses).

## Installation
Décompresse l'archive à la racine de `Redmine_Automation` en écrasant les fichiers existants, puis commite via Fork.

## Si le Coordinateur n'est pas utilisé
Dans le chat, choisis « Coordinateur tickets » dans le sélecteur d'agents (ou lance `/analyser-tickets`) ; l'agent par défaut du chat travaille seul, sans sous-agents.
