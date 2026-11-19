# Comparaison TF-IDF avec et sans README

## Configuration

Nous comparons les deux versions sur les mêmes 1037 projets. Chaque texte contient la description, les topics et le langage. La version enrichie ajoute au maximum les 12 000 premiers caractères du README nettoyé disponible. Les README absents ou vides n’ajoutent aucun texte. TF-IDF et cosinus utilisent les mêmes réglages.

Cette limite de longueur est provisoire. Les premiers caractères peuvent contenir de la navigation ou des annonces. Les données brutes et les références initiales restent conservées. Les scores sont des similarités, pas des probabilités. Les empreintes des corpus et les scores complets figurent dans comparaison_tfidf_readme.json.

## Résultats de développement

### stefan-jansen/machine-learning-for-trading

#### sans readme

| Rang | Suggestion | Similarité |
|---|---|---|
| 1 | edtechre/pybroker | 0.582 |
| 2 | PyPatel/Machine-Learning-and-AI-in-Trading | 0.459 |
| 3 | SoftAlgoTrade/TradingStrategies | 0.414 |
| 4 | coding-kitties/investing-algorithm-framework | 0.406 |
| 5 | firmai/financial-machine-learning | 0.397 |

#### avec readme

| Rang | Suggestion | Similarité |
|---|---|---|
| 1 | PacktPublishing/Machine-Learning-for-Algorithmic-Trading-Second-Edition_Original | 0.535 |
| 2 | PacktPublishing/Hands-On-Machine-Learning-for-Algorithmic-Trading-sample | 0.379 |
| 3 | PacktPublishing/Hands-On-Machine-Learning-for-Algorithmic-Trading | 0.374 |
| 4 | PacktPublishing/Python-for-Algorithmic-Trading-Cookbook-Second-Edition | 0.368 |
| 5 | coding-kitties/investing-algorithm-framework | 0.361 |

### openai/whisper

#### sans readme

| Rang | Suggestion | Similarité |
|---|---|---|
| 1 | SpeechColab/Leaderboard | 0.277 |
| 2 | julius-speech/julius | 0.242 |
| 3 | SpeechColab/GigaSpeech | 0.232 |
| 4 | espressif/esp-sr | 0.231 |
| 5 | amaas/rnn-speech-denoising | 0.200 |

#### avec readme

| Rang | Suggestion | Similarité |
|---|---|---|
| 1 | linto-ai/whisper-timestamped | 0.465 |
| 2 | huggingface/distil-whisper | 0.433 |
| 3 | savbell/whisper-writer | 0.405 |
| 4 | douglas125/SpeechCmdRecognition | 0.396 |
| 5 | m-bain/whisperX | 0.393 |

## Observations

Pour Whisper, les README font apparaître des projets explicitement liés à Whisper. Pour le projet de trading, plusieurs suggestions sont des éditions ou des exemples de livres proches. Cette proximité peut être utile, mais elle peut aussi rendre la liste répétitive. Nous ne désignons pas de meilleure méthode avant les jugements humains.

## Limites de cette comparaison

Le corpus est plus grand que celui des premiers essais à 98 projets : les différences avec ce premier essai ne peuvent pas être attribuées aux seuls README. La comparaison actuelle avec et sans README utilise bien les mêmes candidats. Les six projets d’évaluation sont des exemples de développement ; ils ne constituent pas un test indépendant.
