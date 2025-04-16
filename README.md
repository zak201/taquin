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

Pour comparer tous les algorithmes (DFS, BFS, Best-First, A*) sur plusieurs instances :
```bash
python generer_graphiques.py
```
Cette commande génère des tableaux comparatifs et des graphiques visuels.

Pour analyser toutes les instances disponibles avec A* et l'heuristique combinée :
```bash
python analyse_toutes_instances.py
```

Les graphiques seront sauvegardés dans le dossier `graphiques/` et incluent :
- Temps d'exécution par algorithme
- Nombre de nœuds explorés
- Longueur des solutions
- Efficacité (nœuds explorés par étape)

## Documentation complète

Pour une documentation détaillée sur les algorithmes, les heuristiques, les analyses comparatives et les résultats obtenus, consultez le fichier [DOCUMENTATION.md](DOCUMENTATION.md).

## Structure du projet

- `src/taquin_complet.py` : Module principal contenant toutes les fonctionnalités
- `data/taquin_instances.py` : Instances de test prédéfinies
- `generer_graphiques.py` : Script pour générer des graphiques comparatifs
- `analyse_toutes_instances.py` : Script pour tester toutes les instances
- `DOCUMENTATION.md` : Documentation complète du projet

## Comparaison des algorithmes

Le projet implémente quatre algorithmes de recherche différents, chacun avec ses avantages et inconvénients :

### BFS (Breadth-First Search / Recherche en largeur)
- **Principe** : Explore l'arbre de recherche niveau par niveau.
- **Garanties** : Trouve toujours la solution optimale (moins d'étapes).
- **Points forts** : Optimalité garantie.
- **Points faibles** : Consommation mémoire élevée, exploration exhaustive.
- **Exemples de résultats** :
  - Sur instance 3x3b : 21 étapes, 60785 nœuds explorés, 5.46s
  - Ne parvient pas à résoudre les instances 4x4 et 5x5 complexes dans un temps raisonnable.

### DFS (Depth-First Search / Recherche en profondeur)
- **Principe** : Explore l'arbre de recherche en profondeur d'abord.
- **Garanties** : Trouve une solution si elle existe (sans limite de profondeur).
- **Points forts** : Faible consommation mémoire.
- **Points faibles** : Solutions souvent très longues et non optimales.
- **Exemples de résultats** :
  - Sur instance 3x3b : 30993 étapes (!), 49794 nœuds explorés, 2s
  - Sur instance 2x4b : 12154 étapes, 19920 nœuds explorés, 0.52s

### Best-First Search (Recherche par le meilleur d'abord)
- **Principe** : Explore les nœuds selon une heuristique estimant la proximité au but.
- **Garanties** : Aucune garantie d'optimalité.
- **Points forts** : Très rapide, explore peu de nœuds.
- **Points faibles** : Peut trouver des solutions sous-optimales.
- **Exemples de résultats** :
  - Sur instance 3x3b (heuristique combinée) : 31 étapes, 54 nœuds explorés, 0.01s
  - Sur instance 4x4 (heuristique combinée) : 70 étapes, 468 nœuds explorés, 0.15s

### A* (A-Star)
- **Principe** : Combine BFS avec une heuristique, considère à la fois le coût déjà parcouru et l'estimation jusqu'au but.
- **Garanties** : Trouve la solution optimale si l'heuristique est admissible.
- **Points forts** : Optimal et efficace, explore beaucoup moins de nœuds que BFS.
- **Points faibles** : Peut être limité par la mémoire sur les instances très complexes.
- **Exemples de résultats** :
  - Sur instance 3x3b (heuristique combinée) : 21 étapes, 111 nœuds explorés, 0.02s
  - Sur instance 4x4 (heuristique combinée) : 46 étapes, 837 nœuds explorés, 0.27s

### Impact des heuristiques

Les deux heuristiques implémentées ont des impacts différents :

- **Heuristique linéaire** : 
  - Améliore Manhattan en ajoutant une pénalité pour les conflits entre pièces
  - Généralement performante sur les grilles de grande taille
  - Ex. sur 4x4 avec A* : 30 étapes, 9784 nœuds, 2.42s

- **Heuristique combinée** :
  - Fusion optimisée de plusieurs métriques (Manhattan, cases mal placées, conflits)
  - Généralement la plus efficace en nombre de nœuds explorés
  - Ex. sur 4x4 avec A* : 46 étapes, 837 nœuds, 0.27s

Pour des graphiques comparatifs détaillés, exécutez `python generer_graphiques.py` et consultez les résultats dans le dossier `graphiques/`.

## Résultats et performances

Selon nos analyses :
- L'algorithme A* avec l'heuristique combinée offre les meilleures performances
- 64% des instances ont été résolues avec succès
- Les instances 5x5 sont toutes résolubles, tandis que les instances 3x4 posent plus de difficultés
- Le nombre d'étapes dans les solutions varie de 18 à 166 selon l'instance

Pour plus de détails, consultez la section [Résultats obtenus](DOCUMENTATION.md#résultats-obtenus) dans la documentation. 