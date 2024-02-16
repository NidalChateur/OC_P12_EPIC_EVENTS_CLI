[![Windows](https://img.shields.io/badge/Windows-11-blue.svg?logo=Powershell)](https://www.microsoft.com/fr-fr/windows)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1-blue.svg?logo=Powershell)](https://learn.microsoft.com/fr-fr/powershell/scripting/overview?view=powershell-7.4)

[![Python](https://raw.githubusercontent.com/NidalChateur/badges/779ce02cc0ce5bdc16ca2fe297b1229d4e5068d3/svg/python.svg)](https://www.python.org/) 
[![Poetry](https://img.shields.io/badge/poetry-1.7.1-blue.svg?logo=Poetry)](https://python-poetry.org/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Flake8](https://img.shields.io/badge/linting-flake8-yellowgreen.svg?logo=python)](https://github.com/pycqa/flake8)
[![Pylint](https://img.shields.io/badge/linting-pylint-yellowgreen.svg?logo=python)](https://github.com/pylint-dev/pylint)

# Projet EPIC EVENTS CRM 


Epic Events est une entreprise qui organise des événements (fêtes,
réunions professionnelles, manifestations hors les murs) pour ses clients.

Le logiciel CRM permet de collecter et de traiter les données des clients
et de leurs événements, tout en facilitant la communication entre les
différents pôles de l'entreprise.

Interface utilisateur en ligne de commande.



 ## Réalisations
 - <a href="https://github.com/NidalChateur/OC_P12_EPIC_EVENTS/blob/main/mission/schema_bdd.pdf">Schéma de base de donnée Epic Events.</a> 

## Cas d'usages

 #### Besoin généraux
- Chaque collaborateur doit avoir ses identifiants pour utiliser la
plateforme.

- Chaque collaborateur est associé à un rôle (suivant son
département).

- La plateforme doit permettre de stocker et de mettre à jour les
informations sur les clients, les contrats et les événements.

- Tous les collaborateurs doivent pouvoir accéder à tous les clients,
contrats et événements en lecture seule.

 #### Cas d'usages d'un utilisateur Gestion
1. Créer, mettre à jour et supprimer des collaborateurs dans le
système CRM.

2. Créer et modifier tous les contrats.

3. Filtrer l’affichage des événements, par exemple : afficher tous les
événements qui n’ont pas de « support » associé.

4. Modifier des événements (pour associer un collaborateur support à
l’événement).

 #### Cas d'usages d'un utilisateur Commercial

1. Créer des clients (le client leur sera automatiquement associé).

2.  Mettre à jour les clients dont ils sont responsables.

3.  Modifier/mettre à jour les contrats des clients dont ils sont
responsables.

4. Filtrer l’affichage des contrats, par exemple : afficher tous les
contrats qui ne sont pas encore signés, ou qui ne sont pas encore
entièrement payés.

5. Créer un événement pour un de leurs clients qui a signé un
contrat.

 #### Cas d'usages d'un utilisateur Support

1. Filtrer l’affichage des événements, par exemple : afficher
uniquement les événements qui leur sont attribués.

2. Mettre à jour les événements dont ils sont responsables

## Pré-requis

* Installer Python 3 : [Téléchargement Python 3](https://www.python.org/downloads/)
* Installer git : [Téléchargement Git](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git)

## Installation

### 1. Télécharger le projet sur votre répertoire local : 
```
git clone https://github.com/NidalChateur/OC_P12_EPIC_EVENTS
cd OC_P12_EPIC_EVENTS
```
### 2. Mettre en place un environnement virtuel :
* Créer l'environnement virtuel: `python -m venv env`

### 3. Activer l'environnement virtuel
* Activer l'environnement virtuel :
    * Windows : `env\Scripts\activate.bat`
    * Unix/MacOS : `source env/bin/activate`
   
### 4. Installer les dépendances du projet

```
python -m pip install --upgrade pip

pip install poetry

poetry install
```

### 5. Démarrage avec poetry
* Lancer le script à l'aide de la commande suivante : `poetry run python main.py`


Les étapes 1, 2 et 4 ne sont requises que pour l'installation initiale. Pour les lancements ultérieurs de l'application, il suffit d'exécuter les étapes 3 et 5 à partir du répertoire racine du projet.

## Générer un rapport d'erreur grâce à flake8

Flake8 est souvent utilisé pour vérifier le respect des conventions de style PEP 8 dans le code Python. Pour réaliser ceci, se positionner à la racine du projet puis exécuter dans le terminal : 

`poetry run flake8`

Un rapport d'erreur au format html sera alors disponible dans le dossier "flake8_html_report".

## Générer un rapport complet et détaillé de couverture de test 

La couverture de test vérifie le taux de lignes couvertes par des tests. 

Pour réaliser ceci, se positionner à la racine du projet puis exécuter dans le terminal : 

`poetry run pytest --cov=. --cov-report html`

Quand le script est terminé, vous découvrez qu'un nouveau dossier "htmlcov" a été créé à l'endroit où vous avez lancé la commande. Ce dossier contient différents documents dont des fichiers HTML.

Ouvrez le fichier "index.html" qui contient un résumé du rapport de couverture.

À partir de cette page, vous pourrez naviguer à travers les différents fichiers afin d’avoir le détail sur la couverture. Effectivement, vous aurez un rapport détaillé pour chaque fichier source sous le format HTML.

