# Évaluation humaine des suggestions

## Objectif

Nous cherchons des projets qui aident le développeur du projet source à découvrir des outils, des alternatives ou des ressources répondant à un besoin proche. Une simple correspondance de mots ne suffit pas. Nous consultons la présentation et, si nécessaire, le README de chaque candidat.

Pour commencer, nous évaluons les candidats de six projets sources. La liste rassemble les cinq premiers résultats de chaque méthode, dédupliqués et mélangés. Les rangs, scores et méthodes ne sont pas affichés. Éviter de consulter le rapport comparatif pendant la notation. Certains résultats ont déjà été vus : cette présentation ne garantit pas une évaluation entièrement aveugle.

## Barème commun

- 0 : non pertinent pour le besoin du projet source.
- 1 : lié au domaine, mais utilité indirecte ou besoin différent.
- 2 : très pertinent, objectif ou usage proche et utilité identifiable.
- ? : impossible à juger avec les informations disponibles. Ne pas transformer ce cas en 0.

Avant de noter chaque section, écrire le besoin du développeur en une phrase pour garder le même critère entre candidats. Chaque membre du binôme remplit sa propre copie, puis nous discutons les désaccords pour produire une note commune. Les notes doivent rester vides avant la lecture des projets.

La colonne « Redondant avec » indique un autre candidat qui apporte presque la même ressource, par exemple une édition ou un extrait du même livre. Ce signal sera étudié séparément de la pertinence. Un contenu ancien n’est pas automatiquement non pertinent ; préciser la raison de la note.

## Exploitation prévue

Après annotation, nous calculerons Precision@5 en considérant la note 2 comme pertinente et NDCG@5 avec les notes graduées. Nous publierons aussi le nombre de requêtes, la couverture des jugements et les cas non jugés. Les requêtes dont un candidat du top 5 reste non jugé ne recevront pas de score définitif.

La comparaison est limitée aux candidats proposés par ces deux méthodes. Elle ne mesure pas le rappel sur tout GitHub. Ces exemples servent au développement ; un jeu de test distinct devra être fixé avant le choix final du modèle. Les Transformers pourront apporter de nouveaux candidats à annoter.

## stefan-jansen/machine-learning-for-trading

Projet source : [ouvrir sur GitHub](https://github.com/stefan-jansen/machine-learning-for-trading)

Besoin du développeur : à compléter avant de noter.

| Candidat | Note 0 1 2 ou ? | Justification | Redondant avec |
|---|---|---|---|
| [PacktPublishing/Hands-On-Machine-Learning-for-Algorithmic-Trading-sample](https://github.com/PacktPublishing/Hands-On-Machine-Learning-for-Algorithmic-Trading-sample) |  |  |  |
| [PacktPublishing/Machine-Learning-for-Algorithmic-Trading-Second-Edition_Original](https://github.com/PacktPublishing/Machine-Learning-for-Algorithmic-Trading-Second-Edition_Original) |  |  |  |
| [edtechre/pybroker](https://github.com/edtechre/pybroker) |  |  |  |
| [PyPatel/Machine-Learning-and-AI-in-Trading](https://github.com/PyPatel/Machine-Learning-and-AI-in-Trading) |  |  |  |
| [firmai/financial-machine-learning](https://github.com/firmai/financial-machine-learning) |  |  |  |
| [PacktPublishing/Hands-On-Machine-Learning-for-Algorithmic-Trading](https://github.com/PacktPublishing/Hands-On-Machine-Learning-for-Algorithmic-Trading) |  |  |  |
| [SoftAlgoTrade/TradingStrategies](https://github.com/SoftAlgoTrade/TradingStrategies) |  |  |  |
| [PacktPublishing/Python-for-Algorithmic-Trading-Cookbook-Second-Edition](https://github.com/PacktPublishing/Python-for-Algorithmic-Trading-Cookbook-Second-Edition) |  |  |  |
| [coding-kitties/investing-algorithm-framework](https://github.com/coding-kitties/investing-algorithm-framework) |  |  |  |

## openai/whisper

Projet source : [ouvrir sur GitHub](https://github.com/openai/whisper)

Besoin du développeur : à compléter avant de noter.

| Candidat | Note 0 1 2 ou ? | Justification | Redondant avec |
|---|---|---|---|
| [huggingface/distil-whisper](https://github.com/huggingface/distil-whisper) |  |  |  |
| [douglas125/SpeechCmdRecognition](https://github.com/douglas125/SpeechCmdRecognition) |  |  |  |
| [julius-speech/julius](https://github.com/julius-speech/julius) |  |  |  |
| [amaas/rnn-speech-denoising](https://github.com/amaas/rnn-speech-denoising) |  |  |  |
| [m-bain/whisperX](https://github.com/m-bain/whisperX) |  |  |  |
| [espressif/esp-sr](https://github.com/espressif/esp-sr) |  |  |  |
| [SpeechColab/Leaderboard](https://github.com/SpeechColab/Leaderboard) |  |  |  |
| [savbell/whisper-writer](https://github.com/savbell/whisper-writer) |  |  |  |
| [linto-ai/whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) |  |  |  |
| [SpeechColab/GigaSpeech](https://github.com/SpeechColab/GigaSpeech) |  |  |  |

## wepe/MachineLearning

Projet source : [ouvrir sur GitHub](https://github.com/wepe/MachineLearning)

Besoin du développeur : à compléter avant de noter.

| Candidat | Note 0 1 2 ou ? | Justification | Redondant avec |
|---|---|---|---|
| [ljpzzz/machinelearning](https://github.com/ljpzzz/machinelearning) |  |  |  |
| [TeFuirnever/Machine-Learning-in-Action](https://github.com/TeFuirnever/Machine-Learning-in-Action) |  |  |  |
| [gyy8426/Computer_Vision_primer](https://github.com/gyy8426/Computer_Vision_primer) |  |  |  |
| [HadXu/machine-learning](https://github.com/HadXu/machine-learning) |  |  |  |
| [ujjwalkarn/Machine-Learning-Tutorials](https://github.com/ujjwalkarn/Machine-Learning-Tutorials) |  |  |  |
| [RedstoneWill/HsuanTienLin_MachineLearning](https://github.com/RedstoneWill/HsuanTienLin_MachineLearning) |  |  |  |
| [susanli2016/Machine-Learning-with-Python](https://github.com/susanli2016/Machine-Learning-with-Python) |  |  |  |
| [mdozmorov/MachineLearning_notes](https://github.com/mdozmorov/MachineLearning_notes) |  |  |  |
| [bfortuner/ml-glossary](https://github.com/bfortuner/ml-glossary) |  |  |  |
| [vivienzou1/DL-Notes-for-Interview](https://github.com/vivienzou1/DL-Notes-for-Interview) |  |  |  |

## opencv/opencv

Projet source : [ouvrir sur GitHub](https://github.com/opencv/opencv)

Besoin du développeur : à compléter avant de noter.

| Candidat | Note 0 1 2 ou ? | Justification | Redondant avec |
|---|---|---|---|
| [carlosmccosta/Car-Detection](https://github.com/carlosmccosta/Car-Detection) |  |  |  |
| [rssr25/Computer-Vision](https://github.com/rssr25/Computer-Vision) |  |  |  |
| [luispedro/mahotas](https://github.com/luispedro/mahotas) |  |  |  |
| [Alireza-Akhavan/class.vision](https://github.com/Alireza-Akhavan/class.vision) |  |  |  |
| [ClarityCoders/ComputerVision-OpenCV](https://github.com/ClarityCoders/ComputerVision-OpenCV) |  |  |  |
| [YunchuZhang/PyImageSearch-Gurus-Course](https://github.com/YunchuZhang/PyImageSearch-Gurus-Course) |  |  |  |
| [PacktPublishing/Learning-OpenCV-4-Computer-Vision-with-Python-Third-Edition](https://github.com/PacktPublishing/Learning-OpenCV-4-Computer-Vision-with-Python-Third-Edition) |  |  |  |
| [GihanRathnayake/ComputerVision](https://github.com/GihanRathnayake/ComputerVision) |  |  |  |
| [osrf/ovc](https://github.com/osrf/ovc) |  |  |  |
| [MasteringOpenCV/code](https://github.com/MasteringOpenCV/code) |  |  |  |

## django/django

Projet source : [ouvrir sur GitHub](https://github.com/django/django)

Besoin du développeur : à compléter avant de noter.

| Candidat | Note 0 1 2 ou ? | Justification | Redondant avec |
|---|---|---|---|
| [dropseed/plain](https://github.com/dropseed/plain) |  |  |  |
| [clue/framework-x](https://github.com/clue/framework-x) |  |  |  |
| [torreyleonard/algotrader](https://github.com/torreyleonard/algotrader) |  |  |  |
| [encode/django-rest-framework](https://github.com/encode/django-rest-framework) |  |  |  |
| [manosim/django-rest-framework-docs](https://github.com/manosim/django-rest-framework-docs) |  |  |  |
| [jfinal/jfinal](https://github.com/jfinal/jfinal) |  |  |  |
| [softage0/algorithm-trading-webapp](https://github.com/softage0/algorithm-trading-webapp) |  |  |  |
| [StockSharp/StockSharp](https://github.com/StockSharp/StockSharp) |  |  |  |

## edtechre/pybroker

Projet source : [ouvrir sur GitHub](https://github.com/edtechre/pybroker)

Besoin du développeur : à compléter avant de noter.

| Candidat | Note 0 1 2 ou ? | Justification | Redondant avec |
|---|---|---|---|
| [AliHabibnia/Algorithmic_Trading_with_Python](https://github.com/AliHabibnia/Algorithmic_Trading_with_Python) |  |  |  |
| [joelowj/awesome-algorithmic-trading](https://github.com/joelowj/awesome-algorithmic-trading) |  |  |  |
| [stefan-jansen/machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) |  |  |  |
| [TheFourGreatErrors/alpha-rptr](https://github.com/TheFourGreatErrors/alpha-rptr) |  |  |  |
| [PacktPublishing/Machine-Learning-for-Algorithmic-Trading-Second-Edition_Original](https://github.com/PacktPublishing/Machine-Learning-for-Algorithmic-Trading-Second-Edition_Original) |  |  |  |
| [alkalescent/hyperdrive](https://github.com/alkalescent/hyperdrive) |  |  |  |
| [paulperry/quant](https://github.com/paulperry/quant) |  |  |  |
| [PyPatel/Machine-Learning-and-AI-in-Trading](https://github.com/PyPatel/Machine-Learning-and-AI-in-Trading) |  |  |  |
| [PacktPublishing/Learn-Algorithmic-Trading](https://github.com/PacktPublishing/Learn-Algorithmic-Trading) |  |  |  |
| [coding-kitties/investing-algorithm-framework](https://github.com/coding-kitties/investing-algorithm-framework) |  |  |  |

