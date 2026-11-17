import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import ssl
import certifi


def recuperer_repositories():
    parametres = {
        "q": "machine learning fork:false archived:false",
        "per_page": 10,
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
    try:
        donnees = recuperer_repositories()
    except HTTPError as erreur:
        print(f"Erreur GitHub : HTTP {erreur.code}.")
        if erreur.code in (403, 429):
            print("L’accès peut être limité par le quota de requêtes.")
        return
    except (URLError, TimeoutError) as erreur:
        print(f"Impossible de contacter GitHub : {erreur}")
        return

    repositories = donnees["items"]

    for repository in repositories:
        print(repository["full_name"])
        print(repository["description"] or "Description absente")
        print()

    fichier = enregistrer_donnees(donnees)

    print(f"{len(repositories)} repositories récupérés.")
    print(f"Données enregistrées dans : {fichier}")


if __name__ == "__main__":
    main()