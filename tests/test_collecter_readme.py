import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import collecter_readme as collecte


class TestSourceReadme(unittest.TestCase):
    def test_formats_brut_et_reference(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / 'source.json'
            fichier.write_text(json.dumps({'items': [{'full_name': 'a/b'}]}))
            self.assertEqual(collecte.charger_projets(fichier), ['a/b'])
            fichier.write_text(json.dumps([{'nom': 'c/d'}]))
            self.assertEqual(collecte.charger_projets(fichier), ['c/d'])

    def test_bilan_puis_telechargement_des_manquants(self):
        with tempfile.TemporaryDirectory() as dossier:
            racine = Path(dossier)
            source = racine / 'data/brut/repositories.json'
            source.parent.mkdir(parents=True)
            source.write_text(json.dumps({'items': [{'full_name': 'a/b'}, {'full_name': 'c/d'}]}))
            present = racine / 'data/readme/a/b/README.md'
            present.parent.mkdir(parents=True)
            present.write_text('README existant')
            with patch.object(collecte, '__file__', str(racine / 'src/collecter_readme.py')), patch.object(collecte, 'recuperer_readme', return_value=('Nouveau README', {})) as appel, patch.object(collecte.time, 'sleep'), redirect_stdout(io.StringIO()):
                with patch('sys.argv', ['collecter_readme.py', '--bilan']):
                    collecte.main()
                appel.assert_not_called()
                with patch('sys.argv', ['collecter_readme.py']):
                    collecte.main()
                appel.assert_called_once_with('c/d')
            self.assertEqual(present.read_text(), 'README existant')
            self.assertEqual((racine / 'data/readme/c/d/README.md').read_text(), 'Nouveau README')


if __name__ == '__main__':
    unittest.main()
