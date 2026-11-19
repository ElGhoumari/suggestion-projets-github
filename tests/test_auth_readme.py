import io
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import collecter_readme as collecte


class TestAuthentification(unittest.TestCase):
    def test_token_env_et_absence_token(self):
        for token in ['', 'jeton-fictif-pour-test']:
            reponse = io.BytesIO(b'README')
            reponse.headers = {}
            with patch.dict(os.environ, {'GITHUB_TOKEN': token}), patch.object(collecte, 'urlopen', return_value=reponse) as appel:
                texte, _ = collecte.recuperer_readme('a/b')
                self.assertEqual(texte, 'README')
                requete = appel.call_args.args[0]
                self.assertEqual(requete.get_header('Authorization'), 'Bearer ' + token if token else None)
                self.assertNotIn('jeton-fictif', requete.full_url)


if __name__ == '__main__':
    unittest.main()
