import argparse
import json
from pathlib import Path


def preparer_repositories(repositories, dossier_readme=None, limite_readme=12000):
    projets = []
    identifiants = set()

    for repository in repositories:
        identifiant = repository["id"]
        if identifiant in identifiants:
            continue
        identifiants.add(identifiant)

        description = " ".join((repository.get("description") or "").split())
        topics = repository.get("topics") or []
        langage = repository.get("language") or ""

        # Même sélection dans les deux versions pour comparer les mêmes candidats.
        if not description and not topics:
            continue

        readme = ""
        if dossier_readme is not None:
            fichier = dossier_readme / repository["full_name"] / "README.txt"
            if fichier.is_file():
                readme = " ".join(fichier.read_text(encoding="utf-8").split())

        extrait = readme[:limite_readme]
        texte = " ".join(
            " ".join([description, " ".join(topics), langage, extrait]).split()
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
            "readme_utilise": bool(extrait),
            "readme_caracteres_total": len(readme),
            "readme_caracteres_utilises": len(extrait),
            "readme_tronque": len(readme) > limite_readme,
        })

    return projets


def enregistrer(projets, fichier):
    fichier.parent.mkdir(parents=True, exist_ok=True)
    temporaire = fichier.with_suffix(".tmp")
    temporaire.write_text(
        json.dumps(projets, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    temporaire.replace(fichier)


def main():
    analyseur = argparse.ArgumentParser(description="Préparer deux corpus comparables avec et sans README.")
    analyseur.add_argument("--limite-readme", type=int, default=12000,
                          help="Nombre maximal de caractères ajoutés par README (défaut : 12000).")
    arguments = analyseur.parse_args()
    if arguments.limite_readme < 1:
        analyseur.error("--limite-readme doit être positif.")

    racine = Path(__file__).resolve().parent.parent
    source = racine / "data/brut/repositories.json"
    with source.open(encoding="utf-8") as fichier:
        donnees = json.load(fichier)

    sans_readme = preparer_repositories(donnees["items"])
    avec_readme = preparer_repositories(
        donnees["items"], racine / "data/readme_nettoye", arguments.limite_readme
    )
    for nom, projets in [("sans", sans_readme), ("avec", avec_readme)]:
        destination = racine / "data/prepare" / f"repositories_{nom}_readme.json"
        enregistrer(projets, destination)
        print(f"{len(projets)} projets préparés {nom} README : {destination}")

    print(f"README non vides utilisés : {sum(p['readme_utilise'] for p in avec_readme)}")
    print(f"README tronqués à {arguments.limite_readme} caractères : {sum(p['readme_tronque'] for p in avec_readme)}")
    print("Les fichiers de référence et l'ancien repositories.json ne sont pas modifiés.")


if __name__ == "__main__":
    main()
