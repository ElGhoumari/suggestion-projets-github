import json
from pathlib import Path


def main():
    racine = Path(__file__).resolve().parent.parent
    fichier = racine / "data" / "brut" / "repositories.json"

    with fichier.open("r", encoding="utf-8") as entree:
        donnees = json.load(entree)

    repositories = donnees["items"]

    print(f"Repositories récupérés : {len(repositories)}")
    for bilan in donnees["recherches"]:
        print(
            f"Recherche : {bilan['recherche']} | "
            f"Résultats reçus : {bilan['nombre_recupere']} | "
            f"Incomplète : {bilan['incomplete_results']}"
        )
    descriptions_absentes = 0
    topics_absents = 0
    identifiants = set()

    for repository in repositories:
        identifiants.add(repository["id"])

        if not (repository.get("description") or "").strip():
            descriptions_absentes += 1

        if not repository.get("topics"):
            topics_absents += 1

        print()
        print(f"Projet : {repository['full_name']}")
        print(f"Description : {repository.get('description')}")
        print(f"Langage : {repository.get('language')}")
        print(f"Topics : {repository.get('topics', [])}")
        print(f"Étoiles : {repository['stargazers_count']}")

    print("\nBilan")
    print(f"Descriptions absentes : {descriptions_absentes}")
    print(f"Repositories sans topics : {topics_absents}")
    print(f"Identifiants en double : {len(repositories) - len(identifiants)}")


if __name__ == "__main__":
    main()