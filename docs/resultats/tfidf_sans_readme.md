# Premiers résultats de recommandation sans README

## Configuration

Nous avons collecté 100 repositories à partir de cinq recherches :
machine learning, trading algorithmique, reconnaissance vocale,
vision par ordinateur et frameworks web.

Nous avons conservé 98 projets après avoir exclu deux repositories
sans description ni topics.

La recommandation utilise TF-IDF et la similarité cosinus sur
la description, les topics et le langage de chaque projet.

## Projet de départ stefan-jansen/machine-learning-for-trading

| Rang | Suggestion | Similarité |
|---|---|---|
| 1 | edtechre/pybroker | 0.611 |
| 2 | joelowj/awesome-algorithmic-trading | 0.441 |
| 3 | StockSharp/StockSharp | 0.378 |
| 4 | Superalgos/Superalgos | 0.344 |
| 5 | lazyprogrammer/machine_learning_examples | 0.318 |

## Projet de départ openai/whisper

| Rang | Suggestion | Similarité |
|---|---|---|
| 1 | espressif/esp-sr | 0.300 |
| 2 | julius-speech/julius | 0.279 |
| 3 | TalAter/annyang | 0.218 |
| 4 | nl8590687/ASRT_SpeechRecognition | 0.206 |
| 5 | m-bain/whisperX | 0.193 |

## Nos observations

Les suggestions distinguent les deux domaines testés :
le trading et la reconnaissance vocale.

Cependant, les descriptions courtes apportent peu de contexte.
Un projet peut être bien classé parce qu’il partage quelques mots,
sans être nécessairement le plus pertinent.

Ces essais vérifient le fonctionnement du système.
Ils ne constituent pas encore une évaluation formelle.
Les scores de similarité ne sont pas des probabilités de pertinence.

## Prochaine comparaison

Nous comparerons ces résultats avec ceux obtenus après l’ajout
des README, en gardant les mêmes projets de départ et les mêmes
candidats pour isoler l’effet de cet enrichissement.