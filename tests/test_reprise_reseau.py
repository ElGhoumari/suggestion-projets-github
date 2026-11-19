import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import collecter_readme as collecte


class TestRepriseReseau(unittest.TestCase):
    def test_timeout_puis_succes(self):
        reponse = io.BytesIO(b'README')
        reponse.headers = {}
        with patch.object(collecte, 'urlopen', side_effect=[URLError(TimeoutError()), reponse]) as appel, patch.object(collecte.time, 'sleep') as attente, redirect_stdout(io.StringIO()):
            self.assertEqual(collecte.recuperer_readme('a/b')[0], 'README')
            self.assertEqual(appel.call_count, 2)
            attente.assert_called_once_with(5)

    def test_quatre_essais_maximum(self):
        with patch.object(collecte, 'urlopen', side_effect=TimeoutError()) as appel, patch.object(collecte.time, 'sleep') as attente, redirect_stdout(io.StringIO()):
            with self.assertRaises(TimeoutError):
                collecte.recuperer_readme('a/b')
            self.assertEqual(appel.call_count, 4)
            self.assertEqual([a.args[0] for a in attente.call_args_list], [5, 10, 20])

    def test_projet_en_echec_ne_bloque_pas_le_suivant(self):
        with tempfile.TemporaryDirectory() as dossier:
            racine = Path(dossier)
            source = racine / 'data/brut/repositories.json'
            source.parent.mkdir(parents=True)
            source.write_text(json.dumps({'items': [{'full_name': 'a/echec'}, {'full_name': 'b/succes'}]}))
            sortie = io.StringIO()
            with patch.object(collecte, '__file__', str(racine / 'src/collecter_readme.py')), patch('sys.argv', ['collecter_readme.py']), patch.object(collecte, 'recuperer_readme', side_effect=[TimeoutError(), ('README', {})]), patch.object(collecte.time, 'sleep'), redirect_stdout(sortie):
                collecte.main()
            self.assertTrue((racine / 'data/readme/b/succes/README.md').is_file())
            self.assertFalse((racine / 'data/readme/a/echec/README.md').exists())
            self.assertIn('échecs : 1', sortie.getvalue())
            self.assertIn('a/echec', sortie.getvalue())


if __name__ == '__main__':
    unittest.main()
