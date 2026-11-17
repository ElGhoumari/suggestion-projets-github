# Système de suggestion de projets GitHub

## Présentation

Nous développons une application qui recommande des projets GitHub
similaires à un projet choisi par l’utilisateur.

Notre objectif est d’aider les développeurs à découvrir des outils,
des alternatives et des projets proches de leurs besoins.

## Fonctionnement prévu

L’utilisateur indique un repository GitHub. Le système analyse
ses informations et propose jusqu’à cinq repositories similaires,
avec leur description, leur lien et une explication de la suggestion.

## Notre approche

Nous allons collecter les descriptions, les topics et les README
avec l’API GitHub, puis nettoyer et stocker ces données.

Nous commencerons avec TF-IDF et la similarité cosinus.
Nous comparerons ensuite cette méthode à des embeddings et à
une recommandation fondée sur la popularité.

## Étapes du projet

1. Collecter un premier échantillon de données.
2. Nettoyer et explorer les données.
3. Construire une première méthode de recommandation.
4. Évaluer et comparer les résultats.
5. Créer une interface.
6. Automatiser les mises à jour et déployer l’application.

## Avancement

Le dépôt est créé. Nous commençons par la collecte et
l’exploration des données.
