import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from preparer_donnees import preparer_repositories


class TestPreparationReadme(unittest.TestCase):
    def test_memes_candidats_manquants_vides_et_troncature(self):
        def projet(i, description):
            return dict(id=i, full_name=f'a/p{i}', html_url=f'https://github.com/a/p{i}',
                        description=description, topics=[], language='Python', stargazers_count=1)
        projets = [projet(1, 'audio'), projet(2, 'vision'), projet(3, 'web'), projet(4, None)]
        projets.append(projets[0])
        with tempfile.TemporaryDirectory() as dossier:
            root = Path(dossier)
            for nom, texte in [('p1', 'reconnaissance vocale'), ('p2', '   '), ('p4', 'description readme seule')]:
                fichier = root / 'a' / nom / 'README.txt'
                fichier.parent.mkdir(parents=True)
                fichier.write_text(texte)
            sans = preparer_repositories(projets)
            avec = preparer_repositories(projets, root, 10)
        self.assertEqual([p['id'] for p in sans], [1, 2, 3])
        self.assertEqual([p['id'] for p in sans], [p['id'] for p in avec])
        self.assertTrue(avec[0]['readme_tronque'])
        self.assertEqual(avec[0]['readme_caracteres_utilises'], 10)
        for i in [1, 2]:
            self.assertFalse(avec[i]['readme_utilise'])
            self.assertEqual(sans[i]['texte'], avec[i]['texte'])
        self.assertTrue(all(not p['readme_utilise'] for p in sans))


if __name__ == '__main__':
    unittest.main()
