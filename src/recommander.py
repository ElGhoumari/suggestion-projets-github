import json
import argparse
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def charger_projets():
    racine = Path(__file__).resolve().parent.parent
    fichier = racine / "data" / "prepare" / "repositories.json"

    with fichier.open(encoding="utf-8") as entree:
        return json.load(entree)


def recommander(projets, nom_projet, nombre=5):
    noms = [projet["nom"] for projet in projets]

    if nom_projet not in noms:
        raise ValueError(f"Projet absent des données : {nom_projet}")

    textes = [projet["texte"] for projet in projets]

    vectoriseur = TfidfVectorizer()
    matrice = vectoriseur.fit_transform(textes)

    indice_source = noms.index(nom_projet)
    scores = cosine_similarity(
        matrice[indice_source], matrice
    ).ravel()

    indices = sorted(
        range(len(projets)),
        key=lambda indice: (-scores[indice], noms[indice]),
    )

    resultats = []

    for indice in indices:
        if indice == indice_source or scores[indice] <= 0:
            continue

        resultats.append({
            "nom": projets[indice]["nom"],
            "url": projets[indice]["url"],
            "score": float(scores[indice]),
        })

        if len(resultats) == nombre:
            break

    return resultats


def main():
    analyseur = argparse.ArgumentParser(
        description="Recommander des repositories GitHub similaires."
    )
    analyseur.add_argument(
        "repository",
        help="Nom du repository, par exemple organisation/projet",
    )
    arguments = analyseur.parse_args()

    projets = charger_projets()
    nom_projet = arguments.repository

    resultats = recommander(projets, nom_projet)

    print(f"Projets proches de : {nom_projet}\n")

    for position, resultat in enumerate(resultats, start=1):
        print(f"{position}. {resultat['nom']}")
        print(f"   Similarité : {resultat['score']:.3f}")
        print(f"   {resultat['url']}\n")


if __name__ == "__main__":
    main()
