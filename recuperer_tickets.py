#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Récupération des tickets Redmine à tester pour une version donnée.

Utilisation (depuis le dossier Redmine_Automation) :
    python recuperer_tickets.py          met à jour les tickets modifiés depuis le dernier passage
    python recuperer_tickets.py --tout   récupère de nouveau tous les tickets de la sélection

Paramètres lus dans le fichier .env placé à côté du script :
    REDMINE_URL                  adresse du Redmine (ex. https://srvfr-redmine)
    REDMINE_API_KEY              clé d'accès API (« Mon compte » dans Redmine)
    REDMINE_VERSION_ID           identifiant de la version cible (67 = ISAP-V27.1)
Facultatifs (valeur par défaut entre parenthèses) :
    REDMINE_PROJET               identifiant du projet (isapv2)
    REDMINE_STATUT_ID            statut des tickets à tester (3 = Résolu)
    REDMINE_EXCLURE_ASSIGNE_ID   utilisateur dont les tickets sont exclus (21) ; vide = aucune exclusion
    REDMINE_PJ_TAILLE_MAX_MO     taille maximale d'une pièce jointe téléchargée, en Mo (20)
    REDMINE_CA_FILE              certificat d'autorité à utiliser si celui du serveur n'est pas reconnu

Le script n'utilise que la bibliothèque standard de Python : aucune installation n'est nécessaire.
"""

import argparse
import json
import os
import re
import shutil
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

DOSSIER = Path(__file__).resolve().parent

LIBELLES = {
    "status_id": "Statut",
    "tracker_id": "Tracker",
    "priority_id": "Priorité",
    "assigned_to_id": "Assigné à",
    "fixed_version_id": "Version cible",
    "category_id": "Catégorie",
    "project_id": "Projet",
    "done_ratio": "Avancement",
    "subject": "Sujet",
    "description": "Description",
    "start_date": "Début",
    "due_date": "Échéance",
    "estimated_hours": "Temps estimé",
    "parent_id": "Ticket parent",
    "is_private": "Privé",
}

RELATIONS = {
    "relates": "liée à",
    "duplicates": "duplique",
    "duplicated": "dupliquée par",
    "blocks": "bloque",
    "blocked": "bloquée par",
    "precedes": "précède",
    "follows": "suit",
    "copied_to": "copiée vers",
    "copied_from": "copiée depuis",
}

RELATIONS_INVERSES = {
    "relates": "relates",
    "duplicates": "duplicated",
    "duplicated": "duplicates",
    "blocks": "blocked",
    "blocked": "blocks",
    "precedes": "follows",
    "follows": "precedes",
    "copied_to": "copied_from",
    "copied_from": "copied_to",
}


# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

def charger_env(chemin: Path) -> None:
    """Charge le .env dans les variables d'environnement. Le fichier fait foi."""
    if not chemin.exists():
        return
    for ligne in chemin.read_text(encoding="utf-8-sig").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#") or "=" not in ligne:
            continue
        cle, valeur = ligne.split("=", 1)
        os.environ[cle.strip()] = valeur.strip().strip('"').strip("'")


def parametre(nom, defaut=None, obligatoire=False):
    valeur = os.environ.get(nom, "").strip()
    if not valeur:
        if obligatoire:
            sys.exit(f"Paramètre manquant dans le .env : {nom}")
        return defaut
    return valeur


# --------------------------------------------------------------------------
# Accès Redmine
# --------------------------------------------------------------------------

class Redmine:
    def __init__(self, url, cle, ca_file=None):
        self.url = url.rstrip("/")
        self.cle = cle
        contexte = ssl.create_default_context(cafile=ca_file) if ca_file else ssl.create_default_context()
        # Serveur interne : connexion directe, sans passer par un éventuel proxy système.
        self.opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({}),
            urllib.request.HTTPSHandler(context=contexte),
        )

    def _requete(self, chemin, params=None, accept=None):
        url = self.url + chemin
        if params:
            url += "?" + urllib.parse.urlencode(params, safe="!")
        entetes = {"X-Redmine-API-Key": self.cle}
        if accept:
            entetes["Accept"] = accept
        return self.opener.open(urllib.request.Request(url, headers=entetes), timeout=60)

    def lire_json(self, chemin, params=None):
        with self._requete(chemin, params, "application/json") as reponse:
            return json.loads(reponse.read().decode("utf-8"))

    def telecharger(self, chemin, destination: Path):
        temporaire = destination.with_name(destination.name + ".part")
        with self._requete(chemin) as reponse, open(temporaire, "wb") as fichier:
            shutil.copyfileobj(reponse, fichier)
        temporaire.replace(destination)


def charger_referentiels(rm, projet):
    """Correspondances identifiant -> libellé, pour rendre l'historique lisible."""
    ref = {cle: {} for cle in LIBELLES}
    sources = [
        ("status_id", "/issue_statuses.json", "issue_statuses"),
        ("tracker_id", "/trackers.json", "trackers"),
        ("priority_id", "/enumerations/issue_priorities.json", "issue_priorities"),
        ("fixed_version_id", f"/projects/{projet}/versions.json", "versions"),
        ("category_id", f"/projects/{projet}/issue_categories.json", "issue_categories"),
    ]
    for cle, chemin, racine in sources:
        try:
            for element in rm.lire_json(chemin).get(racine, []):
                ref[cle][str(element["id"])] = element["name"]
        except urllib.error.HTTPError:
            pass  # référentiel non accessible avec ce compte : les identifiants resteront affichés
    return ref


def memoriser_libelles(ticket, ref):
    """Complète les référentiels avec les libellés présents dans le ticket.
    La liste des utilisateurs, en particulier, n'est pas accessible sans droits d'administration."""
    for champ, cle in (("status", "status_id"), ("tracker", "tracker_id"), ("priority", "priority_id"),
                       ("category", "category_id"), ("fixed_version", "fixed_version_id"), ("project", "project_id")):
        if ticket.get(champ) and "name" in ticket[champ]:
            ref[cle].setdefault(str(ticket[champ]["id"]), ticket[champ]["name"])
    personnes = ref["assigned_to_id"]
    for champ in ("author", "assigned_to"):
        if ticket.get(champ):
            personnes[str(ticket[champ]["id"])] = ticket[champ]["name"]
    for journal in ticket.get("journals", []):
        if journal.get("user"):
            personnes[str(journal["user"]["id"])] = journal["user"]["name"]
    for pj in ticket.get("attachments", []):
        if pj.get("author"):
            personnes[str(pj["author"]["id"])] = pj["author"]["name"]


def lister_tickets(rm, projet, filtre):
    tickets, decalage = [], 0
    while True:
        page = rm.lire_json(f"/projects/{projet}/issues.json", {**filtre, "limit": 100, "offset": decalage})
        tickets += page.get("issues", [])
        decalage += len(page.get("issues", []))
        if not page.get("issues") or decalage >= page.get("total_count", 0):
            return tickets


# --------------------------------------------------------------------------
# Mise en forme
# --------------------------------------------------------------------------

def date_locale(iso):
    if not iso:
        return ""
    try:
        moment = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    except ValueError:
        return iso
    if "T" not in iso:
        return moment.strftime("%d/%m/%Y")
    return moment.astimezone().strftime("%d/%m/%Y %H:%M")


def cellule(texte):
    return str(texte).replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def nom_fichier_sur(nom):
    nom = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", nom).strip(" .")
    return nom or "fichier"


def taille_lisible(octets):
    octets = octets or 0
    if octets < 1024:
        return f"{octets} o"
    if octets < 1024 * 1024:
        return f"{octets / 1024:.0f} Ko"
    return f"{octets / (1024 * 1024):.1f} Mo"


def bloc_textile(texte):
    texte = (texte or "").replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    return ["~~~textile", texte, "~~~"]


def nom_de(objet):
    return objet.get("name", "") if objet else ""


def valeur_cf(valeur):
    if isinstance(valeur, list):
        return ", ".join(str(v) for v in valeur if v)
    return valeur if valeur is not None else ""


def fonction_du_ticket(ticket):
    for champ in ticket.get("custom_fields", []):
        if champ.get("name") == "Fonction":
            return valeur_cf(champ.get("value")) or ""
    return ""


def valeur_lisible(nom, valeur, ref):
    if valeur in (None, ""):
        return "(vide)"
    if nom in ref and str(valeur) in ref[nom]:
        return ref[nom][str(valeur)]
    if nom == "done_ratio":
        return f"{valeur} %"
    if nom == "parent_id":
        return f"#{valeur}"
    if nom in ("start_date", "due_date"):
        return date_locale(valeur)
    if nom == "estimated_hours":
        return f"{valeur} h"
    return str(valeur)


def decrire_modification(detail, ref, noms_cf):
    nature, nom = detail.get("property"), detail.get("name")
    ancien, nouveau = detail.get("old_value"), detail.get("new_value")
    if nature == "attr":
        if nom == "description":
            return "Description modifiée (version actuelle en tête de fiche, versions précédentes dans ticket.json)"
        if nom == "subject":
            return f"Sujet : « {ancien} » → « {nouveau} »"
        return f"{LIBELLES.get(nom, nom)} : {valeur_lisible(nom, ancien, ref)} → {valeur_lisible(nom, nouveau, ref)}"
    if nature == "cf":
        libelle = noms_cf.get(str(nom), f"Champ personnalisé {nom}")
        return f"{libelle} : {ancien or '(vide)'} → {nouveau or '(vide)'}"
    if nature == "attachment":
        return f"Pièce jointe ajoutée : {nouveau}" if nouveau else f"Pièce jointe supprimée : {ancien}"
    if nature == "relation":
        libelle = RELATIONS.get(nom, nom)
        return f"Relation ajoutée ({libelle}) : #{nouveau}" if nouveau else f"Relation supprimée ({libelle}) : #{ancien}"
    return f"{nature} {nom} : {ancien} → {nouveau}"


def ticket_markdown(ticket, ref, url_redmine, pieces_jointes):
    numero = ticket["id"]
    noms_cf = {str(c["id"]): c["name"] for c in ticket.get("custom_fields", [])}
    lignes = [f"# #{numero} — {ticket.get('subject', '')}", ""]

    # En-tête
    entete = [
        ("Tracker", nom_de(ticket.get("tracker"))),
        ("Statut", nom_de(ticket.get("status"))),
        ("Priorité", nom_de(ticket.get("priority"))),
        ("Fonction", fonction_du_ticket(ticket)),
        ("Catégorie", nom_de(ticket.get("category"))),
        ("Version cible", nom_de(ticket.get("fixed_version"))),
        ("Ticket parent", f"#{ticket['parent']['id']}" if ticket.get("parent") else ""),
        ("Auteur", nom_de(ticket.get("author"))),
        ("Assigné à", nom_de(ticket.get("assigned_to"))),
        ("Avancement", f"{ticket.get('done_ratio', 0)} %"),
        ("Créé le", date_locale(ticket.get("created_on"))),
        ("Mis à jour le", date_locale(ticket.get("updated_on"))),
    ]
    for champ in ticket.get("custom_fields", []):
        valeur = valeur_cf(champ.get("value"))
        if champ.get("name") != "Fonction" and valeur not in ("", None):
            entete.append((champ["name"], valeur))
    entete.append(("Lien Redmine", f"{url_redmine}/issues/{numero}"))

    lignes += ["| Champ | Valeur |", "|---|---|"]
    lignes += [f"| {cellule(nom)} | {cellule(valeur)} |" for nom, valeur in entete if valeur not in ("", None)]
    lignes += ["", "## Description", ""]
    lignes += bloc_textile(ticket.get("description")) if ticket.get("description") else ["(aucune description)"]

    # Relations et sous-tickets
    relations = []
    for rel in ticket.get("relations", []):
        if rel.get("issue_id") == numero:
            type_rel, autre = rel.get("relation_type"), rel.get("issue_to_id")
        else:
            type_rel, autre = RELATIONS_INVERSES.get(rel.get("relation_type"), rel.get("relation_type")), rel.get("issue_id")
        relations.append(f"- {RELATIONS.get(type_rel, type_rel).capitalize()} #{autre}")
    for enfant in ticket.get("children", []):
        relations.append(f"- Sous-ticket #{enfant['id']} ({nom_de(enfant.get('tracker'))}) : {enfant.get('subject', '')}")
    if relations:
        lignes += ["", "## Relations", ""] + relations

    # Pièces jointes
    if ticket.get("attachments"):
        lignes += ["", "## Pièces jointes", ""]
        for pj in ticket["attachments"]:
            local, motif = pieces_jointes.get(pj["id"], (None, "non téléchargée"))
            nom = f"[{pj['filename']}](pieces_jointes/{urllib.parse.quote(local)})" if local else f"{pj['filename']} ({motif})"
            ligne = f"- {nom} — {taille_lisible(pj.get('filesize'))}, ajoutée par {nom_de(pj.get('author'))} le {date_locale(pj.get('created_on'))}"
            if pj.get("description"):
                ligne += f" — {pj['description']}"
            lignes.append(ligne)

    # Historique
    journaux = [j for j in ticket.get("journals", []) if j.get("notes") or j.get("details")]
    if journaux:
        lignes += ["", "## Historique"]
        for journal in journaux:
            titre = f"### {date_locale(journal.get('created_on'))} — {nom_de(journal.get('user'))}"
            if journal.get("private_notes"):
                titre += " (note privée)"
            lignes += ["", titre, ""]
            lignes += [f"- {decrire_modification(d, ref, noms_cf)}" for d in journal.get("details", [])]
            if journal.get("notes"):
                if journal.get("details"):
                    lignes.append("")
                lignes += bloc_textile(journal["notes"])

    return "\n".join(lignes) + "\n"


# --------------------------------------------------------------------------
# Pièces jointes
# --------------------------------------------------------------------------

def telecharger_pieces_jointes(rm, ticket, dossier, taille_max):
    """Renvoie {id : (nom local ou None, motif)} et le nombre de fichiers téléchargés."""
    resultats, deja_pris, telechargees = {}, set(), 0
    if not ticket.get("attachments"):
        return resultats, 0
    dossier_pj = dossier / "pieces_jointes"
    dossier_pj.mkdir(exist_ok=True)
    for pj in ticket["attachments"]:
        nom = nom_fichier_sur(pj["filename"])
        if nom.lower() in deja_pris:
            nom = f"{pj['id']}_{nom}"
        deja_pris.add(nom.lower())
        if (pj.get("filesize") or 0) > taille_max:
            resultats[pj["id"]] = (None, f"non téléchargée : plus de {taille_max / (1024 * 1024):.0f} Mo")
            continue
        cible = dossier_pj / nom
        try:
            if not (cible.exists() and cible.stat().st_size == pj.get("filesize")):
                rm.telecharger(f"/attachments/download/{pj['id']}/{urllib.parse.quote(pj['filename'])}", cible)
                telechargees += 1
            resultats[pj["id"]] = (nom, "")
        except (urllib.error.URLError, OSError) as erreur:
            resultats[pj["id"]] = (None, f"échec du téléchargement : {erreur}")
    return resultats, telechargees


# --------------------------------------------------------------------------
# Index de la version
# --------------------------------------------------------------------------

def ecrire_index(dossier_version, version_nom, selection, description_filtre):
    lignes = [
        f"# Tickets à tester — {version_nom}",
        "",
        f"Sélection : {description_filtre}.",
        f"Dernière récupération : {datetime.now().strftime('%d/%m/%Y %H:%M')} — {len(selection)} tickets.",
        "",
        "| Ticket | Sujet | Tracker | Fonction | Mis à jour le |",
        "|---|---|---|---|---|",
    ]
    for t in sorted(selection, key=lambda t: (fonction_du_ticket(t).lower(), t["id"])):
        lignes.append(
            f"| [#{t['id']}]({t['id']}/ticket.md) | {cellule(t.get('subject', ''))} | "
            f"{cellule(nom_de(t.get('tracker')))} | {cellule(fonction_du_ticket(t))} | "
            f"{date_locale(t.get('updated_on'))} |"
        )

    numeros = {t["id"] for t in selection}
    sortis = []
    for dossier in sorted(dossier_version.iterdir(), key=lambda d: d.name):
        if dossier.is_dir() and dossier.name.isdigit() and int(dossier.name) not in numeros:
            sujet = ""
            try:
                sujet = json.loads((dossier / "ticket.json").read_text(encoding="utf-8"))["issue"].get("subject", "")
            except (OSError, ValueError, KeyError):
                pass
            sortis.append(f"- [#{dossier.name}]({dossier.name}/ticket.md) — {sujet}")
    if sortis:
        lignes += [
            "",
            "## Tickets sortis de la sélection",
            "",
            "Ces tickets ont été récupérés lors d'un passage précédent mais ne correspondent plus au filtre "
            "(ticket repassé en cours, version modifiée, etc.). Leurs fichiers sont conservés.",
            "",
        ] + sortis

    (dossier_version / "index.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# Programme principal
# --------------------------------------------------------------------------

def main():
    analyseur = argparse.ArgumentParser(description="Récupère les tickets Redmine à tester pour une version.")
    analyseur.add_argument("--tout", action="store_true", help="récupère de nouveau tous les tickets, même inchangés")
    args = analyseur.parse_args()

    charger_env(DOSSIER / ".env")
    url = parametre("REDMINE_URL", obligatoire=True)
    cle = parametre("REDMINE_API_KEY", obligatoire=True)
    version_id = parametre("REDMINE_VERSION_ID", obligatoire=True)
    projet = parametre("REDMINE_PROJET", "isapv2")
    statut_id = parametre("REDMINE_STATUT_ID", "3")
    exclure = parametre("REDMINE_EXCLURE_ASSIGNE_ID", "21")
    taille_max = float(parametre("REDMINE_PJ_TAILLE_MAX_MO", "20")) * 1024 * 1024

    rm = Redmine(url, cle, parametre("REDMINE_CA_FILE"))
    ref = charger_referentiels(rm, projet)

    try:
        version_nom = rm.lire_json(f"/versions/{version_id}.json")["version"]["name"]
    except urllib.error.HTTPError:
        version_nom = ref["fixed_version_id"].get(version_id, f"version-{version_id}")
    dossier_version = DOSSIER / "tickets" / nom_fichier_sur(version_nom)
    dossier_version.mkdir(parents=True, exist_ok=True)

    filtre = {"status_id": statut_id, "fixed_version_id": version_id, "sort": "id"}
    if exclure:
        filtre["assigned_to_id"] = "!" + exclure
    selection = lister_tickets(rm, projet, filtre)
    print(f"{version_nom} : {len(selection)} tickets dans la sélection")

    recuperes = inchanges = pj_telechargees = 0
    echecs = []
    for resume in selection:
        numero = resume["id"]
        dossier = dossier_version / str(numero)
        fichier_json, fichier_md = dossier / "ticket.json", dossier / "ticket.md"

        if not args.tout and fichier_json.exists() and fichier_md.exists():
            try:
                ancien = json.loads(fichier_json.read_text(encoding="utf-8"))["issue"]
                if ancien.get("updated_on") == resume.get("updated_on"):
                    inchanges += 1
                    continue
            except (OSError, ValueError, KeyError):
                pass

        try:
            donnees = rm.lire_json(f"/issues/{numero}.json", {"include": "journals,relations,children,attachments"})
            ticket = donnees["issue"]
            dossier.mkdir(exist_ok=True)
            pieces_jointes, nombre = telecharger_pieces_jointes(rm, ticket, dossier, taille_max)
            pj_telechargees += nombre
            memoriser_libelles(ticket, ref)
            # Le .md est écrit avant le .json : un ticket n'est considéré à jour que si les deux le sont.
            fichier_md.write_text(ticket_markdown(ticket, ref, rm.url, pieces_jointes), encoding="utf-8")
            fichier_json.write_text(json.dumps(donnees, ensure_ascii=False, indent=2), encoding="utf-8")
            recuperes += 1
            print(f"  #{numero} récupéré")
        except urllib.error.HTTPError as erreur:
            echecs.append(f"#{numero} : erreur HTTP {erreur.code}")
        except (urllib.error.URLError, OSError, ValueError, KeyError) as erreur:
            echecs.append(f"#{numero} : {erreur}")

    statut_nom = ref["status_id"].get(statut_id, f"n° {statut_id}")
    description_filtre = f"projet {projet}, statut {statut_nom}, version {version_nom}"
    if exclure:
        nom_exclu = ref["assigned_to_id"].get(exclure)
        description_filtre += f", assigné différent de {nom_exclu}" if nom_exclu else f", assigné différent de l'utilisateur n° {exclure}"
    ecrire_index(dossier_version, version_nom, selection, description_filtre)

    print()
    print(f"Récupérés : {recuperes} | Inchangés : {inchanges} | Pièces jointes téléchargées : {pj_telechargees}")
    print(f"Dossier : {dossier_version}")
    if echecs:
        print(f"Échecs ({len(echecs)}) :")
        for ligne in echecs:
            print(f"  {ligne}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as erreur:
        messages = {
            401: "clé API refusée (401). Vérifier REDMINE_API_KEY dans le .env.",
            403: "accès refusé (403). Le compte n'a pas les droits nécessaires ou l'API REST est désactivée.",
            404: "ressource introuvable (404). Vérifier REDMINE_URL, REDMINE_PROJET et REDMINE_VERSION_ID.",
        }
        sys.exit(f"Erreur : {messages.get(erreur.code, f'erreur HTTP {erreur.code}')}")
    except urllib.error.URLError as erreur:
        if isinstance(erreur.reason, ssl.SSLCertVerificationError):
            sys.exit("Erreur : certificat du serveur non reconnu. Renseigner REDMINE_CA_FILE dans le .env.")
        sys.exit(f"Erreur : serveur injoignable ({erreur.reason}). Vérifier REDMINE_URL et la connexion au réseau interne.")
    except KeyboardInterrupt:
        sys.exit("Interrompu.")
        