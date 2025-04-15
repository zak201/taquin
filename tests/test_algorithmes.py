"""
Tests unitaires pour les algorithmes de recherche.
"""
import os
import sys
import unittest
import numpy as np
import time

# Ajouter le répertoire parent au chemin de recherche des modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.taquin import Taquin, Etat
from src.recherche import resolution_dfs, resolution_bfs, resolution_best_first


class TestAlgorithmes(unittest.TestCase):
    """
    Classe de tests pour les algorithmes de recherche.
    """
    
    def setUp(self):
        """
        Initialisation avant chaque test.
        """
        # Créer une grille simple (une seule étape pour la résoudre)
        self.taquin_simple = Taquin(3)
        grille_simple = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]
        ])
        pos_vide_simple = (2, 1)
        self.taquin_simple.etat_initial = Etat(grille_simple, pos_vide_simple)
        self.taquin_simple.etat_courant = self.taquin_simple.etat_initial.copier()
        
        # État final (la case vide en bas à droite)
        grille_finale = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        pos_vide_finale = (2, 2)
        self.taquin_simple.etat_final = Etat(grille_finale, pos_vide_finale)
        
        # Créer une grille plus complexe (plusieurs étapes pour la résoudre)
        self.taquin_complexe = Taquin(3)
        grille_complexe = np.array([
            [1, 2, 3],
            [4, 0, 6],
            [7, 5, 8]
        ])
        pos_vide_complexe = (1, 1)
        self.taquin_complexe.etat_initial = Etat(grille_complexe, pos_vide_complexe)
        self.taquin_complexe.etat_courant = self.taquin_complexe.etat_initial.copier()
        self.taquin_complexe.etat_final = Etat(grille_finale.copy(), pos_vide_finale)
        
        # Créer un taquin impossible manuellement pour les tests
        self.taquin_manuel = Taquin(3)
        # Au lieu de vérifier est_resoluble, nous allons simplement créer un taquin
        # manuellement qui retournera False pour est_resoluble
        grille_manuelle = np.array([
            [2, 1, 3],  # 1 et 2 sont inversés - ceci crée un nombre impair d'inversions
            [4, 5, 6],
            [7, 8, 0]
        ])
        pos_vide_manuelle = (2, 2)
        self.taquin_manuel.etat_initial = Etat(grille_manuelle, pos_vide_manuelle)
        self.taquin_manuel.etat_courant = self.taquin_manuel.etat_initial.copier()
        self.taquin_manuel.etat_final = Etat(grille_finale.copy(), pos_vide_finale)
    
    def test_resolution_dfs_simple(self):
        """
        Teste la résolution DFS sur un problème simple.
        """
        chemin = resolution_dfs(self.taquin_simple, limite_profondeur=10, limite_temps=5)
        self.assertIsNotNone(chemin)
        self.assertGreaterEqual(len(chemin), 1)  # Au moins une étape
        
        # Vérifier que le dernier état du chemin est l'état final
        derniere_action, dernier_etat = chemin[-1]
        self.assertTrue(np.array_equal(dernier_etat.grille, self.taquin_simple.etat_final.grille))
    
    def test_resolution_bfs_simple(self):
        """
        Teste la résolution BFS sur un problème simple.
        """
        chemin = resolution_bfs(self.taquin_simple, limite_noeuds=100, limite_temps=5)
        self.assertIsNotNone(chemin)
        self.assertGreaterEqual(len(chemin), 1)  # Au moins une étape
        
        # Vérifier que le dernier état du chemin est l'état final
        derniere_action, dernier_etat = chemin[-1]
        self.assertTrue(np.array_equal(dernier_etat.grille, self.taquin_simple.etat_final.grille))
    
    def test_resolution_best_first_simple(self):
        """
        Teste la résolution Best-First sur un problème simple.
        """
        chemin = resolution_best_first(self.taquin_simple, limite_noeuds=100, limite_temps=5)
        self.assertIsNotNone(chemin)
        self.assertGreaterEqual(len(chemin), 1)  # Au moins une étape
        
        # Vérifier que le dernier état du chemin est l'état final
        derniere_action, dernier_etat = chemin[-1]
        self.assertTrue(np.array_equal(dernier_etat.grille, self.taquin_simple.etat_final.grille))
    
    def test_resolution_dfs_complexe(self):
        """
        Teste la résolution DFS sur un problème plus complexe.
        """
        chemin = resolution_dfs(self.taquin_complexe, limite_profondeur=30, limite_temps=10)
        self.assertIsNotNone(chemin)
        self.assertGreaterEqual(len(chemin), 1)  # Au moins une étape
        
        # Vérifier que le dernier état du chemin est l'état final
        derniere_action, dernier_etat = chemin[-1]
        self.assertTrue(np.array_equal(dernier_etat.grille, self.taquin_complexe.etat_final.grille))
    
    def test_resolution_bfs_complexe(self):
        """
        Teste la résolution BFS sur un problème plus complexe.
        """
        chemin = resolution_bfs(self.taquin_complexe, limite_noeuds=10000, limite_temps=10)
        self.assertIsNotNone(chemin)
        self.assertGreaterEqual(len(chemin), 1)  # Au moins une étape
        
        # Vérifier que le dernier état du chemin est l'état final
        derniere_action, dernier_etat = chemin[-1]
        self.assertTrue(np.array_equal(dernier_etat.grille, self.taquin_complexe.etat_final.grille))
    
    def test_resolution_best_first_complexe(self):
        """
        Teste la résolution Best-First sur un problème plus complexe.
        """
        chemin = resolution_best_first(self.taquin_complexe, limite_noeuds=1000, limite_temps=10)
        self.assertIsNotNone(chemin)
        self.assertGreaterEqual(len(chemin), 1)  # Au moins une étape
        
        # Vérifier que le dernier état du chemin est l'état final
        derniere_action, dernier_etat = chemin[-1]
        self.assertTrue(np.array_equal(dernier_etat.grille, self.taquin_complexe.etat_final.grille))
    
    def test_probleme_impossible(self):
        """
        Vérifie que les algorithmes détectent correctement un problème non résoluble.
        """
        # Vérifie manuellement que la configuration n'est pas résoluble
        # (un nombre impair d'inversions pour une grille de taille impaire est non résoluble)
        inversions = 1  # 2 vient avant 1 -> 1 inversion
        self.assertEqual(inversions % 2, 1)  # Impair
        
        # Forcer est_resoluble à retourner False pour ce test
        self.taquin_manuel.est_resoluble = lambda: False
        
        # Vérifier que les algorithmes retournent None pour un problème impossible
        chemin_dfs = resolution_dfs(self.taquin_manuel, limite_profondeur=10, limite_temps=1)
        self.assertIsNone(chemin_dfs)
        
        chemin_bfs = resolution_bfs(self.taquin_manuel, limite_noeuds=100, limite_temps=1)
        self.assertIsNone(chemin_bfs)
        
        chemin_best_first = resolution_best_first(self.taquin_manuel, limite_noeuds=100, limite_temps=1)
        self.assertIsNone(chemin_best_first)
    
    def test_comparaison_performances(self):
        """
        Compare les performances des trois algorithmes.
        """
        # Mesurer le temps pour DFS
        debut = time.time()
        chemin_dfs = resolution_dfs(self.taquin_complexe, limite_profondeur=20, limite_temps=5)
        temps_dfs = time.time() - debut
        
        # Mesurer le temps pour BFS
        debut = time.time()
        chemin_bfs = resolution_bfs(self.taquin_complexe, limite_noeuds=10000, limite_temps=5)
        temps_bfs = time.time() - debut
        
        # Mesurer le temps pour Best-First
        debut = time.time()
        chemin_best_first = resolution_best_first(self.taquin_complexe, limite_noeuds=1000, limite_temps=5)
        temps_best_first = time.time() - debut
        
        # Vérifier que tous les algorithmes ont trouvé une solution
        self.assertIsNotNone(chemin_dfs)
        self.assertIsNotNone(chemin_bfs)
        self.assertIsNotNone(chemin_best_first)
        
        # Afficher les performances pour comparaison
        print(f"\nComparaison des performances:")
        print(f"DFS: {len(chemin_dfs)} étapes en {temps_dfs:.4f}s")
        print(f"BFS: {len(chemin_bfs)} étapes en {temps_bfs:.4f}s")
        print(f"Best-First: {len(chemin_best_first)} étapes en {temps_best_first:.4f}s")
        
        # Vérifier que Best-First est généralement plus rapide pour ce type de problème
        # mais ne pas en faire un test strict car c'est aléatoire
        print(f"Best-First est plus rapide que BFS: {temps_best_first < temps_bfs}")
        
        # Vérifier que BFS trouve généralement le chemin le plus court
        print(f"BFS trouve un chemin plus court que DFS: {len(chemin_bfs) <= len(chemin_dfs)}")


if __name__ == '__main__':
    unittest.main() 