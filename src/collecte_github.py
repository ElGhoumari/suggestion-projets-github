import json
import ssl
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import certifi


def recuperer_repositories(recherche):
    parametres = {
        "q": f"{recherche} fork:false archived:false",
        "per_page": 20,
    }

    url = (
        "https://api.github.com/search/repositories?"
        + urlencode(parametres)
    )

    requete = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "suggestion-projets-github",
        },
    )

    contexte_ssl = ssl.create_default_context(cafile=certifi.where())

    with urlopen(requete, timeout=30, context=contexte_ssl) as reponse:
        return json.load(reponse)


def enregistrer_donnees(donnees):
    racine = Path(__file__).resolve().parent.parent
    fichier = racine / "data" / "brut" / "repositories.json"
    fichier.parent.mkdir(parents=True, exist_ok=True)

    with fichier.open("w", encoding="utf-8") as sortie:
        json.dump(donnees, sortie, ensure_ascii=False, indent=2)

    return fichier


def main():
    recherches = [
        "machine learning",
        "algorithmic trading",
        "speech recognition",
        "computer vision",
        "web framework",
    ]

    projets_par_id = {}
    bilan_recherches = []

    for position, recherche in enumerate(recherches):
        print(f"Collecte : {recherche}")

        try:
            donnees = recuperer_repositories(recherche)
        except HTTPError as erreur:
            print(f"Erreur GitHub : HTTP {erreur.code}.")
            print("Collecte interrompue. Le fichier précédent est conservé.")
            return
        except (URLError, TimeoutError) as erreur:
            print(f"Impossible de contacter GitHub : {erreur}")
            print("Le fichier précédent est conservé.")
            return

        repositories = donnees["items"]

        for repository in repositories:
            projets_par_id[repository["id"]] = repository

        bilan_recherches.append({
            "recherche": recherche,
            "total_count": donnees["total_count"],
            "incomplete_results": donnees["incomplete_results"],
            "nombre_recupere": len(repositories),
        })

        print(f"  {len(repositories)} résultats reçus.")

        if position < len(recherches) - 1:
            time.sleep(7)

    resultat = {
        "nombre_repositories": len(projets_par_id),
        "recherches": bilan_recherches,
        "items": list(projets_par_id.values()),
    }

    fichier = enregistrer_donnees(resultat)

    print(f"\n{len(projets_par_id)} repositories uniques enregistrés.")
    print(f"Fichier : {fichier}")


if __name__ == "__main__":
    main()