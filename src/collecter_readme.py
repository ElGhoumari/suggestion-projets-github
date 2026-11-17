import ssl
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import json
import time

import certifi


def recuperer_readme(nom_projet):
    url = f"https://api.github.com/repos/{nom_projet}/readme"

    requete = Request(
        url,
        headers={
            "Accept": "application/vnd.github.raw+json",
            "User-Agent": "suggestion-projets-github",
        },
    )

    contexte_ssl = ssl.create_default_context(cafile=certifi.where())

    with urlopen(requete, timeout=30, context=contexte_ssl) as reponse:
        return reponse.read().decode("utf-8")


def main():
    racine = Path(__file__).resolve().parent.parent
    fichier_projets = (
        racine / "data" / "reference_sans_readme"
        / "repositories_prepares.json"
    )

    with fichier_projets.open(encoding="utf-8") as entree:
        donnees = json.load(entree)

    projets = [projet["nom"] for projet in donnees[:30]]
    dossier = racine / "data" / "readme"

    for nom_projet in projets:
        fichier = dossier / nom_projet / "README.md"

        if fichier.exists():
            print(f"Déjà enregistré : {nom_projet}")
            continue

        print(f"Téléchargement : {nom_projet}")

        try:
            texte = recuperer_readme(nom_projet)
        except HTTPError as erreur:
            if erreur.code == 404:
                print("  README introuvable ou repository inaccessible.")
                continue

            print(f"  Erreur GitHub : HTTP {erreur.code}.")
            print("Collecte arrêtée. Les fichiers déjà enregistrés restent disponibles.")
            return
        except (URLError, TimeoutError, UnicodeDecodeError) as erreur:
            print(f"  Impossible de récupérer le README : {erreur}")
            return

        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_text(texte, encoding="utf-8")

        print(f"  {len(texte)} caractères enregistrés.")
        print(f"  Fichier : {fichier}")
        time.sleep(2)


if __name__ == "__main__":
    main()