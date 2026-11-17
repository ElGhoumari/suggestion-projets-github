import json
from pathlib import Path


def preparer_repositories(repositories):
    projets = []
    identifiants = set()

    for repository in repositories:
        identifiant = repository["id"]

        if identifiant in identifiants:
            continue

        identifiants.add(identifiant)

        description = " ".join(
            (repository.get("description") or "").split()
        )
        topics = repository.get("topics") or []
        langage = repository.get("language") or ""

        texte = " ".join(
            " ".join([description, " ".join(topics), langage]).split()
        )

        projets.append({
            "id": identifiant,
            "nom": repository["full_name"],
            "url": repository["html_url"],
            "description": description,
            "topics": topics,
            "langage": langage,
            "etoiles": repository["stargazers_count"],
            "texte": texte,
        })

    return projets


def main():
    racine = Path(__file__).resolve().parent.parent
    source = racine / "data" / "brut" / "repositories.json"
    destination = racine / "data" / "prepare" / "repositories.json"

    with source.open("r", encoding="utf-8") as fichier:
        donnees = json.load(fichier)

    projets = preparer_repositories(donnees["items"])

    destination.parent.mkdir(parents=True, exist_ok=True)

    with destination.open("w", encoding="utf-8") as fichier:
        json.dump(projets, fichier, ensure_ascii=False, indent=2)

    print(f"{len(projets)} repositories préparés.")
    print(f"Fichier enregistré : {destination}")


if __name__ == "__main__":
    main()
