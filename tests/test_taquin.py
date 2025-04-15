"""
Tests unitaires pour le jeu de Taquin.
"""
import os
import sys
import unittest
import numpy as np

# Ajouter le répertoire parent au chemin de recherche des modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.taquin import Taquin, Etat


class TestTaquin(unittest.TestCase):
    """Classe de tests pour le jeu de Taquin."""
    
    def setUp(self):
        """Initialisation avant chaque test."""
        self.taquin = Taquin(3)
        
        # Créer une grille de test 3x3
        grille = np.array([
            [1, 2, 3],
            [4, 0, 6],
            [7, 5, 8]
        ])
        pos_vide = (1, 1)
        self.taquin.etat_initial = Etat(grille, pos_vide)
        self.taquin.etat_courant = self.taquin.etat_initial.copier()
        
        # Créer l'état final (grille ordonnée)
        grille_finale = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ])
        pos_vide_finale = (2, 2)
        self.taquin.etat_final = Etat(grille_finale, pos_vide_finale)
    
    def test_chargement_fichier(self):
        """Teste le chargement d'une grille depuis un fichier."""
        # Créer un fichier temporaire pour le test
        with open('test_grid.txt', 'w') as f:
            f.write("3\n")
            f.write("1 2 3\n")
            f.write("4 0 6\n")
            f.write("7 5 8\n")
        
        # Créer un nouveau jeu pour tester le chargement
        taquin_test = Taquin()
        resultat = taquin_test.charger_depuis_fichier('test_grid.txt')
        
        # Supprimer le fichier temporaire
        os.remove('test_grid.txt')
        
        # Vérifier que le chargement a réussi
        self.assertTrue(resultat)
        self.assertEqual(taquin_test.taille, 3)
        self.assertEqual(taquin_test.etat_courant.pos_vide, (1, 1))
        self.assertTrue(np.array_equal(taquin_test.etat_courant.grille, self.taquin.etat_courant.grille))
    
    def test_est_resoluble(self):
        """Teste la détection de configuration résoluble."""
        # Notre configuration de test doit être résoluble
        self.assertTrue(self.taquin.est_resoluble())
        
        # Créer une configuration non résoluble en permutant deux cases
        taquin_non_resoluble = Taquin(3)
        grille = np.array([
            [1, 2, 3],
            [4, 0, 6],
            [5, 7, 8]  # 5 et 7 sont permutés par rapport à l'ordre normal
        ])
        pos_vide = (1, 1)
        taquin_non_resoluble.etat_initial = Etat(grille, pos_vide)
        taquin_non_resoluble.etat_courant = taquin_non_resoluble.etat_initial.copier()
        taquin_non_resoluble.etat_final = self.taquin.etat_final.copier()
        
        # Pour une grille 3x3, permuter deux cases rend la configuration non résoluble
        self.assertFalse(taquin_non_resoluble.est_resoluble())
    
    def test_est_resolu(self):
        """Teste la détection d'un état résolu."""
        # L'état initial n'est pas résolu
        self.assertFalse(self.taquin.est_resolu())
        
        # Modifier l'état courant pour qu'il soit égal à l'état final
        self.taquin.etat_courant = self.taquin.etat_final.copier()
        
        # Maintenant, l'état courant est résolu
        self.assertTrue(self.taquin.est_resolu())


if __name__ == '__main__':
    unittest.main() 