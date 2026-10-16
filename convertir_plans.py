#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversion des plans de validation Word (.docx) en Markdown, pour que l'agent puisse les lire.

Les plans Word restent la source de vérité. Les fichiers Markdown produits dans
referentiel/plans/ sont des copies de lecture : ils sont régénérés à chaque conversion
et ne doivent pas être modifiés à la main.

Utilisation (depuis le dossier Redmine_Automation) :
    python convertir_plans.py          convertit les plans modifiés depuis la dernière conversion
    python convertir_plans.py --tout   reconvertit tous les plans

Paramètre lu dans le fichier .env :
    PLANS_WORD_DIR   dossier des plans de validation Word (fichiers .docx numérotés de 00 à 99)

Le script n'utilise que la bibliothèque standard de Python.
"""

import argparse
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent
SORTIE = DOSSIER / "referentiel" / "plans"

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def charger_env(chemin: Path) -> None:
    if not chemin.exists():
        return
    for ligne in chemin.read_text(encoding="utf-8-sig").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#") or "=" not in ligne:
            continue
        cle, valeur = ligne.split("=", 1)
        os.environ[cle.strip()] = valeur.strip().strip('"').strip("'")


# --------------------------------------------------------------------------
# Lecture du document Word
# --------------------------------------------------------------------------

def noms_des_styles(archive):
    """Correspondance identifiant de style -> nom (ex. Titre1 -> heading 1)."""
    try:
        racine = ET.fromstring(archive.read("word/styles.xml"))
    except KeyError:
        return {}
    noms = {}
    for style in racine.iter(W + "style"):
        identifiant = style.get(W + "styleId")
        nom = style.find(W + "name")
        if identifiant and nom is not None:
            noms[identifiant] = nom.get(W + "val", "")
    return noms


def niveau_de_titre(paragraphe, styles):
    ppr = paragraphe.find(W + "pPr")
    if ppr is None:
        return 0
    style = ppr.find(W + "pStyle")
    if style is not None:
        identifiant = style.get(W + "val", "")
        for libelle in (styles.get(identifiant, ""), identifiant):
            trouve = re.search(r"(?:heading|titre)\s*(\d)", libelle, re.IGNORECASE)
            if trouve:
                return min(int(trouve.group(1)), 6)
            if libelle.lower() in ("title", "titre"):
                return 1
    niveau = ppr.find(W + "outlineLvl")
    if niveau is not None:
        try:
            return min(int(niveau.get(W + "val", "9")) + 1, 6)
        except ValueError:
            return 0
    return 0


def est_element_de_liste(paragraphe, styles):
    ppr = paragraphe.find(W + "pPr")
    if ppr is None:
        return False
    if ppr.find(W + "numPr") is not None:
        return True
    style = ppr.find(W + "pStyle")
    if style is not None:
        libelle = (styles.get(style.get(W + "val", ""), "") + " " + style.get(W + "val", "")).lower()
        return "list" in libelle or "liste" in libelle
    return False


def texte_du_paragraphe(paragraphe):
    morceaux = []
    for element in paragraphe.iter():
        if element.tag == W + "t":
            morceaux.append(element.text or "")
        elif element.tag in (W + "tab",):
            morceaux.append(" ")
        elif element.tag in (W + "br", W + "cr"):
            morceaux.append(" ")
        elif element.tag == W + "drawing" or element.tag.endswith("}pict"):
            morceaux.append(" _[image]_ ")
    return re.sub(r"[  ]+", " ", "".join(morceaux)).strip()


def texte_de_cellule(cellule):
    lignes = [texte_du_paragraphe(p) for p in cellule.iter(W + "p")]
    return " ".join(l for l in lignes if l).replace("|", "\\|")


def convertir_tableau(tableau):
    lignes = []
    for rangee in tableau.findall(W + "tr"):
        cellules = [texte_de_cellule(c) for c in rangee.findall(W + "tc")]
        if any(cellules):
            lignes.append(cellules)
    if not lignes:
        return []
    largeur = max(len(l) for l in lignes)
    lignes = [l + [""] * (largeur - len(l)) for l in lignes]
    sortie = ["| " + " | ".join(lignes[0]) + " |", "|" + "---|" * largeur]
    sortie += ["| " + " | ".join(l) + " |" for l in lignes[1:]]
    return [""] + sortie + [""]


def parcourir(conteneur, styles, sortie):
    for enfant in conteneur:
        if enfant.tag == W + "p":
            texte = texte_du_paragraphe(enfant)
            if not texte:
                continue
            niveau = niveau_de_titre(enfant, styles)
            if niveau:
                sortie += ["", "#" * niveau + " " + texte, ""]
            elif est_element_de_liste(enfant, styles):
                sortie.append("- " + texte)
            else:
                sortie.append(texte)
        elif enfant.tag == W + "tbl":
            sortie += convertir_tableau(enfant)
        elif enfant.tag == W + "sdt":
            contenu = enfant.find(W + "sdtContent")
            if contenu is not None:
                parcourir(contenu, styles, sortie)


def convertir(fichier_word: Path) -> str:
    with zipfile.ZipFile(fichier_word) as archive:
        styles = noms_des_styles(archive)
        racine = ET.fromstring(archive.read("word/document.xml"))
    corps = racine.find(W + "body")
    lignes = []
    if corps is not None:
        parcourir(corps, styles, lignes)
    texte = "\n".join(lignes)
    texte = re.sub(r"\n{3,}", "\n\n", texte).strip()
    entete = (
        f"# {fichier_word.stem}\n\n"
        f"> Conversion automatique de `{fichier_word.name}` le {datetime.now().strftime('%d/%m/%Y %H:%M')}. "
        f"Copie de lecture : ne pas modifier, le plan Word fait foi.\n\n"
    )
    return entete + texte + "\n"


# --------------------------------------------------------------------------
# Programme principal
# --------------------------------------------------------------------------

def main():
    analyseur = argparse.ArgumentParser(description="Convertit les plans de validation Word en Markdown.")
    analyseur.add_argument("--tout", action="store_true", help="reconvertit tous les plans, même inchangés")
    args = analyseur.parse_args()

    charger_env(DOSSIER / ".env")
    dossier_word = os.environ.get("PLANS_WORD_DIR", "").strip()
    if not dossier_word:
        sys.exit("Paramètre manquant dans le .env : PLANS_WORD_DIR (dossier des plans de validation Word).")
    dossier_word = Path(dossier_word)
    if not dossier_word.is_dir():
        sys.exit(f"Dossier introuvable : {dossier_word}")

    # Les plans se reconnaissent à leur numéro en tête de nom (00 à 99), quelle que soit la suite :
    # « 01 V26.1 - WEBAPP », « 03_Plan de validation V25.1 - WINAPP_VIDEO », « 14_PdV 25.1 - ... ».
    plans = sorted(
        f for f in dossier_word.glob("*.docx")
        if re.match(r"\d{2}[ _-]", f.name) and not f.name.startswith("~$")
    )
    if not plans:
        sys.exit(f"Aucun plan .docx numéroté (00 à 99) dans {dossier_word}")

    SORTIE.mkdir(parents=True, exist_ok=True)
    convertis = inchanges = 0
    echecs = []
    for plan in plans:
        cible = SORTIE / (plan.stem + ".md")
        if not args.tout and cible.exists() and cible.stat().st_mtime >= plan.stat().st_mtime:
            inchanges += 1
            continue
        try:
            cible.write_text(convertir(plan), encoding="utf-8")
            convertis += 1
            print(f"  converti : {plan.name}")
        except (zipfile.BadZipFile, KeyError, ET.ParseError, OSError) as erreur:
            echecs.append(f"{plan.name} : {erreur}")

    print()
    print(f"Plans convertis : {convertis} | Inchangés : {inchanges}")
    print(f"Dossier : {SORTIE}")
    if echecs:
        print(f"Échecs ({len(echecs)}) :")
        for ligne in echecs:
            print(f"  {ligne}")
        sys.exit(1)


if __name__ == "__main__":
    main()
    