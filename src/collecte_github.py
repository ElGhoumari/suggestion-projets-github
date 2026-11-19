import argparse
import json
import os
import ssl
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import certifi

from collecter_readme import afficher_quota, attendre_quota


RECHERCHES = [
    "machine learning",
    "algorithmic trading",
    "speech recognition",
    "computer vision",
    "web framework",
]
TAILLE_PAGE = 100


def recuperer_repositories(recherche, page):
    parametres = {
        "q": f"{recherche} fork:false archived:false",
        "per_page": TAILLE_PAGE,
        "page": page,
    }
    url = "https://api.github.com/search/repositories?" + urlencode(parametres)
    entetes = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "suggestion-projets-github",
    }
    # Le token est optionnel et n'est jamais enregistré dans les données.
    if os.environ.get("GITHUB_TOKEN"):
        entetes["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]

    requete = Request(url, headers=entetes)
    contexte = ssl.create_default_context(cafile=certifi.where())

    for tentative in range(4):
        try:
            with urlopen(requete, timeout=30, context=contexte) as reponse:
                donnees = json.load(reponse)
                afficher_quota(reponse.headers)
                if donnees.get("incomplete_results"):
                    raise ValueError("Recherche incomplète : page non validée, à reprendre plus tard.")
                if not isinstance(donnees.get("items"), list):
                    raise ValueError("Réponse GitHub inattendue : liste items absente.")
                return donnees
        except HTTPError as erreur:
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
            print(f"Reprise : {recherche}, page {page}", flush=True)


def enregistrer_donnees(donnees, fichier):
    fichier.parent.mkdir(parents=True, exist_ok=True)
    temporaire = fichier.with_suffix(".tmp")
    with temporaire.open("w", encoding="utf-8") as sortie:
        json.dump(donnees, sortie, ensure_ascii=False, indent=2)
    temporaire.replace(fichier)


def collecter(fichier, objectif):
    if fichier.exists():
        donnees = json.loads(fichier.read_text(encoding="utf-8"))
    else:
        donnees = {"items": [], "recherches": []}

    projets = {p["id"]: p for p in donnees["items"]}
    configuration = {"recherches": RECHERCHES, "taille_page": TAILLE_PAGE}
    if donnees.get("configuration_collecte", configuration) != configuration:
        raise ValueError("Configuration de pagination différente : vérifier l'avancement avant de poursuivre.")

    pages = donnees.get("prochaines_pages", {r: 1 for r in RECHERCHES})
    bilans = {b["recherche"]: b for b in donnees.get("recherches", [])}
    print(f"Départ : {len(projets)} repositories uniques. Objectif : au moins {objectif}.", flush=True)

    while len(projets) < objectif:
        progression = False
        # Une page par domaine à chaque tour pour diversifier la collecte.
        for recherche in RECHERCHES:
            if len(projets) >= objectif:
                break
            page = pages[recherche]
            if page is None:
                continue
            progression = True
            print(f"Collecte : {recherche}, page {page}", flush=True)
            reponse = recuperer_repositories(recherche, page)
            maintenant = datetime.now(timezone.utc).isoformat()

            # Conserver aussi chaque réponse brute et sa date.
            archive = fichier.parent / "pages" / f"{RECHERCHES.index(recherche)}_{page}.json"
            enregistrer_donnees({"collecte_le": maintenant, "recherche": recherche,
                                  "page": page, "reponse": reponse}, archive)
            avant = len(projets)
            for projet in reponse["items"]:
                projets[projet["id"]] = projet

            # GitHub ne rend accessibles que les 1 000 premiers résultats d'une recherche.
            fin = (not reponse["items"] or page * TAILLE_PAGE >= min(reponse["total_count"], 1000))
            pages[recherche] = None if fin else page + 1
            bilan = bilans.get(recherche, {})
            bilans[recherche] = {
                "recherche": recherche,
                "total_count": reponse["total_count"],
                "incomplete_results": False,
                "nombre_recupere": (bilan.get("nombre_recupere", 0) if page > 1 else 0) + len(reponse["items"]),
                "derniere_page": page,
                "collecte_le": maintenant,
            }
            donnees.update({
                "nombre_repositories": len(projets),
                "items": list(projets.values()),
                "recherches": list(bilans.values()),
                "configuration_collecte": configuration,
                "prochaines_pages": pages,
                "derniere_collecte": maintenant,
            })
            # Données et curseurs sont sauvegardés ensemble après chaque page.
            enregistrer_donnees(donnees, fichier)
            print(f"  {len(projets) - avant} nouveaux ; {len(projets)} uniques sauvegardés.", flush=True)
            if len(projets) < objectif:
                time.sleep(7)

        if not progression:
            print("Recherches épuisées. Il faudra élargir les requêtes pour augmenter le corpus.")
            break

    print(f"Fin : {len(projets)} repositories uniques. Fichier : {fichier}")
    print("Les recherches évoluent sur GitHub : ce corpus n'est pas un échantillon représentatif.")


def main():
    analyseur = argparse.ArgumentParser(description="Collecte paginée et reprenable des repositories GitHub.")
    analyseur.add_argument("--objectif", type=int, default=1000,
                          help="Nombre total de repositories uniques visé (défaut : 1000).")
    arguments = analyseur.parse_args()
    if arguments.objectif < 1:
        analyseur.error("--objectif doit être positif.")

    racine = Path(__file__).resolve().parent.parent
    fichier = racine / "data" / "brut" / "repositories.json"
    try:
        collecter(fichier, arguments.objectif)
    except KeyboardInterrupt:
        print("\nInterruption : les pages déjà sauvegardées seront conservées pour la reprise.")
    except (HTTPError, URLError, TimeoutError, ValueError, OSError) as erreur:
        print(f"Collecte arrêtée : {erreur}")
        print("Relancer la même commande pour reprendre après la dernière page sauvegardée.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
