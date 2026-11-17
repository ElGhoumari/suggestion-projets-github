import re
from pathlib import Path


def nettoyer_readme(texte):
    # Retirer les blocs de code.
    texte = re.sub(r"```.*?```", " ", texte, flags=re.DOTALL)
    texte = re.sub(r"~~~.*?~~~", " ", texte, flags=re.DOTALL)

    # Retirer les images Markdown et garder le texte des liens.
    texte = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", texte)
    texte = re.sub(
        r"\[((?:\[[^\]]*\]|[^\[\]])*)\]\([^)]*\)",
        lambda lien: lien.group(1).replace("[", "").replace("]", ""),
        texte,
    )

    # Retirer les balises HTML et les URL restantes.
    texte = re.sub(r"<[^>]+>", " ", texte)
    texte = re.sub(r"https?://\S+", " ", texte)

    # Retirer quelques marqueurs Markdown.
    texte = re.sub(r"[#*`]+", " ", texte)

    return " ".join(texte.split())


def main():
    racine = Path(__file__).resolve().parent.parent
    source = racine / "data" / "readme"
    destination = racine / "data" / "readme_nettoye"

    fichiers = sorted(source.glob("*/*/README.md"))

    if not fichiers:
        print("Aucun README à nettoyer.")
        return

    for fichier in fichiers:
        texte = fichier.read_text(encoding="utf-8")
        texte_nettoye = nettoyer_readme(texte)

        chemin_relatif = fichier.relative_to(source)
        sortie = (destination / chemin_relatif).with_suffix(".txt")
        sortie.parent.mkdir(parents=True, exist_ok=True)
        sortie.write_text(texte_nettoye, encoding="utf-8")

        print(f"\nProjet : {chemin_relatif.parent}")
        print(f"Avant : {len(texte)} caractères")
        print(f"Après : {len(texte_nettoye)} caractères")
        print(f"Aperçu : {texte_nettoye[:500]}")


if __name__ == "__main__":
    main()
