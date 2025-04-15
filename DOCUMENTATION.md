# Documentation du Jeu de Taquin

Ce document présente une vue d'ensemble du projet de Jeu de Taquin et explique comment utiliser les différents algorithmes de résolution implémentés.

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Structure du projet](#structure-du-projet)
3. [Algorithmes implémentés](#algorithmes-implémentés)
4. [Heuristiques disponibles](#heuristiques-disponibles)
5. [Comment exécuter les algorithmes](#comment-exécuter-les-algorithmes)
6. [Analyses comparatives](#analyses-comparatives)
7. [Résultats obtenus](#résultats-obtenus)

## Vue d'ensemble

Le Jeu de Taquin (ou puzzle à glisser) est un jeu de logique où l'on doit reconstituer une configuration finale à partir d'une configuration initiale, en déplaçant des pièces adjacentes à un espace vide. Ce projet fournit une implémentation du jeu avec des caractères et propose plusieurs algorithmes de résolution.

Le projet a été implémenté en Python et unifié dans un seul module `taquin_complet.py` pour faciliter son utilisation.

## Structure du projet

- `src/taquin_complet.py`: Module principal contenant toutes les fonctionnalités
- `data/taquin_instances.py`: Définitions des instances de test (configurations initiales et finales)
- `analyse_toutes_instances.py`: Script pour analyser toutes les instances disponibles
- `src/analyse_comparative.py`: Script pour comparer les différents algorithmes et heuristiques

## Algorithmes implémentés

Quatre algorithmes de recherche sont disponibles pour résoudre le jeu de Taquin :

1. **DFS** (Depth-First Search / Parcours en profondeur) : Explore l'arbre de recherche en profondeur d'abord. Non optimal en termes de longueur de solution, mais peut être efficace en mémoire.

2. **BFS** (Breadth-First Search / Parcours en largeur) : Explore l'arbre de recherche en largeur d'abord. Garantit des solutions optimales (nombre minimal d'étapes) mais consomme plus de mémoire.

3. **Best-First Search** (Recherche par le meilleur d'abord) : Utilise une heuristique pour guider la recherche vers les états les plus prometteurs. Non garanti d'être optimal mais plus efficace que BFS en termes de nœuds explorés.

4. **A*** (A-Star) : Combine BFS avec une heuristique pour guider la recherche. Optimal si l'heuristique est admissible. Généralement le meilleur compromis entre optimalité et efficacité.

## Heuristiques disponibles

Pour les algorithmes Best-First et A*, deux heuristiques sont disponibles, sélectionnées pour leur efficacité optimale :

1. **lineaire** : Prend en compte les conflits linéaires en plus de la distance de Manhattan, particulièrement efficace pour les grands puzzles.

2. **combinee** : Combine plusieurs métriques pour une estimation plus précise, généralement la plus performante pour la plupart des instances.

Ces deux heuristiques ont été retenues après analyse comparative car elles offrent les meilleurs résultats en termes d'efficacité et de temps de calcul.

## Comment exécuter les algorithmes

### Exécution simple d'un algorithme sur une instance

```bash
# Format général
python -m src.taquin_complet -i <instance> -a <algorithme> [-u <heuristique>] [-t <temps_limite>] [-l <limite_noeuds>]

# Exemples
# Résoudre taquin_3x3b avec BFS
python -m src.taquin_complet -i taquin_3x3b -a bfs

# Résoudre taquin_4x4 avec A* et l'heuristique combinée
python -m src.taquin_complet -i taquin_4x4 -a a-star -u combinee

# Résoudre taquin_2x4b avec DFS avec une limite de 1000 nœuds
python -m src.taquin_complet -i taquin_2x4b -a dfs -l 1000

# Résoudre taquin_5x5b avec Best-First et l'heuristique linéaire
python -m src.taquin_complet -i taquin_5x5b -a best-first -u lineaire
```

### Comparer les heuristiques sur une instance

```bash
# Compare les heuristiques linéaire et combinée sur une instance
python -m src.taquin_complet -i <instance> -c

# Exemple
python -m src.taquin_complet -i taquin_3x3b -c
```

### Analyser toutes les instances disponibles

```bash
# Exécuter l'analyse sur toutes les instances avec A* et l'heuristique combinée
python analyse_toutes_instances.py
```

## Analyses comparatives

Pour réaliser des analyses plus complètes et générer des graphiques, utilisez le script `src/analyse_comparative.py` :

```bash
# Exécuter les tests comparatifs complets
python -m src.analyse_comparative
```

Cela génère :
- Des tableaux comparatifs pour chaque instance
- Des graphiques de performance dans le dossier `graphiques/`
- Un rapport détaillé `rapport_analyse.md`

## Résultats obtenus

Nos analyses montrent que :

1. **A* avec l'heuristique combinée** offre généralement les meilleures performances pour la plupart des instances.

2. **Répartition des résultats** : 16/25 instances (64%) ont été résolues avec succès.

3. **Performances par taille** :
   - 2x4 : 3/4 instances résolues (75%)
   - 3x3 : 2/4 instances résolues (50%)
   - 3x4 : 0/4 instances résolues (0%)
   - 4x4 : 5/7 instances résolues (71%)
   - 5x5 : 6/6 instances résolues (100%)

4. **Complexité variable** :
   - Certaines instances sont résolues très rapidement (<0.1s)
   - D'autres sont beaucoup plus complexes (jusqu'à 17s de calcul)
   - Le nombre d'étapes varie de 18 à 166 selon l'instance

5. **Meilleure heuristique** : L'heuristique combinée est généralement la plus performante, suivie de l'heuristique linéaire.

### Tableau comparatif des algorithmes

| Algorithme | Optimalité | Mémoire | Temps de calcul | Commentaire |
|------------|------------|---------|----------------|-------------|
| DFS        | Non        | Basse   | Variable       | Peut trouver des solutions très longues |
| BFS        | Oui        | Haute   | Élevé          | Garantit les solutions optimales |
| Best-First | Non        | Moyenne | Moyen          | Bon compromis pour instances difficiles |
| A*         | Oui*       | Moyenne | Bas            | Meilleur algorithme dans la plupart des cas |

\* Si l'heuristique est admissible.

### Tableau comparatif des heuristiques retenues

| Heuristique | Performance | Complexité de calcul | Commentaire |
|-------------|-------------|----------------------|-------------|
| lineaire    | Très bonne  | Haute                | Très efficace pour les grands puzzles |
| combinee    | Excellente  | Haute                | Meilleure heuristique dans la plupart des cas | 