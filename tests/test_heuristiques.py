"""
Tests unitaires pour les différentes heuristiques.
"""
import os
import sys
import unittest
import numpy as np
import time

# Ajouter le répertoire parent au chemin de recherche des modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.taquin import Taquin, Etat
from src.recherche import resolution_best_first, resolution_a_star


class TestHeuristiques(unittest.TestCase):
    """
    Classe de tests pour les différentes heuristiques.
    """
    
    def setUp(self):
        """
        Initialisation avant chaque test.
        """
        # Créer une grille facile (une seule étape pour la résoudre)
        self.taquin_facile = Taquin(3)
        grille_facile = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 0, 8]
        ])
        pos_vide_facile = (2, 1)
        self.taquin_facile.etat_initial = Etat(grille_facile, pos_vide_facile)
        self.taquin_facile.etat_courant = self.taquin_facile.etat_initial.copier()
        
        # État final (la case vide en bas à droite)
        grille_finale = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        pos_vide_finale = (2, 2)
        self.taquin_facile.etat_final = Etat(grille_finale, pos_vide_finale)
        
        # Créer une grille de difficulté moyenne (quelques étapes pour la résoudre)
        self.taquin_moyen = Taquin(3)
        grille_moyenne = np.array([
            [1, 3, 6],
            [5, 2, 0],
            [4, 7, 8]
        ])
        pos_vide_moyenne = (1, 2)
        self.taquin_moyen.etat_initial = Etat(grille_moyenne, pos_vide_moyenne)
        self.taquin_moyen.etat_courant = self.taquin_moyen.etat_initial.copier()
        self.taquin_moyen.etat_final = Etat(grille_finale.copy(), pos_vide_finale)
        
        # Créer une grille complexe (plus difficile à résoudre)
        self.taquin_complexe = Taquin(3)
        grille_complexe = np.array([
            [8, 6, 7],
            [2, 5, 4],
            [3, 0, 1]
        ])
        pos_vide_complexe = (2, 1)
        self.taquin_complexe.etat_initial = Etat(grille_complexe, pos_vide_complexe)
        self.taquin_complexe.etat_courant = self.taquin_complexe.etat_initial.copier()
        self.taquin_complexe.etat_final = Etat(grille_finale.copy(), pos_vide_finale)
    
    def test_heuristiques_valeurs(self):
        """
        Teste que les différentes heuristiques retournent des valeurs cohérentes.
        Plus l'état est proche de la résolution, plus la valeur doit être faible.
        """
        # Grille facile (presque résolue)
        h_manhattan_facile = self.taquin_facile.calculer_distance_manhattan(self.taquin_facile.etat_initial)
        h_mal_places_facile = self.taquin_facile.calculer_cases_mal_placees(self.taquin_facile.etat_initial)
        h_euclidienne_facile = self.taquin_facile.calculer_distance_euclidienne(self.taquin_facile.etat_initial)
        h_nilsson_facile = self.taquin_facile.calculer_heuristique_nilsson(self.taquin_facile.etat_initial)
        h_lineaire_facile = self.taquin_facile.calculer_heuristique_lineaire(self.taquin_facile.etat_initial)
        
        # Grille moyenne (partiellement désordonnée)
        h_manhattan_moyen = self.taquin_moyen.calculer_distance_manhattan(self.taquin_moyen.etat_initial)
        h_mal_places_moyen = self.taquin_moyen.calculer_cases_mal_placees(self.taquin_moyen.etat_initial)
        h_euclidienne_moyen = self.taquin_moyen.calculer_distance_euclidienne(self.taquin_moyen.etat_initial)
        h_nilsson_moyen = self.taquin_moyen.calculer_heuristique_nilsson(self.taquin_moyen.etat_initial)
        h_lineaire_moyen = self.taquin_moyen.calculer_heuristique_lineaire(self.taquin_moyen.etat_initial)
        
        # Grille complexe (très désordonnée)
        h_manhattan_complexe = self.taquin_complexe.calculer_distance_manhattan(self.taquin_complexe.etat_initial)
        h_mal_places_complexe = self.taquin_complexe.calculer_cases_mal_placees(self.taquin_complexe.etat_initial)
        h_euclidienne_complexe = self.taquin_complexe.calculer_distance_euclidienne(self.taquin_complexe.etat_initial)
        h_nilsson_complexe = self.taquin_complexe.calculer_heuristique_nilsson(self.taquin_complexe.etat_initial)
        h_lineaire_complexe = self.taquin_complexe.calculer_heuristique_lineaire(self.taquin_complexe.etat_initial)
        
        # Afficher les valeurs des heuristiques
        print("\nValeurs des heuristiques pour différentes configurations:")
        print(f"{'Heuristique':15} | {'Facile':10} | {'Moyen':10} | {'Complexe':10}")
        print("-" * 50)
        print(f"{'Manhattan':15} | {h_manhattan_facile:10} | {h_manhattan_moyen:10} | {h_manhattan_complexe:10}")
        print(f"{'Cases mal placées':15} | {h_mal_places_facile:10} | {h_mal_places_moyen:10} | {h_mal_places_complexe:10}")
        print(f"{'Euclidienne':15} | {h_euclidienne_facile:10.2f} | {h_euclidienne_moyen:10.2f} | {h_euclidienne_complexe:10.2f}")
        print(f"{'Nilsson':15} | {h_nilsson_facile:10} | {h_nilsson_moyen:10} | {h_nilsson_complexe:10}")
        print(f"{'Linéaire':15} | {h_lineaire_facile:10} | {h_lineaire_moyen:10} | {h_lineaire_complexe:10}")
        
        # Vérifier que les valeurs sont cohérentes (croissantes avec la difficulté)
        self.assertLessEqual(h_manhattan_facile, h_manhattan_moyen)
        self.assertLessEqual(h_manhattan_moyen, h_manhattan_complexe)
        
        self.assertLessEqual(h_mal_places_facile, h_mal_places_moyen)
        self.assertLessEqual(h_mal_places_moyen, h_mal_places_complexe)
        
        self.assertLessEqual(h_euclidienne_facile, h_euclidienne_moyen)
        self.assertLessEqual(h_euclidienne_moyen, h_euclidienne_complexe)
        
        self.assertLessEqual(h_nilsson_facile, h_nilsson_moyen)
        self.assertLessEqual(h_nilsson_moyen, h_nilsson_complexe)
        
        self.assertLessEqual(h_lineaire_facile, h_lineaire_moyen)
        self.assertLessEqual(h_lineaire_moyen, h_lineaire_complexe)

    def test_resolution_best_first_toutes_heuristiques(self):
        """
        Teste que toutes les heuristiques permettent de résoudre le problème avec Best-First.
        """
        heuristiques = [
            'manhattan',
            'mal_places', 
            'euclidienne', 
            'nilsson', 
            'lineaire', 
            'combinee', 
            'pattern'
        ]
        
        # Test sur la grille moyenne
        print("\nTest de résolution Best-First avec différentes heuristiques (grille moyenne):")
        for h in heuristiques:
            debut = time.time()
            chemin = resolution_best_first(
                self.taquin_moyen, 
                limite_noeuds=10000, 
                limite_temps=15, 
                heuristique=h
            )
            temps = time.time() - debut
            
            # Vérifier que l'algorithme a trouvé une solution
            self.assertIsNotNone(chemin, f"L'heuristique {h} n'a pas trouvé de solution")
            print(f"Heuristique {h:10}: {len(chemin):2d} étapes en {temps:.4f}s avec {(len(chemin)/temps) if temps > 0 else 0:.2f} étapes/s")
    
    def test_resolution_a_star_toutes_heuristiques(self):
        """
        Teste que toutes les heuristiques permettent de résoudre le problème avec A*.
        """
        heuristiques = [
            'manhattan',
            'mal_places', 
            'euclidienne', 
            'nilsson', 
            'lineaire', 
            'combinee', 
            'pattern'
        ]
        
        # Test sur la grille moyenne
        print("\nTest de résolution A* avec différentes heuristiques (grille moyenne):")
        for h in heuristiques:
            debut = time.time()
            chemin = resolution_a_star(
                self.taquin_moyen, 
                limite_noeuds=10000, 
                limite_temps=15, 
                heuristique=h
            )
            temps = time.time() - debut
            
            # Vérifier que l'algorithme a trouvé une solution
            self.assertIsNotNone(chemin, f"L'heuristique {h} n'a pas trouvé de solution")
            print(f"Heuristique {h:10}: {len(chemin):2d} étapes en {temps:.4f}s avec {(len(chemin)/temps) if temps > 0 else 0:.2f} étapes/s")
    
    def test_efficacite_comparative(self):
        """
        Compare l'efficacité des différentes heuristiques sur la grille complexe.
        """
        heuristiques = [
            'manhattan',
            'mal_places', 
            'euclidienne', 
            'nilsson', 
            'lineaire', 
            'combinee', 
            'pattern'
        ]
        
        resultats = {}
        
        # Test sur la grille complexe avec Best-First
        print("\nComparaison d'efficacité Best-First (grille complexe):")
        for h in heuristiques:
            debut = time.time()
            chemin = resolution_best_first(
                self.taquin_complexe, 
                limite_noeuds=50000, 
                limite_temps=20, 
                heuristique=h
            )
            temps = time.time() - debut
            
            if chemin:
                resultats[h] = {
                    'algorithme': 'Best-First',
                    'succes': True,
                    'longueur': len(chemin),
                    'temps': temps,
                    'efficacite': len(chemin) / temps if temps > 0 else 0
                }
            else:
                resultats[h] = {
                    'algorithme': 'Best-First',
                    'succes': False,
                    'temps': temps
                }
        
        # Test sur la grille complexe avec A*
        print("\nComparaison d'efficacité A* (grille complexe):")
        for h in heuristiques:
            debut = time.time()
            chemin = resolution_a_star(
                self.taquin_complexe, 
                limite_noeuds=50000, 
                limite_temps=20, 
                heuristique=h
            )
            temps = time.time() - debut
            
            if chemin:
                resultats[f"a_star_{h}"] = {
                    'algorithme': 'A*',
                    'succes': True,
                    'longueur': len(chemin),
                    'temps': temps,
                    'efficacite': len(chemin) / temps if temps > 0 else 0
                }
            else:
                resultats[f"a_star_{h}"] = {
                    'algorithme': 'A*',
                    'succes': False,
                    'temps': temps
                }
        
        # Afficher les résultats
        print("\nRésultats de la comparaison d'efficacité:")
        print(f"{'Algorithme':10} | {'Heuristique':10} | {'Succès':6} | {'Longueur':8} | {'Temps (s)':9} | {'Étapes/s':8}")
        print("-" * 70)
        
        # Trier les résultats par succès puis par efficacité
        sorted_results = sorted(
            resultats.items(), 
            key=lambda x: (not x[1].get('succes', False), x[1].get('temps', float('inf')))
        )
        
        for name, res in sorted_results:
            algo = res.get('algorithme', '')
            heur = name.replace('a_star_', '') if algo == 'A*' else name
            succes = "Oui" if res.get('succes', False) else "Non"
            longueur = str(res.get('longueur', '-')) if res.get('succes', False) else '-'
            temps = f"{res.get('temps', 0):.4f}"
            efficacite = f"{res.get('efficacite', 0):.2f}" if res.get('succes', False) else '-'
            
            print(f"{algo:10} | {heur:10} | {succes:6} | {longueur:8} | {temps:9} | {efficacite:8}")


if __name__ == '__main__':
    unittest.main() 