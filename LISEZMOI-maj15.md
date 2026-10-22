# Mise à jour 15 — le lot d'un passage ouvert ne change plus

Au passage du 22/10, l'agent a relancé `preparer --lot 1`, puis `--lot 6`, puis `--lot 8` : en élargissant le lot, il contournait la limite du passage.

1. Un passage ouvert depuis moins de 12 h garde son lot. Un autre `--lot` est ignoré avec un message.
2. Pour changer de lot ou repartir de zéro, l'humain lance `python analyses.py preparer --nouveau --lot N`.

Installation : décompresser sur `Redmine_Automation` en écrasant, puis commiter via Fork.
