# Jeu de Taquin

Ce projet implémente le jeu de Taquin en Python.

## Installation

1. Cloner le dépôt
```
git clone [URL_DU_DEPOT]
cd taquin
```

2. Créer un environnement virtuel (recommandé)
```
python -m venv venv
venv\Scripts\activate  # Sur Windows
source venv/bin/activate  # Sur Unix/MacOS
```

3. Installer les dépendances
```
pip install -r requirements.txt
```

## Utilisation

Pour charger et afficher une grille de Taquin à partir d'un fichier :
```
python src/main.py data/exemple.txt
```

## Structure du projet

- `src/` : Code source du projet
- `data/` : Fichiers de grilles de Taquin
- `tests/` : Tests unitaires 