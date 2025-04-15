# Jeu de Taquin

Une implémentation complète du jeu de Taquin en Python, avec plusieurs algorithmes de résolution et heuristiques avancées.

![Taquin](https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/15-puzzle.svg/220px-15-puzzle.svg.png)

## Fonctionnalités principales

- Implémentation unifiée dans un seul module (`taquin_complet.py`)
- Quatre algorithmes de résolution : DFS, BFS, Best-First Search, A*
- Deux heuristiques optimisées pour les algorithmes informés : linéaire et combinée
- Analyse comparative des performances
- 25 instances de test prédéfinies de différentes tailles (2x4, 3x3, 3x4, 4x4, 5x5)

## Installation

1. Cloner le dépôt
```bash
git clone [URL_DU_DEPOT]
cd taquin
```

2. Créer un environnement virtuel (recommandé)
```bash
python -m venv venv
venv\Scripts\activate  # Sur Windows
source venv/bin/activate  # Sur Unix/MacOS
```

3. Installer les dépendances
```bash
pip install numpy tabulate matplotlib
```

## Utilisation rapide

Pour résoudre une instance avec l'algorithme BFS (recherche en largeur):
```bash
python -m src.taquin_complet -i taquin_3x3b -a bfs
```

Pour résoudre une instance avec l'algorithme DFS (recherche en profondeur):
```bash
python -m src.taquin_complet -i taquin_2x4b -a dfs
```

Pour résoudre une instance avec l'algorithme A* et l'heuristique combinée:
```bash
python -m src.taquin_complet -i taquin_3x3b -a a-star -u combinee
```

Pour résoudre une instance avec l'algorithme Best-First et l'heuristique linéaire:
```bash
python -m src.taquin_complet -i taquin_5x5b -a best-first -u lineaire
```

Pour comparer les performances des deux heuristiques sur une instance :
```bash
python -m src.taquin_complet -i taquin_4x4 -c
```

Pour analyser toutes les instances disponibles :
```bash
python analyse_toutes_instances.py
```

## Documentation complète

Pour une documentation détaillée sur les algorithmes, les heuristiques, les analyses comparatives et les résultats obtenus, consultez le fichier [DOCUMENTATION.md](DOCUMENTATION.md).

## Structure du projet

- `src/taquin_complet.py` : Module principal contenant toutes les fonctionnalités
- `data/taquin_instances.py` : Instances de test prédéfinies
- `src/analyse_comparative.py` : Script d'analyse comparative des algorithmes
- `analyse_toutes_instances.py` : Script pour tester toutes les instances
- `DOCUMENTATION.md` : Documentation complète du projet

## Résultats et performances

Selon nos analyses :
- L'algorithme A* avec l'heuristique combinée offre les meilleures performances
- 64% des instances ont été résolues avec succès
- Les instances 5x5 sont toutes résolubles, tandis que les instances 3x4 posent plus de difficultés
- Le nombre d'étapes dans les solutions varie de 18 à 166 selon l'instance

Pour plus de détails, consultez la section [Résultats obtenus](DOCUMENTATION.md#résultats-obtenus) dans la documentation. 