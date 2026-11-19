import argparse
import os
from http.client import IncompleteRead, RemoteDisconnected
from datetime import datetime
from zoneinfo import ZoneInfo
import ssl
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
import time

import certifi


def afficher_quota(entetes):
    restant = entetes.get("X-RateLimit-Remaining")
    limite = entetes.get("X-RateLimit-Limit")
    renouvellement = entetes.get("X-RateLimit-Reset")

    if restant is not None:
        print(f"  Requêtes restantes : {restant} / {limite or '?'}")

    if renouvellement:
        try:
            date = datetime.fromtimestamp(
                int(renouvellement), tz=ZoneInfo("Europe/Paris")
            )
            print(f"  Renouvellement : {date:%d/%m/%Y à %H:%M:%S %Z}")
        except (ValueError, OverflowError, OSError):
            print("  Heure de renouvellement indisponible.")

    return restant == "0"


def attendre_quota(entetes, tentative=0):
    delais = []

    if entetes.get("X-RateLimit-Remaining") == "0":
        try:
            delais.append(max(1, int(entetes["X-RateLimit-Reset"]) - time.time() + 2))
        except (KeyError, ValueError):
            return False

    if entetes.get("Retry-After"):
        try:
            delais.append(max(1, int(entetes["Retry-After"]) + 1))
        except ValueError:
            pass

    if not delais:
        delais.append(60 * (2 ** tentative))

    delai = max(delais)
    reprise = datetime.fromtimestamp(
        time.time() + delai, tz=ZoneInfo("Europe/Paris")
    )
    print(f"  Pause automatique de {int(delai) + 1} secondes.")
    print(f"  Reprise prévue : {reprise:%d/%m/%Y à %H:%M:%S %Z}")
    print("  Laisser le programme ouvert ; Ctrl+C permet de l’arrêter.")
    time.sleep(delai)
    return True


def recuperer_readme(nom_projet):
    url = f"https://api.github.com/repos/{nom_projet}/readme"

    entetes = {
        "Accept": "application/vnd.github.raw+json",
        "User-Agent": "suggestion-projets-github",
    }
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        entetes["Authorization"] = "Bearer " + token

    requete = Request(url, headers=entetes)

    contexte_ssl = ssl.create_default_context(cafile=certifi.where())

    # Trois nouvelles tentatives au maximum pour éviter une boucle sans fin.
    for tentative in range(4):
        try:
            with urlopen(requete, timeout=30, context=contexte_ssl) as reponse:
                return reponse.read().decode("utf-8"), reponse.headers
        except HTTPError as erreur:
            if erreur.code in (408, 500, 502, 503, 504) and tentative < 3:
                delai = 5 * (2 ** tentative)
                print(f"  Erreur temporaire HTTP {erreur.code}. Nouvel essai dans {delai} secondes.", flush=True)
                time.sleep(delai)
                continue

            limitation = (
                erreur.headers.get("X-RateLimit-Remaining") == "0"
                or erreur.headers.get("Retry-After") is not None
                or erreur.code == 429
            )
            if erreur.code not in (403, 429) or not limitation or tentative == 3:
                raise

            afficher_quota(erreur.headers)
            if not attendre_quota(erreur.headers, tentative):
                raise
            print(f"  Reprise du téléchargement : {nom_projet}")
        except (URLError, TimeoutError, IncompleteRead, RemoteDisconnected, ConnectionError):
            if tentative == 3:
                raise
            delai = 5 * (2 ** tentative)
            print(
                f"  Connexion interrompue ou délai dépassé. "
                f"Nouvel essai {tentative + 2}/4 dans {delai} secondes.",
                flush=True,
            )
            time.sleep(delai)


def charger_projets(fichier):
    with fichier.open(encoding="utf-8") as entree:
        donnees = json.load(entree)

    if isinstance(donnees, dict):
        return [projet["full_name"] for projet in donnees["items"]]
    return [projet["nom"] for projet in donnees]


def main():
    analyseur = argparse.ArgumentParser(
        description="Collecter les README des repositories."
    )
    analyseur.add_argument(
        "--limite",
        type=int,
        default=None,
        help="Nombre de projets à examiner. Par défaut : tout le corpus.",
    )
    analyseur.add_argument(
        "--reference",
        action="store_true",
        help="Utiliser les 98 projets de référence au lieu du corpus élargi.",
    )
    analyseur.add_argument(
        "--bilan",
        action="store_true",
        help="Afficher les fichiers disponibles sans contacter GitHub.",
    )
    arguments = analyseur.parse_args()

    if arguments.limite is not None and arguments.limite < 1:
        analyseur.error("--limite doit être un entier positif.")

    racine = Path(__file__).resolve().parent.parent
    if arguments.reference:
        fichier_projets = (
            racine / "data" / "reference_sans_readme"
            / "repositories_prepares.json"
        )
    else:
        fichier_projets = racine / "data" / "brut" / "repositories.json"

    projets = charger_projets(fichier_projets)[:arguments.limite]
    dossier = racine / "data" / "readme"
    disponibles = sum(
        (dossier / nom / "README.md").is_file()
        and (dossier / nom / "README.md").stat().st_size > 0
        for nom in projets
    )
    print(f"Source : {fichier_projets}")
    print(f"{len(projets)} projets à examiner.")
    print(f"README déjà disponibles : {disponibles}")
    print(f"README à récupérer : {len(projets) - disponibles}")
    if arguments.bilan:
        return

    if os.environ.get("GITHUB_TOKEN", "").strip():
        print("Token détecté : les requêtes seront authentifiées.")
    else:
        print("Mode non authentifié : quota réduit. Définir GITHUB_TOKEN pour accélérer.")

    nouveaux = 0
    absents = 0
    echecs = []

    for nom_projet in projets:
        fichier = dossier / nom_projet / "README.md"

        if fichier.is_file() and fichier.stat().st_size > 0:
            print(f"Déjà enregistré : {nom_projet}")
            continue

        print(f"Téléchargement : {nom_projet}")

        try:
            texte, entetes = recuperer_readme(nom_projet)
        except HTTPError as erreur:
            if erreur.code == 401:
                print("Token refusé : vérifier sa validité ou son expiration.")
                print("Les README enregistrés sont conservés.")
                return

            quota_epuise = afficher_quota(erreur.headers)

            if erreur.code in (403, 429) or quota_epuise:
                print(f"  Erreur GitHub : HTTP {erreur.code}.")
                print("Blocage persistant ou accès refusé : collecte arrêtée.")
                print("Les fichiers téléchargés sont conservés pour la prochaine reprise.")
                return

            if erreur.code == 404:
                print("  README introuvable ou repository inaccessible.")
                absents += 1
                continue

            if erreur.code in (408, 500, 502, 503, 504):
                print(f"  Échec HTTP {erreur.code} après les tentatives. Passage au projet suivant.")
                echecs.append(nom_projet)
                continue

            print(f"  Erreur GitHub : HTTP {erreur.code}.")
            print("Collecte arrêtée. Les fichiers déjà enregistrés restent disponibles.")
            return
        except (URLError, TimeoutError, IncompleteRead, RemoteDisconnected, ConnectionError, UnicodeDecodeError):
            print("  README non récupéré. Passage au projet suivant ; il restera à réessayer.")
            echecs.append(nom_projet)
            continue

        fichier.parent.mkdir(parents=True, exist_ok=True)
        temporaire = fichier.with_suffix(".tmp")
        temporaire.write_text(texte, encoding="utf-8")
        temporaire.replace(fichier)
        nouveaux += 1

        print(f"  {len(texte)} caractères enregistrés.")
        print(f"  Fichier : {fichier}")
        afficher_quota(entetes)

        time.sleep(2)

    print("Collecte terminée : tous les projets sélectionnés ont été examinés.")
    print(f"Déjà présents : {disponibles} ; téléchargés : {nouveaux} ; introuvables : {absents} ; échecs : {len(echecs)}.")
    if echecs:
        print("Projets à réessayer :")
        for nom in echecs:
            print(f"  - {nom}")


if __name__ == "__main__":
    main()