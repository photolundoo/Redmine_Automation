#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suivi et contrôle des analyses de tickets.

Utilisation (depuis le dossier Redmine_Automation) :
    python analyses.py etat                       tickets à analyser : nouveaux, modifiés depuis leur analyse ou analyse non conforme
    python analyses.py verifier [--ticket N]      contrôle la forme des analyses (toutes, ou celle d'un ticket)
    python analyses.py question --ticket N --question "..." --proposition "..."
                                                  ajoute une question à trancher dans decisions.md
    python analyses.py journal --ticket N --texte "..."
                                                  ajoute une ligne au journal
    python analyses.py synthese                   régénère analyses/<version>/synthese.md
    python analyses.py reparer-decisions          remet decisions.md au format attendu (numéros en #N, colonne « Appliquée le »)
    python analyses.py preparer                   récupère les tickets, convertit les plans, puis affiche l'état
    python analyses.py reprendre --ticket N       archive l'analyse du ticket avant de la refaire entièrement
    python analyses.py appliquer --ticket N       date les décisions appliquées pour ce ticket, après contrôle

Option commune :
    --version ISAP-V27.1   version à traiter ; par défaut, la seule présente dans tickets/

Le script n'utilise que la bibliothèque standard de Python.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
TICKETS = DOSSIER / "tickets"
ANALYSES = DOSSIER / "analyses"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# --------------------------------------------------------------------------
# Référentiel des valeurs contrôlées (identique à la commande /analyser-tickets)
# --------------------------------------------------------------------------

ENVIRONNEMENTS = ["WebApp", "WinApp", "Serveur / grille", "Simulateur", "Matériel", "Mobile", "Aucun"]

VALEURS = {
    "Application": ["WebApp", "WinApp", "Application mobile", "Serveur et services", "Transverse"],
    "Nature du test": ["Nouveau test", "Re-test ciblé", "Non-régression technique",
                       "Configuration d'environnement", "Relecture documentaire", "Hors campagne"],
    "Automatisabilité": ["Automatisable", "Difficile", "Impossible sans script externe",
                         "Hors outillage actuel", "Non applicable"],
    "Confiance": ["Élevée", "Moyenne", "Faible"],
    "Décision humaine requise": ["Oui", "Non"],
}

CHAMPS_OBLIGATOIRES = ["Fonction Redmine", "Application", "Module", "Plan cible", "Fiche cible",
                       "Nature du test", "Automatisabilité", "Environnement", "Prérequis particuliers",
                       "Déjà au plan", "Confiance", "Décision humaine requise"]

SECTIONS = ["## Fiche signalétique", "## 1. Étude du sujet", "## 2. Compte rendu de la situation",
            "## 3. Comparaison avec l'existant", "## 4. Procédure de test proposée",
            "## 5. Intégration proposée", "## Points ouverts", "## Sources"]

SANS_PROCEDURE = ("Relecture documentaire", "Hors campagne")

ENTETE_DECISIONS = """# Décisions à prendre — {version}

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
"""
LIGNE_ENTETE_DECISIONS = "| Ticket | Question | Proposition de l'agent | Décision | Appliquée le |"

MOT_DE_PASSE = re.compile(r"(?i)\b(mot de passe|mdp|password|passwd|pwd)\b\s*[:=]\s*(?!<)[^\s<`]{3,}")
REPERES_NON_REMPLACES = ("<n>", "<version>")


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
# Lecture des analyses et des décisions
# --------------------------------------------------------------------------

def lire_analyse(chemin):
    texte = chemin.read_text(encoding="utf-8")
    entete = re.search(r"<!--\s*ticket:\s*(\d+)\s*\|\s*mis à jour\s*:\s*(\S+)\s*-->", texte)
    titre = re.search(r"^# Analyse #(\d+) — (.+)$", texte, re.MULTILINE)
    champs = {}
    section = re.search(r"## Fiche signalétique\s*\n(.*?)(?:\n## |\Z)", texte, re.DOTALL)
    if section:
        for ligne in section.group(1).splitlines():
            cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
            if len(cellules) >= 2 and cellules[0] not in ("Champ", "") and not set(cellules[0]) <= {"-"}:
                champs[cellules[0]] = cellules[1]
    return {
        "texte": texte,
        "id": int(entete.group(1)) if entete else None,
        "mis_a_jour": entete.group(2) if entete else "",
        "titre": titre.group(2).strip() if titre else "",
        "titre_id": int(titre.group(1)) if titre else None,
        "champs": champs,
    }


def section_de(texte, titre):
    trouve = re.search(re.escape(titre) + r"\s*\n(.*?)(?=\n## |\Z)", texte, re.DOTALL)
    return trouve.group(1) if trouve else ""


def chemin_decisions(version):
    return ANALYSES / version / "decisions.md"


def lire_decisions(version, avec_ecarts=False):
    """Renvoie (conforme, lignes[, écarts]) ; chaque ligne : dict ticket, question, proposition, decision, appliquee."""
    chemin = chemin_decisions(version)
    if not chemin.exists():
        return (True, [], []) if avec_ecarts else (True, [])
    texte = chemin.read_text(encoding="utf-8")
    ecarts = [] if LIGNE_ENTETE_DECISIONS in texte else ["en-tête du tableau attendu : " + LIGNE_ENTETE_DECISIONS]
    lignes = []
    for ligne in texte.splitlines():
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cellules) >= 5 and re.fullmatch(r"#?\d+", cellules[0]):
            numero = int(cellules[0].lstrip("#"))
            if not cellules[0].startswith("#"):
                ecarts.append(f"ligne du ticket {numero} : le numéro doit s'écrire #{numero}")
            if cellules[4] and not re.fullmatch(r"\d{2}/\d{2}/\d{4}", cellules[4]):
                ecarts.append(f"ligne du ticket #{numero} : « Appliquée le » doit être vide ou une date JJ/MM/AAAA (trouvé « {cellules[4]} »)")
            lignes.append({"ticket": numero, "question": cellules[1],
                           "proposition": cellules[2], "decision": cellules[3], "appliquee": cellules[4]})
    conforme = not ecarts
    return (conforme, lignes, ecarts) if avec_ecarts else (conforme, lignes)


FORMES_DECISION = [
    ("valider", r"valider"),
    ("corriger", r"corriger\s*:\s*\S.*"),
    ("fiche", r"fiche\s*:\s*\S.*"),
    ("réanalyser", r"r[ée]analyser"),
    ("hors campagne", r"hors campagne"),
    ("ignorer", r"ignorer"),
]


def forme_decision(texte):
    texte = (texte or "").strip().strip("`").strip()
    for nom, motif in FORMES_DECISION:
        if re.fullmatch(motif, texte, re.IGNORECASE):
            return nom
    return None


def decisions_a_appliquer(decisions):
    """Décisions renseignées, non encore appliquées, réparties en (reconnues, non reconnues)."""
    reconnues, inconnues = [], []
    for d in decisions:
        if d["decision"] and not d["appliquee"]:
            (reconnues if forme_decision(d["decision"]) else inconnues).append(d)
    return reconnues, inconnues


def decisions_en_attente(version):
    return sum(1 for l in lire_decisions(version)[1] if not l["decision"])


def lire_journal(version):
    chemin = ANALYSES / version / "journal.md"
    if not chemin.exists():
        return []
    return [l for l in chemin.read_text(encoding="utf-8").splitlines() if l.startswith("- ")]


def ecarts_journal(version):
    return [f"journal : ligne hors format « {l[:60]} »" for l in lire_journal(version)
            if not re.fullmatch(r"- \d{4}-\d{2}-\d{2} \d{2}:\d{2} — #\d+ — .+", l)]


def normaliser(texte):
    texte = unicodedata.normalize("NFKC", texte or "").replace("’", "'").replace("`", "")
    texte = re.sub(r"[«»\"*_]", " ", texte)
    return re.sub(r"\s+", " ", texte).strip().lower()


def controler_fiche(champs):
    """Vérifie que la fiche cible existe dans le plan cible et que son titre est le bon."""
    plan, fiche = champs.get("Plan cible", ""), champs.get("Fiche cible", "")
    numero_plan = re.match(r"\s*(\d{2})\b", plan)
    identifiant = re.match(r"\s*([A-Z][A-Z_]*\d+[a-z]?)\b", fiche)
    if not numero_plan or not identifiant:
        return []
    fichiers = sorted((DOSSIER / "referentiel" / "plans").glob(numero_plan.group(1) + "*.md"))
    if not fichiers:
        return [f"fiche cible : aucun plan {numero_plan.group(1)} dans referentiel/plans/"]
    texte = fichiers[0].read_text(encoding="utf-8")
    positions = [m.start() for m in re.finditer(rf"\b{re.escape(identifiant.group(1))}\b", texte)]
    if not positions:
        return [f"fiche cible : {identifiant.group(1)} introuvable dans {fichiers[0].name}"]
    titre = re.split(r"\s+[—–-]\s+", fiche, maxsplit=1)
    if len(titre) < 2 or not titre[1].strip():
        return [f"fiche cible : préciser le titre après l'identifiant, par exemple « {identifiant.group(1)} — titre de la fiche »"]
    attendu = normaliser(titre[1])[:40]
    if not any(attendu in normaliser(texte[max(0, p - 400):p + 800]) for p in positions):
        return [f"fiche cible : le titre « {titre[1].strip()} » ne correspond pas à la fiche {identifiant.group(1)} "
                f"de {fichiers[0].name} ; reprendre l'identifiant et le titre tels qu'ils figurent dans le plan"]
    return []


# --------------------------------------------------------------------------
# Contrôle d'une analyse
# --------------------------------------------------------------------------

def verifier_analyse(version, numero, decisions):
    chemin = ANALYSES / version / f"{numero}.md"
    if not chemin.exists():
        return ["analyse absente"]
    erreurs = []
    a = lire_analyse(chemin)
    texte, champs = a["texte"], a["champs"]

    try:
        ticket = lire_ticket(version, numero)
    except (OSError, ValueError, KeyError):
        ticket = None
    if a["id"] != numero:
        erreurs.append("première ligne absente ou incorrecte : attendu <!-- ticket: NUMÉRO | mis à jour : DATE -->")
    elif ticket and a["mis_a_jour"] != ticket["mis_a_jour"]:
        erreurs.append(f"date de mise à jour de l'en-tête différente de ticket.json ({ticket['mis_a_jour']})")
    if a["titre_id"] != numero:
        erreurs.append("titre absent ou incorrect : attendu « # Analyse #NUMÉRO — sujet »")

    for titre in SECTIONS:
        if titre not in texte:
            erreurs.append(f"section manquante : {titre}")

    for nom in CHAMPS_OBLIGATOIRES:
        if not champs.get(nom):
            erreurs.append(f"fiche signalétique : champ « {nom} » absent ou vide")
    for nom, autorisees in VALEURS.items():
        valeur = champs.get(nom)
        if valeur and valeur not in autorisees:
            erreurs.append(f"fiche signalétique : « {nom} » vaut « {valeur} », valeurs autorisées : {' · '.join(autorisees)}")
    if champs.get("Environnement"):
        for partie in re.split(r"\s*\+\s*", champs["Environnement"]):
            if partie not in ENVIRONNEMENTS:
                erreurs.append(f"fiche signalétique : environnement « {partie} » inconnu, valeurs autorisées : {' · '.join(ENVIRONNEMENTS)}")

    parties_env = re.split(r"\s*\+\s*", champs.get("Environnement", ""))
    if champs.get("Environnement") and "WebApp" not in parties_env and \
            champs.get("Automatisabilité") not in ("Hors outillage actuel", "Non applicable"):
        erreurs.append("« Automatisabilité » : sans WebApp dans l'environnement, la valeur doit être « Hors outillage actuel » ou « Non applicable »")

    comparaison = section_de(texte, "## 3. Comparaison avec l'existant")
    if "Recherche dans les plans" not in comparaison:
        erreurs.append("section 3 : le paragraphe « **Recherche dans les plans.** » est absent")
    elif f"#{numero}" not in comparaison:
        erreurs.append(f"section 3 : la recherche de #{numero} dans les plans n'est pas rapportée")
    for plan in re.findall(r"referentiel/plans/(\d{2})", section_de(texte, "## Sources").replace("\\", "/")):
        if not re.search(rf"\b({plan}|{int(plan)})\b", comparaison):
            erreurs.append(f"sources : le plan {plan} est cité mais la section 3 n'en rapporte rien")

    nature = champs.get("Nature du test", "")
    if nature not in SANS_PROCEDURE:
        procedure = section_de(texte, "## 4. Procédure de test proposée")
        etapes = [l for l in procedure.splitlines() if l.strip().startswith("- ")]
        if not etapes:
            erreurs.append("procédure de test : aucune étape (lignes commençant par « - »)")
        elif not any(f"#{numero}" in l for l in etapes):
            erreurs.append(f"procédure de test : les étapes doivent citer le ticket (#{numero})")
        elif not any("Résultat attendu" in l for l in etapes):
            erreurs.append("procédure de test : aucune étape ne précise de « Résultat attendu »")

    if "referentiel/plans/" not in section_de(texte, "## Sources").replace("\\", "/"):
        erreurs.append("sources : aucun plan de referentiel/plans/ cité ; la recherche dans les plans est obligatoire, même sans fiche cible")

    erreurs += controler_fiche(champs)

    lignes_ticket = [d for d in decisions if d["ticket"] == numero]
    for d in lignes_ticket:
        if d["decision"] and not d["appliquee"] and forme_decision(d["decision"]):
            erreurs.append(f"décision « {d['decision']} » non appliquée : l'appliquer à l'analyse, puis lancer python analyses.py appliquer --ticket {numero}")
    en_attente = [d for d in lignes_ticket if not d["decision"]]
    if champs.get("Décision humaine requise") == "Oui" and not lignes_ticket:
        erreurs.append("« Décision humaine requise » vaut Oui mais aucune question n'est inscrite dans decisions.md")
    if champs.get("Décision humaine requise") == "Non" and en_attente:
        erreurs.append("« Décision humaine requise » vaut Non alors qu'une question attend une décision dans decisions.md")

    if not any(re.search(rf"— #{numero} —", l) for l in lire_journal(version)):
        erreurs.append("journal : aucune ligne pour ce ticket (python analyses.py journal)")

    if MOT_DE_PASSE.search(texte):
        erreurs.append("un mot de passe semble recopié : le remplacer par un repère, par exemple <MDP_LOCALADMIN>")
    for repere in REPERES_NON_REMPLACES:
        if repere in texte:
            erreurs.append(f"repère non remplacé : {repere}")
    return erreurs


# --------------------------------------------------------------------------
# Commandes
# --------------------------------------------------------------------------

def etat(version):
    numeros = selection_courante(version)
    dossier_analyses = ANALYSES / version
    conforme, decisions = lire_decisions(version)
    a_faire, a_jour = [], []
    reconnues, inconnues = decisions_a_appliquer(decisions)
    a_appliquer = {d["ticket"]: d for d in reconnues}
    for numero in numeros:
        ticket = lire_ticket(version, numero)
        chemin = dossier_analyses / f"{numero}.md"
        if not chemin.exists():
            a_faire.append((ticket, "nouveau"))
            continue
        if numero in a_appliquer:
            a_faire.append((ticket, f"décision à appliquer : {a_appliquer[numero]['decision']}"))
        elif lire_analyse(chemin)["mis_a_jour"] != ticket["mis_a_jour"]:
            a_faire.append((ticket, "ticket modifié depuis l'analyse"))
        elif verifier_analyse(version, numero, decisions):
            a_faire.append((ticket, "analyse non conforme (voir python analyses.py verifier)"))
        else:
            a_jour.append(ticket)

    orphelines = []
    if dossier_analyses.is_dir():
        for chemin in sorted(dossier_analyses.glob("*.md")):
            if chemin.stem.isdigit() and int(chemin.stem) not in numeros:
                orphelines.append(int(chemin.stem))

    # Décisions à appliquer d'abord, puis analyses à reprendre, puis nouvelles analyses.
    a_faire.sort(key=lambda e: (0 if e[1].startswith("décision") else 2 if e[1] == "nouveau" else 1,
                                e[0]["fonction"].lower(), e[0]["id"]))
    print(f"Version {version} : {len(numeros)} tickets dans la sélection")
    print(f"Analyses à jour : {len(a_jour)} | À analyser : {len(a_faire)} | Décisions en attente : {decisions_en_attente(version)}")
    if not conforme:
        print("ATTENTION : decisions.md n'a pas le format attendu ; lancer python analyses.py reparer-decisions avant de poursuivre.")
    for d in inconnues:
        print(f"Décision non reconnue pour #{d['ticket']} (« {d['decision']} ») : à reformuler par l'humain, ne pas l'appliquer.")
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


def verifier(version, numero=None):
    conforme, decisions, ecarts = lire_decisions(version, avec_ecarts=True)
    total = 0
    for e in ecarts:
        print(f"decisions.md : {e}")
    for e in ecarts_journal(version):
        print(e)
    total += len(ecarts) + len(ecarts_journal(version))
    if ecarts:
        print("  → lancer python analyses.py reparer-decisions")
    for d in decisions_a_appliquer(decisions)[1]:
        print(f"avertissement : décision non reconnue pour #{d['ticket']} (« {d['decision']} »), à reformuler par l'humain")
    if numero:
        numeros = [numero]
    else:
        dossier = ANALYSES / version
        numeros = sorted(int(c.stem) for c in dossier.glob("*.md") if c.stem.isdigit()) if dossier.is_dir() else []
    for n in numeros:
        erreurs = verifier_analyse(version, n, decisions)
        total += len(erreurs)
        if erreurs:
            print(f"#{n} : {len(erreurs)} écart(s)")
            for e in erreurs:
                print(f"  - {e}")
        else:
            print(f"#{n} : conforme")
    print()
    print("Aucun écart." if total == 0 else f"{total} écart(s) à corriger.")
    sys.exit(1 if total else 0)


def nettoyer(texte):
    return re.sub(r"\s+", " ", (texte or "").replace("|", "/")).strip()


def question(version, numero, texte_question, proposition):
    if not texte_question or not proposition:
        sys.exit("Préciser --question et --proposition.")
    chemin = chemin_decisions(version)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    if not chemin.exists():
        chemin.write_text(ENTETE_DECISIONS.format(version=version), encoding="utf-8")
    elif not lire_decisions(version)[0]:
        sys.exit("decisions.md n'a pas le format attendu : lancer python analyses.py reparer-decisions, puis relancer.")
    contenu = chemin.read_text(encoding="utf-8")
    if not contenu.endswith("\n"):
        contenu += "\n"
    contenu += f"| #{numero} | {nettoyer(texte_question)} | {nettoyer(proposition)} |  |  |\n"
    chemin.write_text(contenu, encoding="utf-8")
    print(f"Question ajoutée pour #{numero} dans {chemin}")


def journal(version, numero, texte):
    if not texte:
        sys.exit("Préciser --texte.")
    chemin = ANALYSES / version / "journal.md"
    chemin.parent.mkdir(parents=True, exist_ok=True)
    if not chemin.exists():
        chemin.write_text(f"# Journal des analyses — {version}\n\n", encoding="utf-8")
    with open(chemin, "a", encoding="utf-8") as fichier:
        fichier.write(f"- {datetime.now().strftime('%Y-%m-%d %H:%M')} — #{numero} — {nettoyer(texte)}\n")
    print(f"Journal mis à jour : {chemin}")


def reparer_decisions(version):
    chemin = chemin_decisions(version)
    if not chemin.exists():
        print("decisions.md absent : rien à réparer.")
        return
    _, lignes = lire_decisions(version)
    contenu = ENTETE_DECISIONS.format(version=version)
    for l in lignes:
        appliquee = l["appliquee"] if re.fullmatch(r"\d{2}/\d{2}/\d{4}", l["appliquee"]) else ""
        contenu += (f"| #{l['ticket']} | {nettoyer(l['question'])} | {nettoyer(l['proposition'])} | "
                    f"{nettoyer(l['decision'])} | {appliquee} |\n")
    chemin.write_text(contenu, encoding="utf-8")
    print(f"decisions.md réécrit au format attendu ({len(lignes)} ligne(s) conservée(s), décisions intactes).")


def preparer(version_demandee):
    for script in ("recuperer_tickets.py", "convertir_plans.py"):
        print(f"=== {script} ===")
        resultat = subprocess.run([sys.executable, str(DOSSIER / script)], cwd=DOSSIER)
        if resultat.returncode != 0:
            if script == "recuperer_tickets.py":
                sys.exit(f"Échec de {script} : arrêt, les tickets ne sont pas à jour.")
            print(f"Échec de {script} : poursuite avec les plans déjà convertis.")
        print()
    print("=== état ===")
    etat(choisir_version(version_demandee))


def reprendre(version, numero):
    chemin = ANALYSES / version / f"{numero}.md"
    if not chemin.exists():
        sys.exit(f"Aucune analyse à reprendre pour #{numero}.")
    archives = ANALYSES / version / "archives"
    archives.mkdir(parents=True, exist_ok=True)
    cible = archives / f"{numero}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    shutil.move(str(chemin), str(cible))
    print(f"Analyse de #{numero} archivée dans {cible.relative_to(DOSSIER)}. Rédiger la nouvelle analyse à partir du ticket et des plans, sans relire l'archive.")


def appliquer(version, numero):
    chemin = chemin_decisions(version)
    conforme, decisions = lire_decisions(version)
    if not conforme:
        sys.exit("decisions.md n'a pas le format attendu : lancer python analyses.py reparer-decisions.")
    lignes = [d for d in decisions if d["ticket"] == numero and d["decision"] and not d["appliquee"]
              and forme_decision(d["decision"])]
    if not lignes:
        sys.exit(f"Aucune décision reconnue à appliquer pour #{numero}.")
    analyse = ANALYSES / version / f"{numero}.md"
    if not analyse.exists():
        sys.exit(f"Analyse absente pour #{numero}.")
    champs = lire_analyse(analyse)["champs"]
    for d in lignes:
        forme = forme_decision(d["decision"])
        if forme == "fiche" and champs.get("Fiche cible", "") in ("", "À décider", "Aucune"):
            sys.exit(f"#{numero} : la décision « {d['decision']} » n'est pas reportée dans « Fiche cible ».")
        if forme == "hors campagne" and champs.get("Nature du test") != "Hors campagne":
            sys.exit(f"#{numero} : la décision « hors campagne » n'est pas reportée dans « Nature du test ».")
    # Contrôle de l'analyse, hors écarts liés aux décisions qu'on s'apprête à dater.
    erreurs = [e for e in verifier_analyse(version, numero, [dict(d, appliquee="x") if d in lignes else d for d in decisions])]
    if erreurs:
        print(f"#{numero} : l'analyse n'est pas conforme, décisions non datées :")
        for e in erreurs:
            print(f"  - {e}")
        sys.exit(1)
    aujourdhui = datetime.now().strftime("%d/%m/%Y")
    texte = chemin.read_text(encoding="utf-8")
    sortie = []
    for ligne in texte.splitlines():
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if (len(cellules) >= 5 and cellules[0] == f"#{numero}" and cellules[3] and not cellules[4]
                and forme_decision(cellules[3])):
            ligne = f"| {cellules[0]} | {cellules[1]} | {cellules[2]} | {cellules[3]} | {aujourdhui} |"
        sortie.append(ligne)
    chemin.write_text("\n".join(sortie) + "\n", encoding="utf-8")
    print(f"#{numero} : {len(lignes)} décision(s) datée(s) du {aujourdhui}.")


def rang_environnement(valeur):
    premier = re.split(r"\s*\+\s*", valeur or "Aucun")[0].strip()
    return ENVIRONNEMENTS.index(premier) if premier in ENVIRONNEMENTS else len(ENVIRONNEMENTS)


def cellule(texte):
    return str(texte or "").replace("|", "\\|").strip()


def synthese(version):
    numeros = selection_courante(version)
    dossier_analyses = ANALYSES / version
    _, decisions = lire_decisions(version)
    analyses, manquantes, a_reprendre = [], [], set()
    for numero in numeros:
        ticket = lire_ticket(version, numero)
        chemin = dossier_analyses / f"{numero}.md"
        if not chemin.exists():
            manquantes.append(ticket)
            continue
        analyse = lire_analyse(chemin)
        analyse["ticket"] = ticket
        if analyse["mis_a_jour"] != ticket["mis_a_jour"] or verifier_analyse(version, numero, decisions):
            a_reprendre.add(numero)
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
        f"- Analysés : {len(analyses)} (dont {len(a_reprendre)} à reprendre : ticket modifié ou analyse non conforme)",
        f"- Non analysés : {len(manquantes)}",
        f"- Décisions en attente dans `decisions.md` : {decisions_en_attente(version)}",
    ]

    for nom in ("Nature du test", "Environnement", "Automatisabilité"):
        compte = Counter(champ(a, nom) or "(non renseigné)" for a in analyses)
        lignes += ["", f"## Répartition — {nom}", "", f"| {nom} | Tickets |", "|---|---|"]
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
        marque = " (à reprendre)" if t["id"] in a_reprendre else ""
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
    analyseur = argparse.ArgumentParser(description="Suivi et contrôle des analyses de tickets.")
    analyseur.add_argument("commande", choices=["etat", "verifier", "question", "journal", "synthese", "reparer-decisions",
                                                "preparer", "reprendre", "appliquer"])
    analyseur.add_argument("--version", help="version à traiter (ex. ISAP-V27.1)")
    analyseur.add_argument("--ticket", type=int, help="numéro du ticket")
    analyseur.add_argument("--question", help="question à trancher (commande question)")
    analyseur.add_argument("--proposition", help="proposition de l'agent (commande question)")
    analyseur.add_argument("--texte", help="texte de la ligne de journal (commande journal)")
    args = analyseur.parse_args()
    if args.commande == "preparer":
        preparer(args.version)
        return
    version = choisir_version(args.version)

    if args.commande in ("question", "journal", "reprendre", "appliquer") and not args.ticket:
        sys.exit("Préciser --ticket.")
    if args.commande == "etat":
        etat(version)
    elif args.commande == "verifier":
        verifier(version, args.ticket)
    elif args.commande == "question":
        question(version, args.ticket, args.question, args.proposition)
    elif args.commande == "journal":
        journal(version, args.ticket, args.texte)
    elif args.commande == "reprendre":
        reprendre(version, args.ticket)
    elif args.commande == "appliquer":
        appliquer(version, args.ticket)
    elif args.commande == "reparer-decisions":
        reparer_decisions(version)
    else:
        synthese(version)


if __name__ == "__main__":
    main()
