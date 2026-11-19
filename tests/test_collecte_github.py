import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from email.message import Message

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import collecte_github as collecte


class TestCollecte(unittest.TestCase):
    def test_fusion_reprise_et_objectif_deja_atteint(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / 'repositories.json'
            fichier.write_text(json.dumps({'items': [{'id': 1, 'full_name': 'ancien/projet'}], 'recherches': []}))
            appels = []

            def reponse(recherche, page):
                appels.append((recherche, page))
                if len(appels) == 2:
                    raise TimeoutError('interruption simulée')
                return {'items': [{'id': 1}, {'id': 2}], 'total_count': 1000, 'incomplete_results': False}

            with patch.object(collecte, 'recuperer_repositories', side_effect=reponse), patch.object(collecte.time, 'sleep'), redirect_stdout(io.StringIO()):
                with self.assertRaises(TimeoutError):
                    collecte.collecter(fichier, 3)
            sauvegarde = json.loads(fichier.read_text())
            self.assertEqual(len(sauvegarde['items']), 2)
            self.assertEqual(sauvegarde['prochaines_pages']['machine learning'], 2)
            self.assertTrue((Path(dossier) / 'pages/0_1.json').exists())

            reponse2 = {'items': [{'id': 3}], 'total_count': 1, 'incomplete_results': False}
            with patch.object(collecte, 'recuperer_repositories', return_value=reponse2) as appel, patch.object(collecte.time, 'sleep'), redirect_stdout(io.StringIO()):
                collecte.collecter(fichier, 3)
                self.assertEqual(appel.call_args.args, ('machine learning', 2))
                appel.reset_mock()
                collecte.collecter(fichier, 3)
                appel.assert_not_called()
            self.assertEqual({p['id'] for p in json.loads(fichier.read_text())['items']}, {1, 2, 3})

    def test_recherche_epuisee(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / 'repositories.json'
            with patch.object(collecte, 'recuperer_repositories', return_value={'items': [], 'total_count': 0}) as appel, patch.object(collecte.time, 'sleep'), redirect_stdout(io.StringIO()):
                collecte.collecter(fichier, 1000)
                self.assertEqual(appel.call_count, 5)
                appel.reset_mock()
                collecte.collecter(fichier, 1000)
                appel.assert_not_called()

    def test_quota_et_reponse_incomplete(self):
        h = Message(); h['X-RateLimit-Remaining'] = '0'
        erreur = HTTPError('https://api.github.com', 403, 'quota', h, None)
        reponse = io.BytesIO(json.dumps({'items': [], 'total_count': 0, 'incomplete_results': False}).encode())
        reponse.headers = Message()
        with patch.object(collecte, 'urlopen', side_effect=[erreur, reponse]) as appel, patch.object(collecte, 'attendre_quota', return_value=True) as attente, redirect_stdout(io.StringIO()):
            collecte.recuperer_repositories('test', 1)
            self.assertEqual(appel.call_count, 2)
            attente.assert_called_once()
        reponse = io.BytesIO(b'{"items": [], "incomplete_results": true}')
        reponse.headers = Message()
        with patch.object(collecte, 'urlopen', return_value=reponse), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'incomplète'):
                collecte.recuperer_repositories('test', 1)


if __name__ == '__main__':
    unittest.main()
