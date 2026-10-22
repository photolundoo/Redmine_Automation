#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suivi et contrôle des analyses de tickets.

Utilisation (depuis le dossier Redmine_Automation) :

  Passage des agents
    python analyses.py preparer [--lot N]         récupère les tickets, convertit les plans, ouvre le passage (sans limite par défaut) ;
                                                  un passage de moins de 12 h est poursuivi, compteurs conservés
    python analyses.py preparer --nouveau         ouvre un nouveau passage malgré tout (humain seulement)
    python analyses.py prochain [--ticket N]      tickets à confier aux agents, avec leur mode : appliquer, reprendre ou analyser
    python analyses.py prochain --relecture [--tout]
                                                  analyses conformes à faire relire (celles du passage, ou toutes)
    python analyses.py contexte --ticket N [--relecture]
                                                  ouvre le travail sur un ticket et affiche son contexte : décisions,
                                                  correspondance, occurrences de #N, fiches candidates
    python analyses.py relecture --ticket N (--texte "..." | --aucune)
                                                  inscrit une remarque de relecture dans decisions.md, ou note qu'il n'y en a pas
    python analyses.py bilan                      contrôle de fin de passage, synthèse et export

  Travail sur un ticket (après contexte)
    python analyses.py question --ticket N --question "..." --proposition "..."
                                                  ajoute une question à trancher dans decisions.md
    python analyses.py journal --ticket N --texte "..."
                                                  ajoute une ligne au journal
    python analyses.py reprendre --ticket N       archive l'analyse du ticket avant de la refaire entièrement
    python analyses.py appliquer --ticket N       date les décisions appliquées pour ce ticket, après contrôle
    python analyses.py verifier [--ticket N]      contrôle la forme des analyses (toutes, ou celle d'un ticket)

  Réservé à l'humain
    python analyses.py trancher [--ticket N]      parcourt les décisions en attente et les enregistre, choix par choix

  Divers
    python analyses.py etat [--max N]             état de la sélection et file de travail
    python analyses.py synthese                   régénère analyses/<version>/synthese.md
    python analyses.py exporter                   écrit export/<version>/campagne.json pour le projet de campagne Playwright
    python analyses.py couverture [--depuis F]    lit le projet Playwright (PLAYWRIGHT_DIR du .env) ou un rapport, écrit referentiel/couverture-playwright.*
    python analyses.py reparer-decisions          remet decisions.md au format attendu (numéros en #N, colonne « Appliquée le »)

Fichiers techniques tenus par le script (ne pas modifier) :
    analyses/<version>/.preparation     passage en cours : date, lot, tickets ouverts, essais par ticket, relectures
    analyses/<version>/.reprises.json   analyses signalées à reprendre entièrement
    analyses/<version>/.relectures.json empreinte de chaque analyse au moment de sa dernière relecture
    analyses/<version>/.verrou          présent seulement pendant une écriture

Option commune :
    --version ISAP-V27.1   version à traiter ; par défaut, la seule présente dans tickets/

Le script n'utilise que la bibliothèque standard de Python.
"""

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from collections import Counter
from contextlib import contextmanager
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
    "Issue": ["A — Reproduire l'existant", "B — Adapter l'existant", "C — Nouvelle procédure automatisable",
              "D — Nouvelle procédure manuelle", "Sans objet"],
}

AUTOMATISABLES = ("Automatisable", "Difficile")
TYPES_PLAYWRIGHT = ("@lecture", "@ecriture", "@perturbateur")
CHAMPS_PLAYWRIGHT = ["Type", "Compte", "Dossier", "Référentiel", "Données créées"]

CHAMPS_OBLIGATOIRES = ["Fonction Redmine", "Application", "Module", "Plan cible", "Fiche cible",
                       "Nature du test", "Automatisabilité", "Environnement", "Prérequis particuliers",
                       "Issue", "Confiance", "Décision humaine requise"]

SECTIONS = ["## Fiche signalétique", "## 1. Étude du sujet", "## 2. Compte rendu de la situation",
            "## 3. Comparaison avec l'existant", "## 4. Procédure de test proposée",
            "## 5. Intégration proposée", "## Points ouverts", "## Sources"]

SANS_PROCEDURE = ("Relecture documentaire", "Hors campagne")

ENTETE_DECISIONS = """# Décisions à prendre — {version}

Le plus simple : lancer `python analyses.py trancher` dans un terminal, qui présente chaque question et enregistre la réponse.

Sinon, remplir la colonne « Décision » avec l'une des formes suivantes, puis relancer `/analyser-tickets` :
- `valider` (ou `validé`, `approuvé`) : la proposition de l'agent est retenue telle quelle. Sans effet si la proposition contient une alternative (« ou », « soit », « à défaut ») ou renvoie la question à quelqu'un (« faire valider », « à confirmer », « sous réserve ») : répondre alors avec `corriger :`, `fiche :` ou `nouveau plan :` ;
- `corriger :` suivi de la correction, par exemple `corriger : la procédure doit aussi couvrir le mode Rejeu` ;
- `fiche :` suivi de la fiche à retenir, par exemple `fiche : MC02 Onglet Main Courante` ;
- `nouveau plan :` suivi de l'intitulé du plan à créer, par exemple `nouveau plan : Installation serveur` ;
- `réanalyser`, éventuellement suivi de `:` et d'une consigne : l'agent refait l'analyse complète du ticket ;
- `hors campagne` : le ticket n'est pas testé dans cette campagne ;
- `ignorer` : la question est sans objet.

Toute autre formulation (« OK », « Nouveau Plan » sans intitulé, texte libre…) n'est pas appliquée : elle reste en attente jusqu'à reformulation.

Pour une remarque de relecture sur un ticket sans question, ajouter une ligne : `| #9006 | Relecture | — | corriger : … |  |`.
Les lignes « Relecture » dont la proposition est remplie viennent de l'agent relecteur : `valider` fait appliquer sa remarque telle quelle.

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
    ("valider", r"valid(?:er|é|ée|e)|approuv(?:er|é|ée)"),
    ("corriger", r"corriger\s*:\s*\S.*"),
    ("fiche", r"fiche\s*:\s*\S.*"),
    ("nouveau plan", r"nouveau plan\s*:\s*\S.*"),
    ("réanalyser", r"r[ée]analyser(?:\s*:\s*\S.*)?"),
    ("hors campagne", r"hors campagne"),
    ("ignorer", r"ignorer"),
]

ALTERNATIVE = re.compile(r"(?i)\b(ou|soit|à défaut|a defaut|sinon)\b")

# Proposition qui renvoie la question à quelqu'un d'autre au lieu d'y répondre.
RENVOI = re.compile(
    r"(?i)\bfaire (valider|préciser|preciser|confirmer|vérifier|verifier|trancher)\b"
    r"|\bà (confirmer|préciser|preciser|valider|convenir|définir|definir)\b"
    r"|\bsous réserve\b|\bjusqu'(?:à|a) (confirmation|précision|validation|réponse)\b"
    r"|\b(confirmer|préciser) (ce|cet|cette|ces|le|la|les|l'|si)\b"
    r"|\b(par|du|au|le) responsable\b|\btant que\b"
    r"|\bsans (précision|confirmation|validation)\b|\bavant de (fixer|finaliser|qualifier)\b")

SANS_PROPOSITION = ("", "—", "-", "–")


def renvoie_la_question(texte):
    return bool(RENVOI.search((texte or "").replace("’", "'")))


def est_relecture(d):
    return normaliser(d.get("question", "")) == "relecture"


def forme_decision(texte):
    texte = (texte or "").strip().strip("`").strip()
    for nom, motif in FORMES_DECISION:
        if re.fullmatch(motif, texte, re.IGNORECASE):
            return nom
    return None


def raison_proposition_invalidable(proposition):
    """None si « valider » peut retenir la proposition telle quelle, sinon pourquoi."""
    proposition = (proposition or "").strip()
    if proposition in SANS_PROPOSITION:
        return "aucune proposition à valider : répondre par « corriger : … »"
    if ALTERNATIVE.search(proposition):
        return "la proposition contient une alternative : répondre par « corriger : … », « fiche : … » ou « nouveau plan : … »"
    if renvoie_la_question(proposition):
        return ("la proposition renvoie la question (« faire valider », « à confirmer », « sous réserve »…) sans y répondre : "
                "donner la réponse avec « corriger : … », ou « ignorer »")
    return None


def refus_decision(d):
    """None si la décision peut être appliquée, sinon la raison pour laquelle l'humain doit la reformuler."""
    forme = forme_decision(d["decision"])
    if not forme:
        return "formulation non reconnue"
    if forme == "valider":
        raison = raison_proposition_invalidable(d["proposition"])
        if raison:
            return "« valider » refusé : " + raison
    return None


def applicable(d):
    return bool(d["decision"]) and not d["appliquee"] and refus_decision(d) is None


def decisions_a_appliquer(decisions):
    """Décisions renseignées, non encore appliquées, réparties en (applicables, à reformuler par l'humain)."""
    reconnues, inconnues = [], []
    for d in decisions:
        if d["decision"] and not d["appliquee"]:
            (reconnues if refus_decision(d) is None else inconnues).append(d)
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
    texte = re.sub(r"\s*[—–]\s*|\s+-\s+", " — ", texte)
    return re.sub(r"\s+", " ", texte).strip().lower()


MOTIF_ID = r"[A-Z][A-Z_]*\d+[a-z]?"
FICHES_SANS_CIBLE = ("À décider", "Aucune")


def fiche_sans_cible(fiche):
    return fiche in FICHES_SANS_CIBLE or fiche.startswith("À créer")


def fichier_plan(plan):
    numero_plan = re.match(r"\s*(\d{2})\b", plan or "")
    if not numero_plan:
        return None, None
    fichiers = sorted((DOSSIER / "referentiel" / "plans").glob(numero_plan.group(1) + "*.md"))
    return numero_plan.group(1), (fichiers[0] if fichiers else None)


def identifiants_du_plan(texte):
    """Identifiants de fiches déclarés dans le plan (« ID : XXX » ou « [XXX] »)."""
    return set(re.findall(rf"ID\s*:\s*({MOTIF_ID})\b", texte)) | set(re.findall(rf"\[({MOTIF_ID})\]", texte))


def controler_fiche(champs):
    """Vérifie que la fiche cible existe dans le plan cible et que son titre est le bon."""
    plan, fiche = champs.get("Plan cible", ""), champs.get("Fiche cible", "")
    if not fiche or fiche_sans_cible(fiche):
        return []
    numero_plan, fichier = fichier_plan(plan)
    if not numero_plan:
        return [f"fiche cible « {fiche} » sans plan cible numéroté : indiquer le plan (par exemple « 13 Outils externes »), "
                "ou mettre « À décider », « À créer » ou « Aucune »"]
    if not fichier:
        return [f"fiche cible : aucun plan {numero_plan} dans referentiel/plans/"]
    texte = fichier.read_text(encoding="utf-8")
    identifiant = re.match(rf"\s*({MOTIF_ID})\b", fiche)
    if not identifiant:
        # Fiche sans identifiant : son titre doit être un titre ou un sous-titre du plan.
        titres = [normaliser(m) for m in re.findall(r"(?m)^#+\s+(.+)$", texte) + re.findall(r"(?m)^\*\*(.+?)\*\*\s*$", texte)]
        if not any(normaliser(fiche) == t or normaliser(fiche) in t for t in titres):
            return [f"fiche cible : « {fiche} » n'est ni un identifiant ni un titre de section de {fichier.name} ; "
                    "reprendre l'identifiant et le titre, ou le titre de section, tels qu'ils figurent dans le plan"]
        return []
    positions = [m.start() for m in re.finditer(rf"\b{re.escape(identifiant.group(1))}\b", texte)]
    if not positions:
        return [f"fiche cible : {identifiant.group(1)} introuvable dans {fichier.name}"]
    titre = re.split(r"\s+[—–-]\s+", fiche, maxsplit=1)
    if len(titre) < 2 or not titre[1].strip():
        return [f"fiche cible : préciser le titre après l'identifiant, par exemple « {identifiant.group(1)} — titre de la fiche »"]
    # Plan structuré en « ID : … Titre : … » : le couple identifiant-titre doit y figurer tel quel.
    couples = fiches_du_plan(numero_plan)
    if couples:
        memes = [f for f in couples if f["identifiant"] == identifiant.group(1)]
        if memes and not any(normaliser(f["titre"]) == normaliser(titre[1]) for f in memes):
            return [f"fiche cible : le plan {numero_plan} ne contient pas « {identifiant.group(1)} — {titre[1].strip()} » ; "
                    f"titre(s) de {identifiant.group(1)} dans le plan : "
                    + " ; ".join(f"« {f['titre']} »" for f in memes)]
        if memes:
            return []
    attendu = normaliser(titre[1])[:40]
    if not any(attendu in normaliser(texte[max(0, p - 400):p + 800]) for p in positions):
        return [f"fiche cible : le titre « {titre[1].strip()} » ne correspond pas à la fiche {identifiant.group(1)} "
                f"de {fichier.name} ; reprendre l'identifiant et le titre tels qu'ils figurent dans le plan"]
    return []


VERBES_INTEGRATION = re.compile(r"(?i)compl[eèé]t|ajout|int[eèé]gr|rattach")


def controler_coherence_fiche(texte, champs):
    """La fiche cible de la fiche signalétique est celle que désignent les sections 3 et 5."""
    fiche = champs.get("Fiche cible", "")
    if not fiche or fiche_sans_cible(fiche):
        return []
    erreurs = []
    integration = section_de(texte, "## 5. Intégration proposée")
    if normaliser(fiche) not in normaliser(integration):
        erreurs.append(f"section 5 : la fiche cible « {fiche} » n'y est pas désignée telle quelle ; "
                       "la section 5 doit nommer la même fiche que la fiche signalétique")
    _, fichier = fichier_plan(champs.get("Plan cible", ""))
    if not fichier:
        return erreurs
    identifiant = re.match(rf"\s*({MOTIF_ID})\b", fiche)
    autres = identifiants_du_plan(fichier.read_text(encoding="utf-8")) - {identifiant.group(1) if identifiant else None}
    for autre in sorted(autres):
        if re.search(rf"\b{autre}\b", integration):
            erreurs.append(f"section 5 : la fiche {autre} est citée alors que la fiche cible est « {fiche} »")
        for phrase in re.split(r"(?<=[.!?])\s+", section_de(texte, "## 3. Comparaison avec l'existant")):
            if re.search(rf"\b{autre}\b", phrase) and VERBES_INTEGRATION.search(phrase):
                erreurs.append(f"section 3 : la phrase « {phrase.strip()[:90]} » rattache le ticket à {autre}, "
                               f"alors que la fiche cible est « {fiche} »")
    return erreurs


def paragraphes_redondants(section):
    """Paires de paragraphes qui disent pour l'essentiel la même chose."""
    paragraphes = [p.strip() for p in re.split(r"\n\s*\n", section) if p.strip()]
    mots = [set(re.findall(r"\w{4,}", normaliser(p))) for p in paragraphes]
    doublons = []
    for i in range(len(paragraphes)):
        for j in range(i + 1, len(paragraphes)):
            a, b = mots[i], mots[j]
            if min(len(a), len(b)) >= 10 and len(a & b) / min(len(a), len(b)) >= 0.7:
                doublons.append((i + 1, j + 1))
    return doublons


# --------------------------------------------------------------------------
# Fichiers techniques : préparation et reprises
# --------------------------------------------------------------------------

DUREE_PREPARATION_H = 12
ESSAIS_MAX = 2

_PROFONDEUR_VERROU = [0]


@contextmanager
def verrou(version):
    """Écriture exclusive des fichiers partagés (decisions.md, journal, fichiers techniques).

    Plusieurs agents peuvent travailler en même temps : sans verrou, deux écritures simultanées de
    decisions.md feraient perdre une question. Le verrou est réentrant dans un même processus.
    """
    if _PROFONDEUR_VERROU[0]:
        _PROFONDEUR_VERROU[0] += 1
        try:
            yield
        finally:
            _PROFONDEUR_VERROU[0] -= 1
        return
    chemin = ANALYSES / version / ".verrou"
    chemin.parent.mkdir(parents=True, exist_ok=True)
    debut = time.time()
    while True:
        try:
            os.close(os.open(str(chemin), os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            break
        except (FileExistsError, PermissionError):
            try:
                if time.time() - chemin.stat().st_mtime > 120:      # verrou laissé par une commande interrompue
                    chemin.unlink()
                    continue
            except OSError:
                pass
            if time.time() - debut > 30:
                sys.exit("Fichiers d'analyse verrouillés par une autre commande depuis plus de 30 s : relancer la commande.")
            time.sleep(0.2)
    _PROFONDEUR_VERROU[0] = 1
    try:
        yield
    finally:
        _PROFONDEUR_VERROU[0] = 0
        try:
            chemin.unlink()
        except OSError:
            pass


def chemin_preparation(version):
    return ANALYSES / version / ".preparation"


def lire_preparation(version):
    """Passage en cours, ou None.

    date : ouverture du passage ; lot : nombre maximal de tickets (0 = sans limite, None = ancien format) ;
    tickets : tickets ouverts par contexte ; essais : nombre d'ouvertures par ticket ; modes : mode de chaque ticket ;
    relus : tickets ouverts en relecture ; force : ticket demandé explicitement (paramètre ticket=).
    """
    try:
        brut = chemin_preparation(version).read_text(encoding="utf-8").strip()
    except OSError:
        return None
    vide = {"tickets": [], "essais": {}, "modes": {}, "relus": [], "force": None}
    try:
        donnees = json.loads(brut)
        preparation = dict(vide, date=datetime.fromisoformat(donnees["date"]), lot=donnees.get("lot"))
        for cle in vide:
            if cle in donnees:
                preparation[cle] = donnees[cle]
        return preparation
    except (ValueError, KeyError, TypeError):
        try:
            return dict(vide, date=datetime.fromisoformat(brut), lot=None)
        except ValueError:
            return None


def ecrire_preparation(version, preparation):
    chemin = chemin_preparation(version)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    donnees = {k: v for k, v in preparation.items() if k != "date"}
    donnees["date"] = preparation["date"].isoformat(timespec="seconds")
    chemin.write_text(json.dumps(donnees, ensure_ascii=False), encoding="utf-8")


def preparation_valide(version):
    """Passage en cours ; arrêt si la préparation est absente ou ancienne."""
    preparation = lire_preparation(version)
    if not preparation or (datetime.now() - preparation["date"]).total_seconds() > DUREE_PREPARATION_H * 3600:
        sys.exit(f"Préparation absente ou datant de plus de {DUREE_PREPARATION_H} h : "
                 "lancer d'abord python analyses.py preparer, puis reprendre.")
    if preparation["lot"] is None:
        sys.exit("Préparation à l'ancien format : relancer python analyses.py preparer.")
    return preparation


def exiger_preparation(version, numero=None):
    """Refuse si la préparation est absente ou ancienne ; pour un ticket, exige qu'il ait été ouvert par contexte."""
    with verrou(version):
        preparation = preparation_valide(version)
        if numero is None:
            return preparation
        if str(numero) not in preparation["essais"]:
            sys.exit(f"Ticket #{numero} non ouvert pendant ce passage : lancer d'abord "
                     f"python analyses.py contexte --ticket {numero}, puis reprendre.")
        return preparation


def ouvrir_ticket(version, numero, mode):
    """Compte un essai sur le ticket et le compte dans le lot ; refuse au-delà de ESSAIS_MAX ou du lot."""
    with verrou(version):
        preparation = preparation_valide(version)
        essais = preparation["essais"].get(str(numero), 0)
        if essais >= ESSAIS_MAX:
            sys.exit(f"Ticket #{numero} : {ESSAIS_MAX} essais déjà faits pendant ce passage. Il est laissé à l'humain : "
                     "ne pas insister, rendre la main.")
        lot = preparation["lot"]
        if numero not in preparation["tickets"]:
            if lot and len(preparation["tickets"]) >= lot:
                sys.exit(f"Lot atteint : {lot} ticket(s) ouverts depuis la préparation du "
                         f"{preparation['date'].strftime('%d/%m/%Y %H:%M')}. Le ticket #{numero} n'est pas traité "
                         "pendant ce passage : rendre la main.")
            preparation["tickets"].append(numero)
        preparation["essais"][str(numero)] = essais + 1
        preparation["modes"][str(numero)] = mode
        ecrire_preparation(version, preparation)
        return essais + 1


def lire_reprises(version):
    try:
        return json.loads((ANALYSES / version / ".reprises.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def ecrire_reprises(version, reprises):
    with verrou(version):
        chemin = ANALYSES / version / ".reprises.json"
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(json.dumps(reprises, ensure_ascii=False, indent=1, sort_keys=True), encoding="utf-8")


def chemin_relectures(version):
    return ANALYSES / version / ".relectures.json"


def lire_relectures(version):
    try:
        return json.loads(chemin_relectures(version).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def empreinte(version, numero):
    chemin = ANALYSES / version / f"{numero}.md"
    return hashlib.sha1(chemin.read_bytes()).hexdigest() if chemin.exists() else ""


# --------------------------------------------------------------------------
# Contrôle d'une analyse
# --------------------------------------------------------------------------

def sous_bloc(section, titre):
    """Contenu d'un bloc « ### titre » à l'intérieur d'une section, jusqu'au bloc ou à la section suivante."""
    trouve = re.search(r"(?m)^###\s+" + re.escape(titre) + r"\s*\n(.*?)(?=^###\s|^##\s|\Z)", section, re.DOTALL)
    return trouve.group(1) if trouve else None


def lire_playwright(section):
    """Champs de la spécification Playwright (dict), ou None si le bloc est absent."""
    bloc = sous_bloc(section, "Spécification Playwright")
    if bloc is None:
        return None
    champs = {}
    for ligne in bloc.splitlines():
        trouve = re.match(r"\s*-\s*([^:]+?)\s*:\s*(.+)$", ligne)
        if trouve:
            champs[trouve.group(1).strip()] = trouve.group(2).strip()
    return champs


def controler_issue(texte, champs, numero):
    """Cohérence entre l'issue retenue, la fiche cible, l'automatisabilité et le contenu de la section 4."""
    issue = champs.get("Issue", "")
    if not issue:
        return []
    erreurs = []
    lettre = issue[:1]
    nature = champs.get("Nature du test", "")
    fiche = champs.get("Fiche cible", "")
    automatisabilite = champs.get("Automatisabilité", "")
    procedure = section_de(texte, "## 4. Procédure de test proposée")
    comparaison = section_de(texte, "## 3. Comparaison avec l'existant")

    if (nature in SANS_PROCEDURE) != (issue == "Sans objet"):
        erreurs.append("« Issue » : « Sans objet » est réservé aux natures « Relecture documentaire » et « Hors campagne », "
                       "et seulement à elles")
    if lettre in "AB" and (not fiche or fiche_sans_cible(fiche)):
        erreurs.append(f"« Issue » {issue} : une procédure existante est rejouée ou adaptée, donc « Fiche cible » "
                       "désigne la fiche existante (identifiant et titre)")
    if lettre in "AB" and "**Comparaison des procédures.**" not in comparaison:
        erreurs.append("section 3 : avec une procédure existante, ajouter le paragraphe « **Comparaison des procédures.** » "
                       "qui confronte, point par point, ce que teste la fiche et ce que demande le ticket")
    if lettre == "A" and "**Procédure existante à rejouer.**" not in procedure:
        erreurs.append("section 4 : issue A, ouvrir la section par « **Procédure existante à rejouer.** » suivi de la fiche, "
                       "du sous-titre et des étapes du plan à exécuter telles quelles")
    if lettre == "B" and "**Écarts avec la procédure existante.**" not in procedure:
        erreurs.append("section 4 : issue B, ouvrir la section par « **Écarts avec la procédure existante.** » "
                       "(étapes conservées, modifiées, ajoutées)")
    parties_env = re.split(r"\s*\+\s*", champs.get("Environnement", ""))
    if lettre == "C":
        if "WebApp" not in parties_env or automatisabilite not in AUTOMATISABLES:
            erreurs.append("« Issue » C : réservée aux procédures entièrement jouables dans le navigateur "
                           "(Environnement WebApp, Automatisabilité « Automatisable » ou « Difficile ») ; sinon l'issue est D")
    if lettre == "D" and automatisabilite in AUTOMATISABLES:
        erreurs.append("« Issue » D : procédure manuelle, l'automatisabilité ne peut pas être « Automatisable » ni « Difficile » ; sinon l'issue est C")

    playwright = lire_playwright(procedure)
    if lettre == "C" or (lettre == "B" and automatisabilite in AUTOMATISABLES):
        if playwright is None:
            erreurs.append("section 4 : bloc « ### Spécification Playwright » absent ; il est obligatoire pour une procédure "
                           "automatisable (issue C, ou issue B automatisable)")
        else:
            for nom in CHAMPS_PLAYWRIGHT:
                if not playwright.get(nom):
                    erreurs.append(f"spécification Playwright : ligne « - {nom} : … » absente ou vide")
            if playwright.get("Type") == "@lecture" and not re.match(r"(?i)aucune?\b", playwright.get("Données créées", "aucune")):
                erreurs.append("spécification Playwright : un test « @lecture » ne crée aucune donnée ; avec « Données créées » "
                               "renseigné, le type est « @ecriture », ou « @perturbateur » s'il modifie un réglage partagé")
            if playwright.get("Type") and playwright["Type"] not in TYPES_PLAYWRIGHT:
                erreurs.append(f"spécification Playwright : « Type » vaut « {playwright['Type']} », valeurs autorisées : "
                               + " · ".join(TYPES_PLAYWRIGHT))
    if lettre == "D":
        bloc = sous_bloc(procedure, "Prérequis et moyens")
        if bloc is None or not any(l.strip().startswith("- ") for l in bloc.splitlines()):
            erreurs.append("section 4 : issue D, bloc « ### Prérequis et moyens » absent ou vide (matériel, simulateur, "
                           "accès, données, machines, personnes nécessaires)")
    return erreurs


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
    attendus = {"WebApp": "WebApp", "WinApp": "WinApp", "Application mobile": "Mobile"}
    application = champs.get("Application", "")
    if champs.get("Environnement") and application in attendus and attendus[application] not in parties_env:
        erreurs.append(f"« Application » vaut « {application} » mais l'environnement ne comprend pas « {attendus[application]} » : "
                       "l'application est celle où se joue le test (un processeur ou un outil serveur relève de « Serveur et services »)")
    if champs.get("Environnement") and "WebApp" not in parties_env and \
            champs.get("Automatisabilité") not in ("Hors outillage actuel", "Non applicable"):
        erreurs.append("« Automatisabilité » : sans WebApp dans l'environnement, la valeur doit être « Hors outillage actuel » ou « Non applicable »")
    if "WebApp" in parties_env and champs.get("Automatisabilité") == "Hors outillage actuel":
        erreurs.append("« Automatisabilité » : avec WebApp dans l'environnement, la valeur est « Automatisable », « Difficile » "
                       "ou « Impossible sans script externe » (étape hors navigateur), jamais « Hors outillage actuel » ; "
                       "si rien ne se passe dans le navigateur, l'environnement n'est pas WebApp")

    comparaison = section_de(texte, "## 3. Comparaison avec l'existant")
    if "Recherche dans les plans" not in comparaison:
        erreurs.append("section 3 : le paragraphe « **Recherche dans les plans.** » est absent")
    elif f"#{numero}" not in comparaison:
        erreurs.append(f"section 3 : la recherche de #{numero} dans les plans n'est pas rapportée")
    for plan in re.findall(r"referentiel/plans/(\d{2})", section_de(texte, "## Sources").replace("\\", "/")):
        if not re.search(rf"\b({plan}|{int(plan)})\b", comparaison):
            erreurs.append(f"sources : le plan {plan} est cité mais la section 3 n'en rapporte rien")
    for i, j in paragraphes_redondants(comparaison):
        erreurs.append(f"section 3 : les paragraphes {i} et {j} disent la même chose ; n'en garder qu'un")

    nature = champs.get("Nature du test", "")
    if nature not in SANS_PROCEDURE:
        procedure = re.split(r"(?m)^###\s", section_de(texte, "## 4. Procédure de test proposée"))[0]
        etapes = [l for l in procedure.splitlines() if l.strip().startswith("- ")]
        if not etapes:
            erreurs.append("procédure de test : aucune étape (lignes commençant par « - »)")
        elif not all(f"#{numero}" in l for l in etapes):
            erreurs.append(f"procédure de test : chaque étape doit citer le ticket analysé (#{numero}) ; une étape propre "
                           "à un autre ticket va dans l'analyse de ce ticket, et la section 5 indique de les exécuter ensemble")
        elif not any("Résultat attendu" in l for l in etapes):
            erreurs.append("procédure de test : aucune étape ne précise de « Résultat attendu »")

    erreurs += controler_issue(texte, champs, numero)

    if "referentiel/plans/" not in section_de(texte, "## Sources").replace("\\", "/"):
        erreurs.append("sources : aucun plan de referentiel/plans/ cité ; la recherche dans les plans est obligatoire, même sans fiche cible")

    erreurs += controler_fiche(champs)
    erreurs += controler_coherence_fiche(texte, champs)

    reprise = lire_reprises(version).get(str(numero))
    if reprise:
        erreurs.append(f"analyse signalée à reprendre le {reprise} : lancer python analyses.py reprendre --ticket {numero}, "
                       "puis la réécrire entièrement ; une retouche de l'analyse existante ne lève pas ce signalement")

    lignes_ticket = [d for d in decisions if d["ticket"] == numero]
    for d in lignes_ticket:
        if applicable(d):
            erreurs.append(f"décision « {d['decision']} » non appliquée : l'appliquer à l'analyse, puis lancer python analyses.py appliquer --ticket {numero}")
    # Les remarques de relecture en attente concernent l'humain : elles ne rendent pas l'analyse non conforme.
    questions = [d for d in lignes_ticket if not est_relecture(d)]
    en_attente = [d for d in questions if not d["decision"]]
    if champs.get("Décision humaine requise") == "Oui" and not questions:
        erreurs.append("« Décision humaine requise » vaut Oui mais aucune question n'est inscrite dans decisions.md")
    ouvertes = [d for d in questions if not d["decision"] or (not d["appliquee"] and refus_decision(d))]
    if champs.get("Décision humaine requise") == "Oui" and questions and not ouvertes:
        erreurs.append("toutes les questions de ce ticket sont tranchées : reporter les décisions dans l'analyse "
                       "et mettre « Décision humaine requise » à « Non »")
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

ORDRE_MODES = {"appliquer": 0, "reprendre": 1, "analyser": 2}


def file_de_travail(version):
    """(file, à jour, décisions à reformuler).

    Chaque élément de la file : {"ticket", "mode", "motif", "decisions"} ; mode = appliquer, reprendre ou analyser.
    1. Pas d'analyse : analyser.
    2. Ticket modifié depuis l'analyse, analyse signalée à reprendre ou décision « réanalyser » : reprendre
       (les décisions à appliquer sont intégrées à la nouvelle analyse).
    3. Décision applicable : appliquer.
    4. Analyse non conforme : reprendre (et signalement « à reprendre »).
    """
    numeros = selection_courante(version)
    _, decisions = lire_decisions(version)
    reconnues, inconnues = decisions_a_appliquer(decisions)
    par_ticket = {}
    for d in reconnues:
        par_ticket.setdefault(d["ticket"], []).append(d)
    reprises = lire_reprises(version)
    maintenant = datetime.now().strftime("%d/%m/%Y %H:%M")
    file, a_jour = [], []
    for numero in numeros:
        ticket = lire_ticket(version, numero)
        chemin = ANALYSES / version / f"{numero}.md"
        a_appliquer = par_ticket.get(numero, [])

        def ajouter(mode, motif):
            file.append({"ticket": ticket, "mode": mode, "motif": motif, "decisions": a_appliquer})

        if not chemin.exists():
            ajouter("analyser", "nouveau ticket")
        elif lire_analyse(chemin)["mis_a_jour"] != ticket["mis_a_jour"]:
            reprises.setdefault(str(numero), maintenant)
            ajouter("reprendre", "ticket modifié depuis l'analyse")
        elif str(numero) in reprises:
            ajouter("reprendre", f"analyse signalée à reprendre le {reprises[str(numero)]}")
        elif any(forme_decision(d["decision"]) == "réanalyser" for d in a_appliquer):
            ajouter("reprendre", "décision « réanalyser »")
        elif a_appliquer:
            ajouter("appliquer", "décision à appliquer : " + " ; ".join(
                f"« {d['decision'][:60]}{'…' if len(d['decision']) > 60 else ''} »" for d in a_appliquer))
        elif verifier_analyse(version, numero, decisions):
            reprises.setdefault(str(numero), maintenant)
            ajouter("reprendre", "analyse non conforme")
        else:
            a_jour.append(ticket)
    if reprises != lire_reprises(version):
        ecrire_reprises(version, reprises)
    file.sort(key=lambda e: (ORDRE_MODES[e["mode"]], e["ticket"]["fonction"].lower(), e["ticket"]["id"]))
    return file, a_jour, inconnues


def etat(version, maximum=None):
    numeros = selection_courante(version)
    dossier_analyses = ANALYSES / version
    conforme = lire_decisions(version)[0]
    file, a_jour, inconnues = file_de_travail(version)

    orphelines = []
    if dossier_analyses.is_dir():
        for chemin in sorted(dossier_analyses.glob("*.md")):
            if chemin.stem.isdigit() and int(chemin.stem) not in numeros:
                orphelines.append(int(chemin.stem))

    print(f"Version {version} : {len(numeros)} tickets dans la sélection")
    print(f"Analyses à jour : {len(a_jour)} | À traiter : {len(file)} | Décisions en attente : {decisions_en_attente(version)}")
    if not conforme:
        print("ATTENTION : decisions.md n'a pas le format attendu ; lancer python analyses.py reparer-decisions avant de poursuivre.")
    for d in inconnues:
        print(f"Décision à reformuler par l'humain pour #{d['ticket']} (« {d['decision']} ») : {refus_decision(d)}. Ne pas l'appliquer.")
    print()
    if file:
        print("À traiter, dans cet ordre (numéro | mode | Fonction | motif | sujet) :")
        for e in file[:maximum] if maximum else file:
            t = e["ticket"]
            print(f"  {t['id']} | {e['mode']} | {t['fonction'] or '(vide)'} | {e['motif']} | {t['sujet']}")
        if maximum and len(file) > maximum:
            print(f"  … et {len(file) - maximum} autre(s).")
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
        print(f"avertissement : décision à reformuler par l'humain pour #{d['ticket']} (« {d['decision']} ») : {refus_decision(d)}")
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


def ajouter_ligne_decision(version, numero, texte_question, proposition):
    """Ajoute une ligne en attente à decisions.md (à appeler sous verrou)."""
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
    return chemin


def question(version, numero, texte_question, proposition):
    if not texte_question or not proposition:
        sys.exit("Préciser --question et --proposition.")
    raison = raison_proposition_invalidable(proposition)
    if raison:
        sys.exit("Proposition refusée : " + raison.split(" : ")[0] + ". La proposition doit être une réponse unique et "
                 "concrète, même provisoire (une fiche, une valeur, un comportement attendu), que l'humain pourra "
                 "valider telle quelle ou corriger. Reformuler et relancer.")
    with verrou(version):
        exiger_preparation(version, numero)
        _, decisions = lire_decisions(version)
        if any(d["ticket"] == numero and not d["decision"] and normaliser(d["question"]) == normaliser(texte_question)
               for d in decisions):
            sys.exit(f"Cette question est déjà en attente pour #{numero} : ne pas la répéter.")
        chemin = ajouter_ligne_decision(version, numero, texte_question, proposition)
    print(f"Question ajoutée pour #{numero} dans {chemin}")


def journal(version, numero, texte):
    if not texte:
        sys.exit("Préciser --texte.")
    with verrou(version):
        exiger_preparation(version, numero)
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
    with verrou(version):
        _, lignes = lire_decisions(version)
        contenu = ENTETE_DECISIONS.format(version=version)
        for l in lignes:
            appliquee = l["appliquee"] if re.fullmatch(r"\d{2}/\d{2}/\d{4}", l["appliquee"]) else ""
            contenu += (f"| #{l['ticket']} | {nettoyer(l['question'])} | {nettoyer(l['proposition'])} | "
                        f"{nettoyer(l['decision'])} | {appliquee} |\n")
        chemin.write_text(contenu, encoding="utf-8")
    print(f"decisions.md réécrit au format attendu ({len(lignes)} ligne(s) conservée(s), décisions intactes).")


def preparer(version_demandee, lot=None, nouveau=False):
    lot = lot or 0
    for script in ("recuperer_tickets.py", "convertir_plans.py"):
        print(f"=== {script} ===")
        resultat = subprocess.run([sys.executable, str(DOSSIER / script)], cwd=DOSSIER)
        if resultat.returncode != 0:
            if script == "recuperer_tickets.py":
                sys.exit(f"Échec de {script} : arrêt, les tickets ne sont pas à jour.")
            print(f"Échec de {script} : poursuite avec les plans déjà convertis.")
        print()
    version = choisir_version(version_demandee)
    if lire_env("PLAYWRIGHT_DIR"):
        print("=== couverture Playwright ===")
        resultat = subprocess.run([sys.executable, str(DOSSIER / "analyses.py"), "couverture", "--version", version], cwd=DOSSIER)
        if resultat.returncode != 0:
            print("Échec de la lecture du projet Playwright : poursuite avec la couverture déjà connue.")
        print()
    with verrou(version):
        ancienne = lire_preparation(version)
        en_cours = (not nouveau and ancienne and ancienne["lot"] is not None
                    and (datetime.now() - ancienne["date"]).total_seconds() < DUREE_PREPARATION_H * 3600)
        if en_cours:
            # Relancer preparer ne remet pas les compteurs à zéro : essais, lot et relectures du passage sont conservés.
            # Le lot du passage ouvert ne change pas : un agent ne peut pas l'élargir en relançant preparer.
            if lot and lot != ancienne["lot"]:
                print(f"Lot demandé ({lot}) ignoré : le passage ouvert garde son lot ({ancienne['lot'] or 'sans limite'}). "
                      "Pour changer de lot, l'humain lance preparer --nouveau --lot N.")
            ancienne["force"] = None
            ecrire_preparation(version, ancienne)
        else:
            ecrire_preparation(version, {"date": datetime.now(), "lot": lot, "tickets": [], "essais": {},
                                         "modes": {}, "relus": [], "force": None})
    preparation = lire_preparation(version)
    print("=== état ===")
    if en_cours:
        print(f"Passage ouvert le {preparation['date'].strftime('%d/%m/%Y %H:%M')} poursuivi : "
              f"{len(preparation['tickets'])} ticket(s) déjà ouverts, essais et relectures conservés. "
              "Un nouveau passage s'ouvre seulement après 12 h, ou par l'humain avec --nouveau.")
    lot = preparation["lot"]
    print(f"Lot de ce passage : {lot} ticket(s) au plus." if lot else "Passage sans limite de tickets.")
    etat(version, 15)
    print()
    print("Suite : python analyses.py prochain")


def reprendre(version, numero):
    chemin = ANALYSES / version / f"{numero}.md"
    if not chemin.exists():
        sys.exit(f"Aucune analyse à reprendre pour #{numero}.")
    with verrou(version):
        exiger_preparation(version, numero)
        archives = ANALYSES / version / "archives"
        archives.mkdir(parents=True, exist_ok=True)
        cible = archives / f"{numero}_{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        shutil.move(str(chemin), str(cible))
        reprises = lire_reprises(version)
        if reprises.pop(str(numero), None):
            ecrire_reprises(version, reprises)
    print(f"Analyse de #{numero} archivée dans {cible.relative_to(DOSSIER)}. Rédiger la nouvelle analyse à partir du ticket et des plans, sans relire l'archive.")


def appliquer(version, numero):
    with verrou(version):
        _appliquer(version, numero)


def _appliquer(version, numero):
    exiger_preparation(version, numero)
    chemin = chemin_decisions(version)
    conforme, decisions = lire_decisions(version)
    if not conforme:
        sys.exit("decisions.md n'a pas le format attendu : lancer python analyses.py reparer-decisions.")
    lignes = [d for d in decisions if d["ticket"] == numero and applicable(d)]
    if not lignes:
        sys.exit(f"Aucune décision applicable pour #{numero} (les décisions à reformuler restent à l'humain).")
    analyse = ANALYSES / version / f"{numero}.md"
    if not analyse.exists():
        sys.exit(f"Analyse absente pour #{numero}.")
    champs = lire_analyse(analyse)["champs"]
    for d in lignes:
        forme = forme_decision(d["decision"])
        valeur = re.sub(r"^[^:]*:\s*", "", d["decision"]).strip()
        if forme == "fiche":
            ident = re.match(rf"({MOTIF_ID})\b", valeur)
            if champs.get("Fiche cible", "") in ("", "À décider", "Aucune") or \
                    (ident and not champs.get("Fiche cible", "").startswith(ident.group(1))):
                sys.exit(f"#{numero} : la décision « {d['decision']} » n'est pas reportée dans « Fiche cible ».")
        if forme == "nouveau plan":
            plan = champs.get("Plan cible", "")
            if not plan.startswith("À créer") or normaliser(valeur)[:30] not in normaliser(plan):
                sys.exit(f"#{numero} : la décision « {d['decision']} » doit être reportée dans « Plan cible » "
                         f"sous la forme « À créer — {valeur} ».")
            if champs.get("Fiche cible", "") in ("", "À décider"):
                sys.exit(f"#{numero} : avec un nouveau plan, « Fiche cible » vaut « À créer — » suivi du titre proposé.")
        if forme == "réanalyser":
            archives = ANALYSES / version / "archives"
            du_jour = list(archives.glob(f"{numero}_{datetime.now().strftime('%Y%m%d')}-*.md")) if archives.is_dir() else []
            if not du_jour:
                sys.exit(f"#{numero} : « réanalyser » impose python analyses.py reprendre --ticket {numero} "
                         "puis une analyse entièrement réécrite.")
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
        if (len(cellules) >= 5 and cellules[0] == f"#{numero}"
                and applicable({"decision": cellules[3], "appliquee": cellules[4], "proposition": cellules[2]})):
            ligne = f"| {cellules[0]} | {cellules[1]} | {cellules[2]} | {cellules[3]} | {aujourdhui} |"
        sortie.append(ligne)
    chemin.write_text("\n".join(sortie) + "\n", encoding="utf-8")
    print(f"#{numero} : {len(lignes)} décision(s) datée(s) du {aujourdhui}.")


def rang_environnement(valeur):
    premier = re.split(r"\s*\+\s*", valeur or "Aucun")[0].strip()
    return ENVIRONNEMENTS.index(premier) if premier in ENVIRONNEMENTS else len(ENVIRONNEMENTS)


def cellule(texte):
    return str(texte or "").replace("|", "\\|").strip()


# --------------------------------------------------------------------------
# Couverture Playwright : lecture du projet de campagne
# --------------------------------------------------------------------------

COUVERTURE_JSON = DOSSIER / "referentiel" / "couverture-playwright.json"
COUVERTURE_MD = DOSSIER / "referentiel" / "couverture-playwright.md"
CORRESPONDANCE_PLAYWRIGHT = DOSSIER / "referentiel" / "correspondance-playwright.md"
MOTS_VIDES = {"onglet", "tests", "test", "de", "des", "du", "la", "le", "les", "et", "a", "via", "sur", "en", "d", "l",
              "mc", "apparence", "fonctionnalite", "fonctionnalites", "interface", "acces"}


def lire_env(nom):
    """Valeur d'une variable de l'environnement ou du fichier .env (jamais affichée)."""
    import os
    if os.environ.get(nom):
        return os.environ[nom]
    chemin = DOSSIER / ".env"
    if chemin.exists():
        for ligne in chemin.read_text(encoding="utf-8").splitlines():
            trouve = re.match(r"\s*([^#=]+?)\s*=\s*(.*?)\s*$", ligne)
            if trouve and trouve.group(1) == nom:
                return trouve.group(2)
    return ""


def jetons(texte):
    texte = unicodedata.normalize("NFKD", texte or "").encode("ascii", "ignore").decode().lower()
    return {m for m in re.findall(r"[a-z0-9]+", texte) if m not in MOTS_VIDES and not re.fullmatch(r"mc\d+|g\d+", m)}


def fiches_du_plan(numero_plan="01"):
    """Fiches d'un plan : identifiant, titre, intitulé (titre de section), sous-titres de la fiche, fiche (« ID — titre »)."""
    _, fichier = fichier_plan(numero_plan)
    if not fichier:
        return []
    texte = fichier.read_text(encoding="utf-8")
    trouves = list(re.finditer(rf"ID\s*:\s*({MOTIF_ID})\b[\s\S]{{0,300}}?Titre\s*:\s*([^|\n·*]+)", texte))
    fiches = []
    for i, m in enumerate(trouves):
        avant = texte[:m.start()].splitlines()
        intitule = next((l.lstrip("#").strip() for l in reversed(avant) if l.startswith("#")), "")
        fin = texte.rfind("\n", 0, trouves[i + 1].start()) if i + 1 < len(trouves) else len(texte)
        lignes_corps = texte[m.end():fin].splitlines()
        while lignes_corps and (not lignes_corps[-1].strip() or lignes_corps[-1].startswith("#")):
            lignes_corps.pop()                  # titres qui introduisent la fiche suivante
        corps = "\n".join(lignes_corps)
        sous_titres = [l.lstrip("#").strip() for l in corps.splitlines() if l.startswith("#")]
        sous_titres += re.findall(r"(?m)^\*\*(.+?)\*\*\s*$", corps)
        titre = m.group(2).strip()
        fiches.append({"identifiant": m.group(1), "titre": titre, "intitule": intitule,
                       "sous_titres": sous_titres, "fiche": f"{m.group(1)} — {titre}"})
    return fiches


def tests_du_rapport(donnees):
    """Tests [(fichier, chemin de describe, titre, tags)] d'un rapport JSON de Playwright (reporter json ou rapport HTML)."""
    tests = []
    if "files" in donnees:                      # rapport HTML (report.json embarqué)
        for f in donnees["files"]:
            for t in f.get("tests", []):
                tests.append((f["fileName"], list(t.get("path", [])), t["title"], list(t.get("tags", []))))
    else:                                       # npx playwright test --list --reporter=json
        def parcourir(suite, fichier, chemin):
            fichier = suite.get("file", fichier)
            titre = suite.get("title", "")
            chemin2 = chemin + ([titre] if titre and titre != fichier and not titre.endswith((".ts", ".js")) else [])
            for spec in suite.get("specs", []):
                tags = ["@" + t.lstrip("@") for t in spec.get("tags", [])]
                tests.append((spec.get("file", fichier), chemin2, spec["title"], tags))
            for sous in suite.get("suites", []):
                parcourir(sous, fichier, chemin2)
        for suite in donnees.get("suites", []):
            parcourir(suite, suite.get("file", ""), [])
    vus, uniques = set(), []
    for t in tests:                             # un test joué par plusieurs projets n'est compté qu'une fois
        cle = (t[0], tuple(t[1]), t[2])
        if cle not in vus:
            vus.add(cle)
            uniques.append(t)
    return uniques


def charger_rapport(depuis):
    """Données du rapport Playwright : fichier JSON, rapport HTML, ou liste obtenue dans PLAYWRIGHT_DIR."""
    import base64, io, zipfile
    if depuis:
        chemin = Path(depuis)
        texte = chemin.read_text(encoding="utf-8")
        if chemin.suffix.lower() in (".html", ".htm"):
            bloc = re.search(r'<template id="playwrightReportBase64">(.*?)</template>', texte, re.S)
            if not bloc:
                sys.exit(f"{chemin} n'est pas un rapport HTML de Playwright.")
            archive = zipfile.ZipFile(io.BytesIO(base64.b64decode(bloc.group(1).split(",", 1)[-1])))
            return json.loads(archive.read("report.json"))
        return json.loads(texte[texte.index("{"):])
    dossier = lire_env("PLAYWRIGHT_DIR")
    if not dossier or not Path(dossier).is_dir():
        sys.exit("PLAYWRIGHT_DIR absent du .env ou introuvable : ajouter PLAYWRIGHT_DIR=<dossier du projet Playwright>, "
                 "ou passer --depuis <rapport HTML ou JSON>.")
    npx = shutil.which("npx.cmd") or shutil.which("npx") or "npx"
    resultat = subprocess.run([npx, "playwright", "test", "--list", "--reporter=json"], cwd=dossier,
                              capture_output=True, text=True, encoding="utf-8", errors="replace")
    if resultat.returncode != 0 or "{" not in resultat.stdout:
        sys.exit("Échec de « npx playwright test --list --reporter=json » dans PLAYWRIGHT_DIR :\n" + resultat.stderr[-1500:])
    return json.loads(resultat.stdout[resultat.stdout.index("{"):])


def lire_correspondance_playwright():
    """Rattachements imposés par l'humain : {groupe Playwright normalisé: fiche du plan, ou "" pour aucune}."""
    if not CORRESPONDANCE_PLAYWRIGHT.exists():
        return {}
    imposes = {}
    for ligne in CORRESPONDANCE_PLAYWRIGHT.read_text(encoding="utf-8").splitlines():
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cellules) >= 2 and re.match(rf"{MOTIF_ID}\s*-", cellules[0]):
            imposes[normaliser(cellules[0])] = "" if cellules[1].lower().startswith("aucune") else cellules[1]
    return imposes


def rattacher(groupe, fiches):
    """(fiche, mode) pour un groupe « MCxx - Libellé ».

    1. Fiche de même identifiant dont un titre ou sous-titre contient tout le libellé : « identifiant et libellé ».
    2. Sinon, fiche dont le titre ou l'intitulé contient tout le libellé, la plus proche : « libellé » (numérotation différente).
    3. Sinon, fiche de même identifiant si elle est unique : « identifiant seul », à confirmer.
    """
    ident = re.match(rf"({MOTIF_ID})", groupe).group(1)
    libelle = jetons(re.sub(r"\(#[^)]*\)", "", groupe))
    if not libelle:
        libelle = {"_"}

    def proximite(textes):
        scores = [len(libelle) / len(libelle | jetons(t)) for t in textes if libelle <= jetons(t)]
        return max(scores) if scores else 0

    memes = [f for f in fiches if f["identifiant"] == ident]
    # Le titre de section fait foi : dans le plan 01, plusieurs champs « Titre » sont des copier-coller.
    meme = max(((proximite([f["intitule"] or f["titre"]] + f["sous_titres"]), f) for f in memes),
               key=lambda c: c[0], default=(0, None))
    autre = max(((proximite([f["intitule"] or f["titre"]]), f) for f in fiches if f["identifiant"] != ident),
                key=lambda c: c[0], default=(0, None))
    if meme[0] and not (autre[0] == 1 and meme[0] < 1):
        return meme[1], "identifiant et libellé"
    if autre[0]:
        return autre[1], "libellé"
    if len(memes) == 1:
        return memes[0], "identifiant seul"
    return None, None


def fiche_imposee(texte, fiches):
    """Fiche du plan désignée dans correspondance-playwright.md : texte exact, ou même identifiant et titre proche."""
    exacte = next((f for f in fiches if normaliser(f["fiche"]) == normaliser(texte)), None)
    if exacte:
        return exacte
    ident = re.match(rf"\s*({MOTIF_ID})\b", texte)
    if not ident:
        return None
    mots = jetons(texte[ident.end():])
    proches = [(len(mots & (jetons(f["titre"]) | jetons(f["intitule"]))), f) for f in fiches if f["identifiant"] == ident.group(1)]
    proches = [p for p in proches if p[0]]
    return max(proches, key=lambda p: p[0])[1] if proches else None


def couverture(version, depuis=None):
    """Génère referentiel/couverture-playwright.json et .md à partir du projet de campagne Playwright."""
    tests = tests_du_rapport(charger_rapport(depuis))
    fiches = fiches_du_plan("01")
    if not fiches:
        sys.exit("Aucune fiche « ID : … Titre : … » trouvée dans le plan 01 de referentiel/plans/ : lancer convertir_plans.py.")
    imposes = lire_correspondance_playwright()
    groupes, par_fiche, par_ticket = {}, {}, {}
    for fichier, chemin, titre, tags in tests:
        racine = chemin[0] if chemin else ""
        entete = re.match(rf"({MOTIF_ID})\s*-\s*([^-]+)", racine)
        for ticket in re.findall(r"#(\d{3,5})", " ".join(chemin + [titre])):
            par_ticket.setdefault(ticket, []).append({"fichier": fichier, "titre": titre})
        if not entete:
            continue
        groupe = f"{entete.group(1)} - {entete.group(2).strip()}"
        if groupe not in groupes:
            cle = normaliser(groupe)
            if cle in imposes:
                fiche = fiche_imposee(imposes[cle], fiches) if imposes[cle] else None
                groupes[groupe] = (fiche, "imposé" if imposes[cle] else "aucune fiche", imposes[cle])
            else:
                fiche, mode = rattacher(groupe, fiches)
                groupes[groupe] = (fiche, mode, "")
        fiche = groupes[groupe][0]
        if fiche:
            entree = par_fiche.setdefault(fiche["fiche"], {"fiche": fiche["fiche"], "fichiers": [], "groupes": [],
                                                           "tests": 0, "a_valider": 0})
            if fichier not in entree["fichiers"]:
                entree["fichiers"].append(fichier)
            if groupe not in entree["groupes"]:
                entree["groupes"].append(groupe)
            entree["tests"] += 1
            entree["a_valider"] += any("a-valider" in t for t in tags)

    COUVERTURE_JSON.write_text(json.dumps({"genere_le": datetime.now().isoformat(timespec="seconds"),
                                           "fiches": par_fiche, "tickets": par_ticket},
                                          ensure_ascii=False, indent=1), encoding="utf-8")
    lignes = ["# Couverture Playwright", "",
              f"Générée le {datetime.now().strftime('%d/%m/%Y %H:%M')} par `python analyses.py couverture`. "
              "Ne pas modifier à la main : corriger les rattachements dans `referentiel/correspondance-playwright.md`.", "",
              f"- Tests lus : {len(tests)}", f"- Fiches du plan 01 couvertes : {len(par_fiche)} sur {len(fiches)}",
              f"- Tickets cités dans les titres de test : {len(par_ticket)}", "",
              "## Fiches couvertes", "", "| Fiche | Tests | Dont @a-valider | Fichiers |", "|---|---|---|---|"]
    for f in fiches:
        e = par_fiche.get(f["fiche"])
        if e:
            lignes.append(f"| {cellule(e['fiche'])} | {e['tests']} | {e['a_valider']} | {cellule(', '.join(e['fichiers']))} |")
    lignes += ["", "## Rattachement des groupes de tests", "",
               "| Groupe Playwright | Fiche du plan | Rattachement | Remarque |", "|---|---|---|---|"]
    for groupe, (fiche, mode, impose) in sorted(groupes.items()):
        remarque = ""
        if fiche and re.match(rf"({MOTIF_ID})", groupe).group(1) != fiche["identifiant"]:
            remarque = f"numérotation différente du plan ({fiche['identifiant']})"
        if mode == "identifiant seul":
            remarque = "à confirmer dans correspondance-playwright.md"
        if not fiche and mode == "imposé":
            remarque = (f"fiche imposée « {impose} » introuvable dans le plan 01 : la recopier depuis la liste "
                        "« Fiches du plan 01 » ci-dessous, ou écrire « Aucune »")
        elif not fiche and mode != "aucune fiche":
            remarque = "non rattaché : préciser la fiche dans correspondance-playwright.md"
        lignes.append(f"| {cellule(groupe)} | {cellule(fiche['fiche'] if fiche else '—')} | {mode or '—'} | {remarque} |")
    lignes += ["", "## Fiches du plan 01", "",
               "Désignations exactes, à recopier telles quelles dans `correspondance-playwright.md`.", "",
               "| Fiche | Titre de section | Couverte |", "|---|---|---|"]
    for f in fiches:
        lignes.append(f"| {cellule(f['fiche'])} | {cellule(f['intitule'])} | {'oui' if f['fiche'] in par_fiche else 'non'} |")
    COUVERTURE_MD.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"Couverture écrite : {COUVERTURE_MD.relative_to(DOSSIER)} ({len(tests)} tests, {len(par_fiche)} fiches, "
          f"{len(par_ticket)} tickets cités)")
    ecarts = [g for g, (f, m, _) in groupes.items() if (not f and m != "aucune fiche") or m == "identifiant seul"]
    if ecarts:
        print("Groupes à rattacher ou confirmer : " + " ; ".join(sorted(ecarts)))


def lire_couverture():
    try:
        return json.loads(COUVERTURE_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"fiches": {}, "tickets": {}}


def test_existant(couverture_, fiche, numero=None):
    """Résumé de ce qui existe déjà dans la campagne Playwright pour ce ticket et cette fiche."""
    morceaux = []
    if numero and str(numero) in couverture_.get("tickets", {}):
        morceaux.append(f"ticket cité dans {len(couverture_['tickets'][str(numero)])} test(s)")
    for cle, e in couverture_.get("fiches", {}).items():
        if fiche and normaliser(cle) == normaliser(fiche):
            morceaux.append(f"fiche couverte ({e['tests']} tests)")
    return " ; ".join(morceaux) or "—"


def etapes_de(procedure):
    """Étapes « - action. Résultat attendu : … (#n) » de la procédure, hors blocs ### (spécification, prérequis)."""
    principal = re.split(r"(?m)^###\s", procedure)[0]
    etapes, sous_titre = [], ""
    for ligne in principal.splitlines():
        titre = re.match(r"\s*\*\*(.+?)\*\*\s*$", ligne)
        if titre:
            sous_titre = titre.group(1).strip()
            continue
        if ligne.strip().startswith("- "):
            corps = ligne.strip()[2:].strip()
            action, _, attendu = corps.partition("Résultat attendu :")
            etapes.append({"sous_titre": sous_titre, "action": action.strip(), "attendu": attendu.strip()})
    return etapes


def fiche_transmission(version, t):
    """Texte de la fiche de transmission d'un ticket au projet Playwright (fichier généré, jamais modifié à la main)."""
    existant = t["playwright_existant"]
    pw = t["playwright"] or {}
    lignes = [f"# Ticket #{t['ticket']} — {t['sujet']}", "",
              "Fiche générée par `python analyses.py exporter` à partir de l'analyse. Ne pas modifier à la main.", "",
              "| Champ | Valeur |", "|---|---|",
              f"| Issue | {t['issue_libelle']} |", f"| Nature du test | {t['nature']} |",
              f"| Automatisabilité | {t['automatisabilite']} |", f"| Environnement | {t['environnement']} |",
              f"| Plan cible | {t['plan']} |", f"| Fiche cible | {t['fiche']} |",
              f"| Fiche déjà couverte par Playwright | {existant['fiche_couverte'] and 'oui' or 'non'} |",
              f"| Mis à jour (Redmine) | {t['mis_a_jour']} |"]
    for cle in ("Type", "Compte", "Dossier", "Référentiel", "Données créées"):
        if pw.get(cle):
            lignes.append(f"| Playwright — {cle} | {pw[cle]} |")
    if t["prerequis"]:
        lignes += ["", "## Prérequis particuliers", "", t["prerequis"]]
    if t["prerequis_et_moyens"]:
        lignes += ["", "## Prérequis et moyens", ""] + [f"- {p}" for p in t["prerequis_et_moyens"]]
    if existant["tests_citant_le_ticket"]:
        lignes += ["", "## Tests Playwright qui citent déjà ce ticket", ""] + [f"- {x}" for x in existant["tests_citant_le_ticket"]]
    lignes += ["", "## Étapes", "", "| Bloc | Action | Résultat attendu |", "|---|---|---|"]
    for e in t["etapes"]:
        cellules = [str(e.get(c, "")).replace("|", "\\|").replace("\n", " ") for c in ("sous_titre", "action", "attendu")]
        lignes.append("| " + " | ".join(cellules) + " |")
    lignes += ["", f"Analyse complète (côté Redmine_Automation) : `{t['analyse']}`", ""]
    return "\n".join(lignes)


def transmettre_a_playwright(version, tickets):
    """Écrit echange/playwright/<version>/ : une fiche par ticket concerné par la WebApp, et index.json.
    N'écrit que dans ce dossier de ce dépôt ; le projet Playwright ne fait que le lire."""
    cible = DOSSIER / "echange" / "playwright" / version
    cible.mkdir(parents=True, exist_ok=True)
    concernes = [t for t in tickets if "webapp" in normaliser(t.get("environnement", "") or "")]
    index = []
    for t in concernes:
        texte = fiche_transmission(version, t)
        (cible / f"{t['ticket']}.md").write_text(texte, encoding="utf-8")
        index.append({"ticket": t["ticket"], "sujet": t["sujet"], "issue": t["issue"], "fiche": t["fiche"],
                      "fichier": f"{t['ticket']}.md", "empreinte": hashlib.sha1(texte.encode("utf-8")).hexdigest()[:12]})
    attendus = {f"{e['ticket']}.md" for e in index}
    for ancien in cible.glob("*.md"):
        if ancien.name not in attendus:
            ancien.unlink()
    (cible / "index.json").write_text(json.dumps(
        {"version": version, "genere_le": datetime.now().isoformat(timespec="seconds"), "format_contrat": 1,
         "tickets": sorted(index, key=lambda e: e["ticket"])}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Échange Playwright écrit : {cible.relative_to(DOSSIER)} ({len(index)} fiche(s) sur {len(tickets)} tickets)")


def exporter(version):
    """Écrit export/<version>/campagne.json : contrat d'échange avec le projet de campagne Playwright."""
    numeros = selection_courante(version)
    _, decisions = lire_decisions(version)
    couverture = lire_couverture()
    tickets, ecartees = [], []
    for numero in numeros:
        chemin = ANALYSES / version / f"{numero}.md"
        if not chemin.exists():
            continue
        if verifier_analyse(version, numero, decisions):
            ecartees.append(numero)
            continue
        a = lire_analyse(chemin)
        champs, texte = a["champs"], a["texte"]
        procedure = section_de(texte, "## 4. Procédure de test proposée")
        prerequis = sous_bloc(procedure, "Prérequis et moyens")
        fiche = champs.get("Fiche cible", "")
        tickets.append({
            "ticket": numero,
            "sujet": a["titre"],
            "mis_a_jour": a["mis_a_jour"],
            "issue": champs.get("Issue", "")[:1] or None,
            "issue_libelle": champs.get("Issue", ""),
            "application": champs.get("Application", ""),
            "plan": champs.get("Plan cible", ""),
            "fiche": fiche,
            "playwright_existant": {
                "fiche_couverte": next((e for k, e in couverture.get("fiches", {}).items()
                                        if fiche and normaliser(k) == normaliser(fiche)), None),
                "tests_citant_le_ticket": couverture.get("tickets", {}).get(str(numero), []),
            },
            "nature": champs.get("Nature du test", ""),
            "automatisabilite": champs.get("Automatisabilité", ""),
            "environnement": champs.get("Environnement", ""),
            "prerequis": champs.get("Prérequis particuliers", ""),
            "prerequis_et_moyens": [l.strip()[2:] for l in (prerequis or "").splitlines() if l.strip().startswith("- ")],
            "playwright": lire_playwright(procedure),
            "etapes": etapes_de(procedure),
            "analyse": f"analyses/{version}/{numero}.md",
        })
    cible = DOSSIER / "export" / version / "campagne.json"
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(json.dumps({"version": version, "genere_le": datetime.now().isoformat(timespec="seconds"),
                                 "format": 1, "tickets": tickets}, ensure_ascii=False, indent=2), encoding="utf-8")
    transmettre_a_playwright(version, tickets)
    compte = Counter(t["issue"] for t in tickets)
    print(f"Export écrit : {cible.relative_to(DOSSIER)} ({len(tickets)} tickets : "
          + ", ".join(f"{k} = {v}" for k, v in sorted(compte.items(), key=lambda e: str(e[0]))) + ")")
    if ecartees:
        print("Analyses non conformes, non exportées : " + ", ".join(f"#{n}" for n in ecartees))


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

    analyses.sort(key=lambda a: (rang_environnement(champ(a, "Environnement")), champ(a, "Plan cible")[:2],
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
    a_reformuler = decisions_a_appliquer(decisions)[1]
    if a_reformuler:
        lignes.append(f"- Décisions à reformuler par l'humain : {len(a_reformuler)} ("
                      + ", ".join(f"#{d['ticket']}" for d in a_reformuler) + ")")

    for nom in ("Issue", "Nature du test", "Environnement", "Automatisabilité"):
        compte = Counter(champ(a, nom) or "(non renseigné)" for a in analyses)
        lignes += ["", f"## Répartition — {nom}", "", f"| {nom} | Tickets |", "|---|---|"]
        lignes += [f"| {cellule(valeur)} | {nombre} |" for valeur, nombre in compte.most_common()]

    lignes += [
        "",
        "## Ordre de campagne",
        "",
        "Tickets regroupés par environnement, puis par plan et par fiche, pour limiter les changements de configuration.",
        "",
        "| Ticket | Sujet | Environnement | Plan | Fiche | Issue | Test Playwright existant | Décision requise |",
        "|---|---|---|---|---|---|---|---|",
    ]
    couverture = lire_couverture()
    for a in analyses:
        t = a["ticket"]
        marque = " (à reprendre)" if t["id"] in a_reprendre else ""
        lignes.append(
            f"| [#{t['id']}]({t['id']}.md){marque} | {cellule(t['sujet'])} | {cellule(champ(a, 'Environnement'))} | "
            f"{cellule(champ(a, 'Plan cible'))} | {cellule(champ(a, 'Fiche cible'))} | {cellule(champ(a, 'Issue'))} | "
            f"{cellule(test_existant(couverture, champ(a, 'Fiche cible'), t['id']))} | {cellule(champ(a, 'Décision humaine requise'))} |"
        )

    if manquantes:
        lignes += ["", "## Tickets non encore analysés", ""]
        lignes += [f"- #{t['id']} — {t['fonction'] or '(Fonction vide)'} — {t['sujet']}" for t in manquantes]

    dossier_analyses.mkdir(parents=True, exist_ok=True)
    cible = dossier_analyses / "synthese.md"
    cible.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"Synthèse écrite : {cible} ({len(analyses)} analyses, {len(manquantes)} tickets non analysés)")


# --------------------------------------------------------------------------
# Passage des agents : file de travail, contexte d'un ticket, relecture, bilan
# --------------------------------------------------------------------------

AGENT_DU_MODE = {"appliquer": "Applicateur décision", "reprendre": "Analyste ticket", "analyser": "Analyste ticket"}


def prochain(version, numero=None, relire=False, tout=False):
    preparation = exiger_preparation(version)
    if relire:
        prochain_relecture(version, preparation, tout)
        return
    file, _, inconnues = file_de_travail(version)
    if numero:
        if numero not in selection_courante(version):
            sys.exit(f"#{numero} n'est pas dans la sélection de {version}.")
        with verrou(version):
            preparation = preparation_valide(version)
            preparation["force"] = numero
            ecrire_preparation(version, preparation)
        entree = next((e for e in file if e["ticket"]["id"] == numero), None)
        if not entree:
            existe = (ANALYSES / version / f"{numero}.md").exists()
            entree = {"ticket": lire_ticket(version, numero), "mode": "reprendre" if existe else "analyser",
                      "motif": "demandé explicitement", "decisions": []}
        file = [entree]
    essais = preparation["essais"]
    abandonnes = [e for e in file if essais.get(str(e["ticket"]["id"]), 0) >= ESSAIS_MAX]
    file = [e for e in file if essais.get(str(e["ticket"]["id"]), 0) < ESSAIS_MAX]
    lot, hors_lot = preparation["lot"], 0
    if lot:
        places = lot - len(preparation["tickets"])
        retenus = []
        for e in file:
            if e["ticket"]["id"] in preparation["tickets"]:
                retenus.append(e)
            elif places > 0:
                retenus.append(e)
                places -= 1
            else:
                hors_lot += 1
        file = retenus

    if file:
        print(f"{len(file)} ticket(s) à confier aux agents, dans cet ordre (numéro | mode | motif | sujet) :")
        for e in file:
            t = e["ticket"]
            print(f"  {t['id']} | {e['mode']} | {e['motif']} | {t['sujet']}")
        print()
        print("Agent par mode : appliquer → « Applicateur décision » ; reprendre et analyser → « Analyste ticket ».")
    else:
        print("Aucun ticket à confier aux agents.")
    if hors_lot:
        print(f"Lot atteint : {hors_lot} autre(s) ticket(s) attendront le prochain passage.")
    if abandonnes:
        print(f"Laissés à l'humain après {ESSAIS_MAX} essais : " + ", ".join(f"#{e['ticket']['id']}" for e in abandonnes))
    if inconnues:
        print("Décisions à reformuler par l'humain (aucun agent ne les traite) : "
              + ", ".join(f"#{d['ticket']}" for d in inconnues))


def a_relire(version, preparation, tout):
    """Analyses conformes dont le contenu actuel n'a pas encore été relu."""
    numeros = selection_courante(version) if tout else [n for n in preparation["tickets"] if n in selection_courante(version)]
    relectures = lire_relectures(version)
    _, decisions = lire_decisions(version)
    resultat = []
    for n in numeros:
        if n in preparation["relus"] or not (ANALYSES / version / f"{n}.md").exists():
            continue
        if relectures.get(str(n)) == empreinte(version, n) or verifier_analyse(version, n, decisions):
            continue
        resultat.append(n)
    return resultat


def prochain_relecture(version, preparation, tout):
    numeros = a_relire(version, preparation, tout)
    if not numeros:
        print("Aucune analyse à relire" + ("." if tout else " parmi celles de ce passage."))
        return
    print(f"{len(numeros)} analyse(s) à relire par l'agent « Relecteur analyse » (numéro | relire | sujet) :")
    for n in numeros:
        print(f"  {n} | relire | {lire_ticket(version, n)['sujet']}")


MOTS_COURANTS = set("""
avec dans pour sans sous depuis entre lors plus moins tout toute tous toutes cette celle celui leur leurs elle elles
etre avoir fait faire peut doit doivent permettre permet possible correctement correct correction corriger ajout ajouter
ajoute probleme erreur erreurs nouveau nouvelle nouvelles nouveaux mise jour version versions fonctionne fonctionnement
utilisation utiliser utilisateur utilisateurs compte comptes parametre parametres affichage afficher affiche gestion
webapp winapp desktopapp mobileapp isap smart shield egidium serveur application applications donnees systeme
apres avant lorsque quand impossible toujours encore aussi ayant existe cause suite desire
""".split())
PART_MAX = 0.3   # un terme présent dans plus de 30 % des sections ne distingue aucune fiche


def ascii_minuscule(texte):
    return unicodedata.normalize("NFKD", texte or "").encode("ascii", "ignore").decode().lower()


def termes_du_ticket(version, numero):
    """(mots du sujet, termes techniques du sujet et de la description) pour chercher les fiches candidates."""
    issue = json.loads((TICKETS / version / str(numero) / "ticket.json").read_text(encoding="utf-8"))["issue"]
    sujet = issue.get("subject", "")
    texte = re.sub(r"https?://\S+|\S+\.(?:png|jpg|jpeg|gif|pdf|zip|log|txt)\b", " ", sujet + "\n" + (issue.get("description") or ""))
    mots = []
    for m in re.findall(r"[a-z0-9]+", ascii_minuscule(sujet)):
        racine = m[:-1] if len(m) > 5 and m.endswith(("s", "x")) else m
        if len(racine) >= 5 and m not in MOTS_COURANTS and racine not in MOTS_COURANTS and racine not in mots:
            mots.append(racine)
    techniques = []
    for m in re.findall(r"\b(?:[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+|[a-z]+[A-Z][A-Za-z0-9]*|[A-Z][a-z0-9]+[A-Z][A-Za-z0-9]*)\b", texte):
        if len(m) >= 6 and m.lower() not in MOTS_COURANTS and m.lower() not in (t.lower() for t in techniques):
            techniques.append(m)
    for m in re.findall(r"\b[A-Z][A-Z0-9]{2,}\b", sujet):     # sigles du sujet : CGU, SIA, SSO, PTZ…
        if m.lower() not in MOTS_COURANTS and m.lower() not in (t.lower() for t in techniques):
            techniques.append(m)
    return mots, techniques[:15]


def sections_des_plans():
    """Sections de tous les plans : plan, chemin des titres, fiche englobante, texte."""
    sections = []
    for fichier in sorted((DOSSIER / "referentiel" / "plans").glob("*.md")):
        texte = fichier.read_text(encoding="utf-8")
        ids = [(m.start(), f"{m.group(1)} — {m.group(2).strip()}")
               for m in re.finditer(rf"ID\s*:\s*({MOTIF_ID})\b[\s\S]{{0,300}}?Titre\s*:\s*([^|\n·*]+)", texte)]
        bornes, chemin = [], []
        for m in re.finditer(r"(?m)^(#+)\s+(.+)$", texte):
            niveau = len(m.group(1))
            chemin = chemin[:niveau - 1] + [m.group(2).strip()]
            bornes.append((m.start(), " > ".join(chemin)))
        bornes = [(p, " > ".join(x.strip()[:70] for x in re.sub(r"\s+", " ", re.sub(r"_\[image\]_", "", c)).split(" > ")))
                  for p, c in bornes]
        bornes.append((len(texte), ""))
        if bornes[0][0] > 0:
            bornes.insert(0, (0, ""))
        for (debut, titre), (fin, _) in zip(bornes, bornes[1:]):
            dedans = [f for p, f in ids if debut <= p < fin]
            avant = [f for p, f in ids if p < debut]
            sections.append({"plan": fichier.name, "numero": fichier.name[:2], "chemin": titre,
                             "fiche": dedans[0] if dedans else (avant[-1] if avant else "(sans fiche)"),
                             "debut": debut, "texte": texte[debut:fin]})
    return sections


def plans_proposes(fonction):
    """Numéros des plans proposés par correspondance-fonctions.md pour cette Fonction, et la ligne de la table."""
    chemin = DOSSIER / "referentiel" / "correspondance-fonctions.md"
    if not chemin.exists():
        return [], ""
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cellules) >= 5 and normaliser(cellules[0]) == normaliser(fonction or "(vide)"):
            return re.findall(r"\b(\d{2})\b", cellules[2]), ligne.strip()
    return [], ""


def statut_decision(d):
    if d["appliquee"]:
        return f"appliquée le {d['appliquee']} — à respecter dans toute réécriture"
    if not d["decision"]:
        return "en attente de l'humain — ne rien appliquer"
    raison = refus_decision(d)
    if raison:
        return f"à reformuler par l'humain ({raison}) — ne pas appliquer"
    return "À APPLIQUER pendant ce passage"


def contexte(version, numero, relire=False):
    if numero not in selection_courante(version):
        sys.exit(f"#{numero} n'est pas dans la sélection de {version}.")
    chemin = ANALYSES / version / f"{numero}.md"
    with verrou(version):
        preparation = preparation_valide(version)
        if relire:
            _, decisions = lire_decisions(version)
            if not chemin.exists() or verifier_analyse(version, numero, decisions):
                sys.exit(f"#{numero} : seule une analyse conforme se relit. Rendre la main.")
            if numero in preparation["relus"]:
                sys.exit(f"#{numero} : déjà ouvert en relecture pendant ce passage. Rendre la main.")
            preparation["relus"].append(numero)
            ecrire_preparation(version, preparation)
            mode, essai = "relecture", 1
        else:
            file, _, _ = file_de_travail(version)
            entree = next((e for e in file if e["ticket"]["id"] == numero), None)
            if entree:
                mode = entree["mode"]
            elif preparation.get("force") == numero:
                mode = "reprendre" if chemin.exists() else "analyser"
            else:
                print(f"#{numero} : analyse à jour, rien à faire pendant ce passage. Rendre la main en le signalant.")
                return
            essai = ouvrir_ticket(version, numero, mode)

    issue = json.loads((TICKETS / version / str(numero) / "ticket.json").read_text(encoding="utf-8"))["issue"]
    ticket = lire_ticket(version, numero)
    sortie = [f"=== Contexte #{numero} — {ticket['sujet']} ===", ""]
    sortie.append(f"Mode : {mode}" + ("" if mode == "relecture" else f" (essai {essai} sur {ESSAIS_MAX})"))
    sortie += [
        "",
        "## Ticket",
        f"- Fichier : tickets/{version}/{numero}/ticket.md (à lire en entier, historique compris)",
        f"- Tracker : {ticket['tracker']} | Statut : {(issue.get('status') or {}).get('name', '')} | "
        f"Fonction : {ticket['fonction'] or '(vide)'} | Assigné à : {(issue.get('assigned_to') or {}).get('name', '—')}",
        f"- Valeur exacte de « mis à jour » pour l'en-tête de l'analyse : {ticket['mis_a_jour']}",
        f"- Commentaires dans l'historique : {sum(1 for j in issue.get('journals', []) if (j.get('notes') or '').strip())} | "
        f"Pièces jointes : {len(issue.get('attachments', []))}",
    ]

    _, decisions = lire_decisions(version)
    lignes = [d for d in decisions if d["ticket"] == numero]
    sortie += ["", "## Décisions de ce ticket dans decisions.md"]
    if lignes:
        for d in lignes:
            libelle = "Remarque de relecture" if est_relecture(d) else "Question"
            sortie.append(f"- {libelle} : {d['question'] if not est_relecture(d) else d['proposition']}")
            if not est_relecture(d):
                sortie.append(f"  Proposition : {d['proposition']}")
            sortie.append(f"  Décision : {d['decision'] or '(vide)'} → {statut_decision(d)}")
    else:
        sortie.append("- Aucune.")

    proposes, ligne_table = plans_proposes(ticket["fonction"])
    sortie += ["", "## Correspondance (referentiel/correspondance-fonctions.md)"]
    sortie.append(f"- {ligne_table}" if ligne_table else "- Fonction absente de la table : règle 3 (proposition et question).")
    prefixe = re.match(r"\s*(\[[^\]]+\]|[A-Za-z]+\s*:)", ticket["sujet"])
    if prefixe:
        sortie.append(f"- Préfixe du sujet « {prefixe.group(1)} » : la règle 1 le fait primer sur la Fonction.")

    sections = sections_des_plans()
    occurrences = []
    for s in sections:
        for m in re.finditer(rf"#{numero}\b", s["texte"]):
            debut = s["texte"].rfind("\n", 0, m.start()) + 1
            fin = s["texte"].find("\n", m.end())
            extrait = re.sub(r"\s+", " ", s["texte"][debut:fin if fin > 0 else None]).strip()
            occurrences.append(f"- Plan {s['numero']} | {s['fiche']} | {s['chemin']} | « {extrait[:160]} »")
    sortie += ["", f"## Occurrences de #{numero} dans les plans"]
    sortie += occurrences[:12] or ["- Aucune occurrence."]
    if len(occurrences) > 12:
        sortie.append(f"- … et {len(occurrences) - 12} autre(s).")
    tests = lire_couverture().get("tickets", {}).get(str(numero), [])
    sortie.append("- Tests Playwright citant le ticket : " +
                  ("; ".join(f"{t['fichier']} « {t['titre']} »" for t in tests[:5]) if tests else "aucun"))

    mots, techniques = termes_du_ticket(version, numero)
    for s in sections:
        s["brut"] = (s["chemin"] + "\n" + s["texte"]).lower()
        s["plat"] = ascii_minuscule(s["chemin"] + "\n" + s["texte"])

    def present_m(m, s):
        return re.search(rf"\b{re.escape(m)}", s["plat"])

    def present_t(t, s):
        return re.search(rf"(?<![a-z0-9]){re.escape(t.lower())}" if len(t) <= 4 else re.escape(t.lower()), s["brut"])

    # Poids d'un terme : plus il est rare dans les plans, plus il désigne une fiche précise.
    sections = [s for s in sections if s["fiche"] != "(sans fiche)"]
    total = len(sections) or 1
    poids, frequents = {}, []
    for terme, present, facteur in [(m, present_m, 1) for m in mots] + [(t, present_t, 2) for t in techniques]:
        df = sum(1 for s in sections if present(terme, s))
        if df > PART_MAX * total:
            frequents.append(terme)
        elif df:
            poids[terme] = facteur * math.log(total / df)
    mots = [m for m in mots if m not in frequents]
    techniques = [t for t in techniques if t not in frequents]
    candidates = []
    for s in sections:
        trouves = [m for m in mots if m in poids and present_m(m, s)] + [t for t in techniques if t in poids and present_t(t, s)]
        score = sum(poids[t] for t in trouves) * (1.2 if s["numero"] in proposes else 1)
        if score > 0:
            candidates.append((score, s, trouves))
    candidates.sort(key=lambda c: (-c[0], c[1]["numero"] not in proposes, c[1]["plan"], c[1]["debut"]))
    sortie += ["", "## Fiches candidates (recherche par mots-clés, à vérifier en lisant le plan)"]
    sortie.append(f"- Mots du sujet : {', '.join(mots) or 'aucun'} | Termes techniques : {', '.join(techniques) or 'aucun'}"
                  + (f" | Écartés car trop fréquents dans les plans : {', '.join(frequents)}" if frequents else ""))
    sortie.append(f"- Plans proposés par la correspondance : {', '.join(proposes) or 'aucun'}")
    for score, s, trouves in candidates[:8]:
        marque = " (plan proposé)" if s["numero"] in proposes else ""
        sortie.append(f"- Plan {s['numero']}{marque} | {s['fiche']} | {s['chemin']} | termes : {', '.join(trouves)}")
    if not candidates:
        sortie.append("- Aucune section ne recoupe les termes du ticket : chercher d'autres mots-clés dans la description.")
    sortie.append("Cette liste oriente la recherche ; elle ne la remplace pas. Toute fiche retenue ou écartée se justifie "
                  "en section 3 après lecture du plan.")

    sortie += ["", "## Suite"]
    if mode == "appliquer":
        sortie.append(f"Appliquer chaque décision « À APPLIQUER » à analyses/{version}/{numero}.md, puis lancer "
                      f"python analyses.py appliquer --ticket {numero}.")
    elif mode == "reprendre":
        if chemin.exists():
            sortie.append(f"Lancer python analyses.py reprendre --ticket {numero}, puis rédiger une analyse entièrement neuve.")
        else:
            sortie.append("L'analyse est déjà archivée : rédiger une analyse entièrement neuve.")
        sortie.append("Les décisions « appliquée » et « À APPLIQUER » ci-dessus s'imposent à la nouvelle analyse ; "
                      f"s'il y en a « À APPLIQUER », terminer par python analyses.py appliquer --ticket {numero}.")
    elif mode == "analyser":
        sortie.append(f"Rédiger analyses/{version}/{numero}.md selon referentiel/methode-analyse.md.")
    else:
        sortie.append(f"Relire analyses/{version}/{numero}.md selon la grille, puis conclure par "
                      f"python analyses.py relecture --ticket {numero} --texte \"…\" (une remarque par appel) ou --aucune.")
    print("\n".join(sortie))


def relecture(version, numero, texte, aucune):
    if bool(texte) == bool(aucune):
        sys.exit("Préciser soit --texte \"remarque\", soit --aucune.")
    with verrou(version):
        preparation = preparation_valide(version)
        if numero not in preparation["relus"]:
            sys.exit(f"Lancer d'abord python analyses.py contexte --ticket {numero} --relecture.")
        _, decisions = lire_decisions(version)
        if verifier_analyse(version, numero, decisions):
            sys.exit(f"#{numero} : l'analyse n'est pas conforme, elle ne se relit pas.")
        if texte:
            if any(d["ticket"] == numero and est_relecture(d) and not d["decision"]
                   and normaliser(d["proposition"]) == normaliser(texte) for d in decisions):
                sys.exit("Cette remarque est déjà en attente : ne pas la répéter.")
            ajouter_ligne_decision(version, numero, "Relecture", texte)
        relectures = lire_relectures(version)
        relectures[str(numero)] = empreinte(version, numero)
        chemin_relectures(version).write_text(json.dumps(relectures, indent=1, sort_keys=True), encoding="utf-8")
    print(f"#{numero} : " + ("remarque inscrite dans decisions.md." if texte else "relu, aucune remarque."))


def validations_sans_reponse(decisions):
    """Décisions « valider » déjà appliquées sur une proposition qui renvoyait la question, sans relecture ensuite."""
    resultat = []
    for i, d in enumerate(decisions):
        if d["appliquee"] and forme_decision(d["decision"]) == "valider" and raison_proposition_invalidable(d["proposition"]):
            if not any(e["ticket"] == d["ticket"] and est_relecture(e) for e in decisions[i + 1:]):
                resultat.append(d)
    return resultat


def bilan(version):
    preparation = lire_preparation(version) or {"essais": {}, "tickets": [], "modes": {}, "relus": [], "lot": 0,
                                                "date": datetime.now()}
    numeros = selection_courante(version)
    file, a_jour, inconnues = file_de_travail(version)
    essais = preparation["essais"]
    abandonnes = [e for e in file if essais.get(str(e["ticket"]["id"]), 0) >= ESSAIS_MAX]
    restants = [e for e in file if essais.get(str(e["ticket"]["id"]), 0) < ESSAIS_MAX]
    lot = preparation.get("lot") or 0
    if lot and len(preparation["tickets"]) >= lot:
        restants = [e for e in restants if e["ticket"]["id"] in preparation["tickets"]]
    if preparation.get("force"):            # passage limité à un ticket (paramètre ticket=)
        restants = [e for e in restants if e["ticket"]["id"] == preparation["force"]]
    _, decisions = lire_decisions(version)
    en_attente = [d for d in decisions if not d["decision"]]
    remarques = [d for d in en_attente if est_relecture(d)]
    relire = a_relire(version, preparation, False) if lire_preparation(version) else []
    sans_reponse = validations_sans_reponse(decisions)
    modes = Counter(preparation["modes"].values())

    print(f"=== Bilan du passage — {version} ===")
    print(f"Passage ouvert le {preparation['date'].strftime('%d/%m/%Y %H:%M')}"
          + (f", lot de {lot} ticket(s)" if lot else ", sans limite de tickets"))
    print(f"Tickets ouverts par les agents : {len(preparation['tickets'])} ("
          + ", ".join(f"{m} : {n}" for m, n in sorted(modes.items())) + ")" if modes else
          "Tickets ouverts par les agents : 0")
    print(f"Sélection : {len(numeros)} | Analyses à jour : {len(a_jour)} | Encore à traiter : {len(file)}")
    if abandonnes:
        print(f"Laissés à l'humain après {ESSAIS_MAX} essais : " + ", ".join(f"#{e['ticket']['id']} ({e['motif']})" for e in abandonnes))
    print(f"Relecture : {len(preparation['relus'])} analyse(s) relue(s) pendant le passage, "
          f"{len(remarques)} remarque(s) en attente de décision")
    print(f"Décisions en attente de l'humain : {len(en_attente)}" + (" → python analyses.py trancher" if en_attente else ""))
    if inconnues:
        print("Décisions à reformuler : " + ", ".join(f"#{d['ticket']} ({refus_decision(d)})" for d in inconnues))
    if sans_reponse:
        print("Validations passées sans réponse (la proposition renvoyait la question) : "
              + ", ".join(f"#{d['ticket']}" for d in sans_reponse)
              + ". Ajouter pour chacune une ligne « | #N | Relecture | — | corriger : <réponse> |  | » dans decisions.md.")
    print()
    synthese(version)
    exporter(version)
    print()
    if restants or relire:
        if restants:
            print("RESTE À TRAITER PAR LES AGENTS : " + ", ".join(f"#{e['ticket']['id']} ({e['mode']})" for e in restants))
        if relire:
            print("RESTE À RELIRE : " + ", ".join(f"#{n}" for n in relire))
        print("Relancer python analyses.py prochain (ou prochain --relecture) et confier ces tickets aux agents.")
        sys.exit(1)
    print("Passage terminé : plus rien à confier aux agents.")


# --------------------------------------------------------------------------
# Décisions humaines : trancher
# --------------------------------------------------------------------------

def ecrire_decision(version, d, decision):
    """Remplit la cellule Décision de la ligne d (identifiée par ticket, question, proposition, décision actuelle)."""
    with verrou(version):
        chemin = chemin_decisions(version)
        lignes = chemin.read_text(encoding="utf-8").splitlines()
        for i, ligne in enumerate(lignes):
            c = [x.strip() for x in ligne.strip().strip("|").split("|")]
            if (len(c) >= 5 and c[0] == f"#{d['ticket']}" and c[1] == d["question"] and c[2] == d["proposition"]
                    and c[3] == d["decision"] and not c[4]):
                lignes[i] = f"| {c[0]} | {c[1]} | {c[2]} | {nettoyer(decision)} |  |"
                chemin.write_text("\n".join(lignes) + "\n", encoding="utf-8")
                return True
    return False


def fiches_connues(identifiant):
    """Fiches de tous les plans portant cet identifiant (« plan : ID — titre »)."""
    trouvees = []
    for fichier in sorted((DOSSIER / "referentiel" / "plans").glob("*.md")):
        for f in fiches_du_plan(fichier.name[:2]):
            if f["identifiant"] == identifiant and f"{fichier.name[:2]} : {f['fiche']}" not in trouvees:
                trouvees.append(f"{fichier.name[:2]} : {f['fiche']}")
    return trouvees


def trancher(version, numero=None):
    if not sys.stdin.isatty():
        sys.exit("python analyses.py trancher est réservée à l'humain : la lancer soi-même dans un terminal.")
    conforme, decisions = lire_decisions(version)
    if not conforme:
        sys.exit("decisions.md n'a pas le format attendu : lancer python analyses.py reparer-decisions, puis relancer.")
    items = [d for d in decisions if not d["decision"] or (not d["appliquee"] and refus_decision(d))]
    if numero:
        items = [d for d in items if d["ticket"] == numero]
    if not items:
        print("Aucune décision en attente.")
        return
    enregistrees = 0
    print(f"{len(items)} décision(s) à prendre. Les choix sont enregistrés au fur et à mesure.")
    try:
        for rang, d in enumerate(items, 1):
            try:
                sujet = lire_ticket(version, d["ticket"])["sujet"]
            except (OSError, ValueError, KeyError):
                sujet = ""
            print()
            print(f"[{rang}/{len(items)}] #{d['ticket']} — {sujet}")
            print(f"Analyse : analyses/{version}/{d['ticket']}.md")
            if est_relecture(d):
                print(f"Remarque du relecteur : {d['proposition']}")
            else:
                print(f"Question : {d['question']}")
                print(f"Proposition de l'agent : {d['proposition']}")
            if d["decision"]:
                print(f"Décision actuelle « {d['decision']} » refusée : {refus_decision(d)}")
            raison_v = raison_proposition_invalidable(d["proposition"])
            print("  v valider" + (f" (indisponible : {raison_v})" if raison_v else " la proposition telle quelle"))
            print("  c corriger : saisir la réponse   f fiche : saisir la fiche   n nouveau plan : saisir l'intitulé")
            print("  r réanalyser   h hors campagne   i ignorer   s passer   q quitter")
            while True:
                choix = input("Choix : ").strip().lower()[:1]
                if choix == "q":
                    raise KeyboardInterrupt
                if choix == "s":
                    break
                if choix == "v":
                    if raison_v:
                        print(f"Impossible : {raison_v}")
                        continue
                    decision = "valider"
                elif choix == "c":
                    texte = input("Réponse, telle que l'agent doit l'appliquer : ").strip()
                    if not texte:
                        continue
                    decision = "corriger : " + texte
                elif choix == "f":
                    texte = input("Fiche (identifiant — titre, tels que dans le plan) : ").strip()
                    if not texte:
                        continue
                    ident = re.match(rf"\s*({MOTIF_ID})\b", texte)
                    if ident:
                        connues = fiches_connues(ident.group(1))
                        if connues:
                            print("Fiches de cet identifiant dans les plans : " + " ; ".join(connues))
                        else:
                            print(f"Attention : {ident.group(1)} n'apparaît dans aucun plan converti.")
                        if input("Confirmer cette fiche ? (o/n) ").strip().lower()[:1] != "o":
                            continue
                    decision = "fiche : " + texte
                elif choix == "n":
                    texte = input("Intitulé du plan à créer : ").strip()
                    if not texte:
                        continue
                    decision = "nouveau plan : " + texte
                elif choix == "r":
                    texte = input("Consigne pour la nouvelle analyse (Entrée pour aucune) : ").strip()
                    decision = "réanalyser" + (" : " + texte if texte else "")
                elif choix == "h":
                    decision = "hors campagne"
                elif choix == "i":
                    decision = "ignorer"
                else:
                    print("Choix non reconnu.")
                    continue
                if ecrire_decision(version, d, decision):
                    enregistrees += 1
                    print(f"Enregistré : {nettoyer(decision)}")
                else:
                    print("Ligne introuvable (decisions.md modifié entre-temps) : relancer trancher.")
                break
    except (KeyboardInterrupt, EOFError):
        print()
    print(f"{enregistrees} décision(s) enregistrée(s) dans decisions.md. Relancer /analyser-tickets pour les faire appliquer.")


def main():
    analyseur = argparse.ArgumentParser(description="Suivi et contrôle des analyses de tickets.")
    analyseur.add_argument("commande", choices=["etat", "verifier", "question", "journal", "synthese", "reparer-decisions",
                                                "preparer", "reprendre", "appliquer", "exporter", "couverture",
                                                "prochain", "contexte", "relecture", "bilan", "trancher"])
    analyseur.add_argument("--relecture", action="store_true", help="analyses à relire (prochain) ou ouverture en relecture (contexte)")
    analyseur.add_argument("--tout", action="store_true", help="toutes les analyses, pas seulement celles du passage (prochain --relecture)")
    analyseur.add_argument("--aucune", action="store_true", help="relecture sans remarque (commande relecture)")
    analyseur.add_argument("--nouveau", action="store_true", help="ouvre un nouveau passage même si le précédent a moins de 12 h (commande preparer, humain seulement)")
    analyseur.add_argument("--version", help="version à traiter (ex. ISAP-V27.1)")
    analyseur.add_argument("--ticket", type=int, help="numéro du ticket")
    analyseur.add_argument("--question", help="question à trancher (commande question)")
    analyseur.add_argument("--proposition", help="proposition de l'agent (commande question)")
    analyseur.add_argument("--texte", help="texte de la ligne de journal (journal) ou de la remarque (relecture)")
    analyseur.add_argument("--lot", type=int, help="nombre maximal de tickets ouverts pendant le passage, sans limite par défaut (commande preparer)")
    analyseur.add_argument("--depuis", help="rapport Playwright HTML ou JSON à lire (commande couverture)")
    analyseur.add_argument("--max", type=int, help="nombre de lignes de la liste « À analyser » affichées (commande etat)")
    args = analyseur.parse_args()
    if args.commande == "preparer":
        preparer(args.version, args.lot, args.nouveau)
        return
    version = choisir_version(args.version)

    if args.commande in ("question", "journal", "reprendre", "appliquer", "contexte", "relecture") and not args.ticket:
        sys.exit("Préciser --ticket.")
    if args.commande == "prochain":
        prochain(version, args.ticket, args.relecture, args.tout)
    elif args.commande == "contexte":
        contexte(version, args.ticket, args.relecture)
    elif args.commande == "relecture":
        relecture(version, args.ticket, args.texte, args.aucune)
    elif args.commande == "bilan":
        bilan(version)
    elif args.commande == "trancher":
        trancher(version, args.ticket)
    elif args.commande == "etat":
        etat(version, args.max)
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
    elif args.commande == "couverture":
        couverture(version, args.depuis)
    elif args.commande == "exporter":
        exporter(version)
    elif args.commande == "reparer-decisions":
        reparer_decisions(version)
    else:
        synthese(version)


if __name__ == "__main__":
    main()
