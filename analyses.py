#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suivi des analyses de tickets.

Utilisation (depuis le dossier Redmine_Automation) :
    python analyses.py etat        liste les tickets à analyser (nouveaux ou modifiés depuis leur analyse)
    python analyses.py synthese    régénère analyses/<version>/synthese.md à partir des analyses

Option commune :
    --version ISAP-V27.1   version à traiter ; par défaut, la seule présente dans tickets/

Le script n'utilise que la bibliothèque standard de Python.
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
TICKETS = DOSSIER / "tickets"
ANALYSES = DOSSIER / "analyses"

ORDRE_ENVIRONNEMENT = ["WebApp", "WinApp", "Serveur / grille", "Simulateur", "Matériel", "Mobile", "Aucun"]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# --------------------------------------------------------------------------
# Lecture des tickets
# --------------------------------------------------------------------------

def choisir_version(version):
    if version:
        if not (TICKETS / version).is_dir():
            sys.exit(f"Version introuvable : tickets/{version}")
        return version
    versions = sorted(d.name for d in TICKETS.iterdir() if d.is_dir()) if TICKETS.is_dir() else []
    if len(versions) != 1:
        sys.exit("Préciser la version avec --version (versions présentes : " + (", ".join(versions) or "aucune") + ").")
    return versions[0]


def selection_courante(version):
    """Numéros des tickets de la sélection, lus dans tickets/<version>/index.md (hors tickets sortis)."""
    index = TICKETS / version / "index.md"
    if not index.exists():
        sys.exit(f"Index introuvable : {index}. Lancer d'abord recuperer_tickets.py.")
    numeros = []
    for ligne in index.read_text(encoding="utf-8").splitlines():
        if ligne.startswith("## "):
            break
        trouve = re.match(r"\|\s*\[#(\d+)\]", ligne)
        if trouve:
            numeros.append(int(trouve.group(1)))
    return numeros


def lire_ticket(version, numero):
    chemin = TICKETS / version / str(numero) / "ticket.json"
    ticket = json.loads(chemin.read_text(encoding="utf-8"))["issue"]
    fonction = ""
    for champ in ticket.get("custom_fields", []):
        if champ.get("name") == "Fonction":
            fonction = champ.get("value") or ""
    return {
        "id": numero,
        "sujet": ticket.get("subject", ""),
        "fonction": fonction,
        "tracker": (ticket.get("tracker") or {}).get("name", ""),
        "mis_a_jour": ticket.get("updated_on", ""),
    }


# --------------------------------------------------------------------------
# Lecture des analyses
# --------------------------------------------------------------------------

def lire_analyse(chemin):
    texte = chemin.read_text(encoding="utf-8")
    entete = re.search(r"<!--\s*ticket:\s*(\d+)\s*\|\s*mis à jour\s*:\s*(\S+)\s*-->", texte)
    titre = re.search(r"^# Analyse #\d+ — (.+)$", texte, re.MULTILINE)
    champs = {}
    section = re.search(r"## Fiche signalétique\s*\n(.*?)(?:\n## |\Z)", texte, re.DOTALL)
    if section:
        for ligne in section.group(1).splitlines():
            cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
            if len(cellules) >= 2 and cellules[0] not in ("Champ", "") and not set(cellules[0]) <= {"-"}:
                champs[cellules[0]] = cellules[1]
    return {
        "id": int(entete.group(1)) if entete else None,
        "mis_a_jour": entete.group(2) if entete else "",
        "titre": titre.group(1).strip() if titre else "",
        "champs": champs,
    }


def decisions_en_attente(version):
    chemin = ANALYSES / version / "decisions.md"
    if not chemin.exists():
        return 0
    attente = 0
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cellules) >= 5 and re.fullmatch(r"#?\d+", cellules[0]) and not cellules[3]:
            attente += 1
    return attente


# --------------------------------------------------------------------------
# Commandes
# --------------------------------------------------------------------------

def etat(version):
    numeros = selection_courante(version)
    dossier_analyses = ANALYSES / version
    a_faire, a_jour = [], []
    for numero in numeros:
        ticket = lire_ticket(version, numero)
        chemin = dossier_analyses / f"{numero}.md"
        if not chemin.exists():
            a_faire.append((ticket, "nouveau"))
            continue
        analyse = lire_analyse(chemin)
        if analyse["mis_a_jour"] != ticket["mis_a_jour"]:
            a_faire.append((ticket, "ticket modifié depuis l'analyse"))
        else:
            a_jour.append(ticket)

    orphelines = []
    if dossier_analyses.is_dir():
        for chemin in sorted(dossier_analyses.glob("*.md")):
            if chemin.stem.isdigit() and int(chemin.stem) not in numeros:
                orphelines.append(int(chemin.stem))

    a_faire.sort(key=lambda e: (e[0]["fonction"].lower(), e[0]["id"]))
    print(f"Version {version} : {len(numeros)} tickets dans la sélection")
    print(f"Analyses à jour : {len(a_jour)} | À analyser : {len(a_faire)} | Décisions en attente : {decisions_en_attente(version)}")
    print()
    if a_faire:
        print("À analyser, dans cet ordre (numéro | Fonction | motif | sujet) :")
        for ticket, motif in a_faire:
            print(f"  {ticket['id']} | {ticket['fonction'] or '(vide)'} | {motif} | {ticket['sujet']}")
    else:
        print("Toutes les analyses sont à jour.")
    if orphelines:
        print()
        print("Analyses de tickets sortis de la sélection (conservées) : " + ", ".join(f"#{n}" for n in orphelines))


def rang_environnement(valeur):
    premier = re.split(r"\s*[+,;/]\s*|\s+et\s+", valeur or "Aucun")[0].strip()
    for rang, nom in enumerate(ORDRE_ENVIRONNEMENT):
        if premier.lower().startswith(nom.split(" ")[0].lower()):
            return rang
    return len(ORDRE_ENVIRONNEMENT)


def cellule(texte):
    return str(texte or "").replace("|", "\\|").strip()


def synthese(version):
    numeros = selection_courante(version)
    dossier_analyses = ANALYSES / version
    analyses, manquantes, perimees = [], [], []
    for numero in numeros:
        ticket = lire_ticket(version, numero)
        chemin = dossier_analyses / f"{numero}.md"
        if not chemin.exists():
            manquantes.append(ticket)
            continue
        analyse = lire_analyse(chemin)
        analyse["ticket"] = ticket
        if analyse["mis_a_jour"] != ticket["mis_a_jour"]:
            perimees.append(ticket)
        analyses.append(analyse)

    def champ(a, nom):
        return a["champs"].get(nom, "")

    analyses.sort(key=lambda a: (rang_environnement(champ(a, "Environnement")), champ(a, "Plan cible"),
                                 champ(a, "Fiche cible"), a["ticket"]["id"]))

    lignes = [
        f"# Synthèse des analyses — {version}",
        "",
        f"Générée le {datetime.now().strftime('%d/%m/%Y %H:%M')} par `python analyses.py synthese`. "
        "Ne pas modifier à la main : le fichier est régénéré à chaque passage.",
        "",
        f"- Tickets dans la sélection : {len(numeros)}",
        f"- Analysés : {len(analyses)} (dont {len(perimees)} à reprendre, ticket modifié depuis)",
        f"- Non analysés : {len(manquantes)}",
        f"- Décisions en attente dans `decisions.md` : {decisions_en_attente(version)}",
    ]

    for titre, nom in (("Nature du test", "Nature du test"), ("Environnement", "Environnement"),
                       ("Automatisabilité", "Automatisabilité")):
        compte = Counter(champ(a, nom) or "(non renseigné)" for a in analyses)
        lignes += ["", f"## Répartition — {titre}", "", f"| {titre} | Tickets |", "|---|---|"]
        lignes += [f"| {cellule(valeur)} | {nombre} |" for valeur, nombre in compte.most_common()]

    lignes += [
        "",
        "## Ordre de campagne",
        "",
        "Tickets regroupés par environnement, puis par plan et par fiche, pour limiter les changements de configuration.",
        "",
        "| Ticket | Sujet | Environnement | Plan | Fiche | Nature | Automatisabilité | Décision requise |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for a in analyses:
        t = a["ticket"]
        marque = " (à reprendre)" if t in perimees else ""
        lignes.append(
            f"| [#{t['id']}]({t['id']}.md){marque} | {cellule(t['sujet'])} | {cellule(champ(a, 'Environnement'))} | "
            f"{cellule(champ(a, 'Plan cible'))} | {cellule(champ(a, 'Fiche cible'))} | {cellule(champ(a, 'Nature du test'))} | "
            f"{cellule(champ(a, 'Automatisabilité'))} | {cellule(champ(a, 'Décision humaine requise'))} |"
        )

    if manquantes:
        lignes += ["", "## Tickets non encore analysés", ""]
        lignes += [f"- #{t['id']} — {t['fonction'] or '(Fonction vide)'} — {t['sujet']}" for t in manquantes]

    dossier_analyses.mkdir(parents=True, exist_ok=True)
    cible = dossier_analyses / "synthese.md"
    cible.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"Synthèse écrite : {cible} ({len(analyses)} analyses, {len(manquantes)} tickets non analysés)")


def main():
    analyseur = argparse.ArgumentParser(description="Suivi des analyses de tickets.")
    analyseur.add_argument("commande", choices=["etat", "synthese"])
    analyseur.add_argument("--version", help="version à traiter (ex. ISAP-V27.1)")
    args = analyseur.parse_args()
    version = choisir_version(args.version)
    if args.commande == "etat":
        etat(version)
    else:
        synthese(version)


if __name__ == "__main__":
    main()
