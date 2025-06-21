# Projet Apiculture

## Introduction

Projet apiculture madame Baovola. Samy manana dossier-any tsirairay avy par modules (jereo repartition.docx).

## Structure du projet

Mitovy daholo structure dossier na routes, na views, na models.
Jereo projet/routes/dashboard.py, projet/views/dashboard.py, projet/models/dashboard.py, projet/templates/dashboard/index.html pour exemple.

- projet/routes : Misy ny routes rehetra
- projet/views : Misy ny views rehetra
- projet/models : Misy ny models rehetra
- projet/templates : Misy ny templates rehetra

## Remarques

- Tandremo ny fichier css, js, etc miady

## Installation

- Cloner le projet.
- Activer l'environnement virtuel :
  1) linux : `source venv/bin/activate`
  2) windows : `venv\Scripts\activate`
- Installer les dependencies : `pip install -r requirements.txt`
- Migrations de la base de données : `python manage.py migrate`
- Lancer le projet : `python manage.py runserver`
