#!/usr/bin/env python3
"""
Implémentation complète du jeu de Taquin avec caractères alphabétiques.
Le fichier regroupe toutes les fonctionnalités en un seul module.
"""
import os
import sys
import time
import argparse
from collections import deque
import numpy as np
from typing import List, Tuple, Optional, Dict, Set

# ============================================================================
# PARTIE 1: STRUCTURES DE DONNÉES
# ============================================================================

class Etat:
    """
    Classe représentant un état du jeu de Taquin avec des caractères.
    """
    def __init__(self, grille: np.ndarray, pos_vide: Tuple[int, int]):
        """
        Initialise un état du jeu.
        
        Args:
            grille: La grille de jeu sous forme de tableau numpy 2D de caractères
            pos_vide: La position de la case vide (ligne, colonne)
        """
        self.grille = grille
        self.pos_vide = pos_vide
    
    def __eq__(self, other):
        """Vérifie si deux états sont identiques"""
        if not isinstance(other, Etat):
            return False
        return np.array_equal(self.grille, other.grille)
    
    def __hash__(self):
        """Permet d'utiliser les états comme clés de dictionnaire"""
        return hash(str(self.grille))
    
    def copier(self) -> 'Etat':
        """Crée une copie profonde de l'état actuel"""
        return Etat(self.grille.copy(), self.pos_vide)


class Taquin:
    """
    Classe principale du jeu de Taquin pour des caractères.
    """
    def __init__(self, taille_x: int = 3, taille_y: int = 3):
        """
        Initialise un jeu de Taquin avec des caractères.
        
        Args:
            taille_x: Nombre de lignes de la grille (par défaut 3)
            taille_y: Nombre de colonnes de la grille (par défaut 3)
        """
        self.taille_x = taille_x
        self.taille_y = taille_y
        self.etat_initial = None
        self.etat_final = None
        self.etat_courant = None
        self.caractere_vide = ' '  # Espace vide
        
    def charger_depuis_fichier(self, chemin_fichier: str) -> bool:
        """
        Charge une grille de Taquin avec des caractères depuis un fichier.
        
        Args:
            chemin_fichier: Chemin vers le fichier contenant la grille
            
        Returns:
            bool: True si le chargement a réussi, False sinon
        """
        try:
            with open(chemin_fichier, 'r') as f:
                lignes = f.readlines()
            
            # Première ligne contient la taille
            self.taille_x = int(lignes[0].strip())
            
            # Pour un taquin rectangulaire, on détermine la taille y à partir des données
            ligne_donnees = lignes[1].strip()
            self.taille_y = len(ligne_donnees)
            
            # Lire la configuration initiale
            grille_initiale = np.empty((self.taille_x, self.taille_y), dtype='U1')
            pos_vide_initiale = None
            
            for i in range(self.taille_x):
                ligne = lignes[i+1].strip()
                for j in range(self.taille_y):
                    if j < len(ligne):
                        caractere = ligne[j]
                        grille_initiale[i, j] = caractere
                        if caractere == self.caractere_vide:
                            pos_vide_initiale = (i, j)
                    else:
                        grille_initiale[i, j] = ' '  # Pad avec des espaces si nécessaire
            
            # Si on n'a pas trouvé la case vide lors de la lecture, cherchons-la
            if pos_vide_initiale is None:
                for i in range(self.taille_x):
                    for j in range(self.taille_y):
                        if grille_initiale[i, j] == self.caractere_vide:
                            pos_vide_initiale = (i, j)
                            break
                    if pos_vide_initiale is not None:
                        break
            
            if pos_vide_initiale is None:
                print("Erreur: Aucune case vide (espace) trouvée dans la grille initiale")
                return False
                
            # Créer l'état initial
            self.etat_initial = Etat(grille_initiale, pos_vide_initiale)
            self.etat_courant = self.etat_initial.copier()
            
            # Lire la configuration finale
            if len(lignes) > self.taille_x + 1:
                # Identifier où se termine la grille initiale (lorsqu'on trouve 'elus' ou 'fin')
                idx_separation = 0
                for i, ligne in enumerate(lignes[1:self.taille_x+1], 1):
                    if ligne.strip() in ['elus', 'fin']:
                        idx_separation = i
                        break
                
                if idx_separation > 0:
                    # Lire la configuration finale à partir de la ligne de séparation
                    grille_finale = np.empty((self.taille_x, self.taille_y), dtype='U1')
                    pos_vide_finale = None
                    
                    for i in range(self.taille_x):
                        idx = i + idx_separation + 1
                        if idx < len(lignes):
                            ligne = lignes[idx].strip()
                            for j in range(self.taille_y):
                                if j < len(ligne):
                                    caractere = ligne[j]
                                    grille_finale[i, j] = caractere
                                    if caractere == self.caractere_vide:
                                        pos_vide_finale = (i, j)
                                else:
                                    grille_finale[i, j] = ' '  # Pad avec des espaces si nécessaire
                    
                    # Si on n'a pas trouvé la case vide lors de la lecture, cherchons-la
                    if pos_vide_finale is None:
                        for i in range(self.taille_x):
                            for j in range(self.taille_y):
                                if grille_finale[i, j] == self.caractere_vide:
                                    pos_vide_finale = (i, j)
                                    break
                            if pos_vide_finale is not None:
                                break
                    
                    if pos_vide_finale is None:
                        print("Erreur: Aucune case vide (espace) trouvée dans la grille finale")
                        return False
                        
                    self.etat_final = Etat(grille_finale, pos_vide_finale)
                else:
                    # Méthode directe: lire les lignes qui suivent la configuration initiale
                    grille_finale = np.empty((self.taille_x, self.taille_y), dtype='U1')
                    pos_vide_finale = None
                    
                    for i in range(self.taille_x):
                        idx = i + self.taille_x + 1
                        if idx < len(lignes):
                            ligne = lignes[idx].strip()
                            for j in range(self.taille_y):
                                if j < len(ligne):
                                    caractere = ligne[j]
                                    grille_finale[i, j] = caractere
                                    if caractere == self.caractere_vide:
                                        pos_vide_finale = (i, j)
                                else:
                                    grille_finale[i, j] = ' '  # Pad avec des espaces
                    
                    # Si on n'a pas trouvé la case vide lors de la lecture, cherchons-la
                    if pos_vide_finale is None:
                        for i in range(self.taille_x):
                            for j in range(self.taille_y):
                                if grille_finale[i, j] == self.caractere_vide:
                                    pos_vide_finale = (i, j)
                                    break
                            if pos_vide_finale is not None:
                                break
                    
                    if pos_vide_finale is None:
                        print("Erreur: Aucune case vide (espace) trouvée dans la grille finale")
                        return False
                        
                    self.etat_final = Etat(grille_finale, pos_vide_finale)
            else:
                # Si la configuration finale n'est pas fournie, on génère une configuration
                print("Configuration finale non fournie, utilisation d'une configuration arbitraire.")
                return False
            
            return True
            
        except Exception as e:
            print(f"Erreur lors du chargement du fichier: {e}")
            return False
    
    def charger_depuis_chaine(self, contenu: str) -> bool:
        """
        Charge une grille de Taquin depuis une chaîne de caractères.
        
        Args:
            contenu: Contenu de la configuration (même format que le fichier)
            
        Returns:
            bool: True si le chargement a réussi, False sinon
        """
        try:
            # Créer un fichier temporaire
            fichier_temp = "temp_taquin.txt"
            with open(fichier_temp, 'w') as f:
                f.write(contenu)
            
            # Charger depuis le fichier temporaire
            resultat = self.charger_depuis_fichier(fichier_temp)
            
            # Supprimer le fichier temporaire
            if os.path.exists(fichier_temp):
                os.remove(fichier_temp)
                
            return resultat
            
        except Exception as e:
            print(f"Erreur lors du chargement de la chaîne: {e}")
            return False
    
    def afficher_grille(self, etat: Optional[Etat] = None):
        """
        Affiche la grille du jeu.
        
        Args:
            etat: État du jeu à afficher (état courant par défaut)
        """
        if etat is None:
            etat = self.etat_courant
            
        if etat is None:
            print("Aucune grille à afficher")
            return
            
        print(f"Grille {self.taille_x}x{self.taille_y}:")
        print('-' * (self.taille_y * 4 + 1))
        
        for i in range(self.taille_x):
            ligne = '|'
            for j in range(self.taille_y):
                caractere = etat.grille[i, j]
                if caractere == self.caractere_vide:
                    ligne += '   |'  # Case vide
                else:
                    ligne += f' {caractere} |'
            print(ligne)
            print('-' * (self.taille_y * 4 + 1))
    
    def est_resolu(self) -> bool:
        """
        Vérifie si le jeu est résolu.
        
        Returns:
            bool: True si l'état courant est égal à l'état final, False sinon
        """
        if self.etat_courant is None or self.etat_final is None:
            return False
        return self.etat_courant == self.etat_final
        
    def deplacer(self, etat: Etat, direction: str) -> Optional[Etat]:
        """
        Déplace la case vide dans la direction indiquée et retourne le nouvel état.
        
        Args:
            etat: État actuel
            direction: Direction du déplacement ('haut', 'bas', 'gauche', 'droite')
            
        Returns:
            Etat: Nouvel état après déplacement, None si le déplacement est impossible
        """
        i, j = etat.pos_vide
        nouvel_etat = None
        
        if direction == 'haut' and i > 0:
            # Déplacer la case du haut vers le bas
            nouvel_etat = etat.copier()
            nouvel_etat.grille[i, j] = nouvel_etat.grille[i-1, j]
            nouvel_etat.grille[i-1, j] = self.caractere_vide
            nouvel_etat.pos_vide = (i-1, j)
            
        elif direction == 'bas' and i < self.taille_x - 1:
            # Déplacer la case du bas vers le haut
            nouvel_etat = etat.copier()
            nouvel_etat.grille[i, j] = nouvel_etat.grille[i+1, j]
            nouvel_etat.grille[i+1, j] = self.caractere_vide
            nouvel_etat.pos_vide = (i+1, j)
            
        elif direction == 'gauche' and j > 0:
            # Déplacer la case de gauche vers la droite
            nouvel_etat = etat.copier()
            nouvel_etat.grille[i, j] = nouvel_etat.grille[i, j-1]
            nouvel_etat.grille[i, j-1] = self.caractere_vide
            nouvel_etat.pos_vide = (i, j-1)
            
        elif direction == 'droite' and j < self.taille_y - 1:
            # Déplacer la case de droite vers la gauche
            nouvel_etat = etat.copier()
            nouvel_etat.grille[i, j] = nouvel_etat.grille[i, j+1]
            nouvel_etat.grille[i, j+1] = self.caractere_vide
            nouvel_etat.pos_vide = (i, j+1)
            
        return nouvel_etat
    
    def obtenir_etats_voisins(self, etat: Etat) -> List[Etat]:
        """
        Obtient tous les états possibles en déplaçant la case vide dans toutes les directions possibles.
        
        Args:
            etat: État actuel
            
        Returns:
            List[Etat]: Liste des états voisins possibles
        """
        directions = ['haut', 'bas', 'gauche', 'droite']
        etats_voisins = []
        
        for direction in directions:
            nouvel_etat = self.deplacer(etat, direction)
            if nouvel_etat is not None:
                etats_voisins.append(nouvel_etat)
                
        return etats_voisins
    
    def est_resoluble(self) -> bool:
        """
        Vérifie si la configuration actuelle du jeu est résoluble.
        Pour un jeu de taquin avec des caractères, on suppose que
        toutes les configurations sont résolubles pour simplifier.
        
        Returns:
            bool: True si la configuration est résoluble, False sinon
        """
        if self.etat_courant is None or self.etat_final is None:
            return False
        
        # Pour un jeu de taquin alpha, on simplifie en supposant que
        # toutes les configurations sont résolubles
        return True
        
    # ----- HEURISTIQUES -----
    
    def calculer_distance_manhattan(self, etat: Etat) -> int:
        """
        Calcule la distance de Manhattan entre l'état donné et l'état final.
        La distance de Manhattan est la somme des distances horizontales et verticales
        que chaque caractère doit parcourir pour atteindre sa position finale.
        
        Args:
            etat: État pour lequel calculer la distance
            
        Returns:
            int: Somme des distances de Manhattan
        """
        if self.etat_final is None:
            return 0
            
        distance = 0
        # Créer un dictionnaire pour accélérer la recherche des positions finales
        positions_finales = {}
        
        # Mémoriser les positions de chaque caractère dans l'état final
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                caractere = self.etat_final.grille[i, j]
                positions_finales[caractere] = (i, j)
        
        # Calculer la distance de Manhattan pour chaque caractère
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                caractere = etat.grille[i, j]
                if caractere != self.caractere_vide:  # Ignorer la case vide
                    if caractere in positions_finales:
                        pos_finale = positions_finales[caractere]
                        # Calculer la distance horizontale + verticale
                        distance += abs(i - pos_finale[0]) + abs(j - pos_finale[1])
        
        return distance
    
    def calculer_cases_mal_placees(self, etat: Etat) -> int:
        """
        Calcule le nombre de cases qui ne sont pas à leur place finale.
        
        Args:
            etat: État pour lequel calculer l'heuristique
            
        Returns:
            int: Nombre de cases mal placées
        """
        if self.etat_final is None:
            return 0
            
        nb_mal_places = 0
        
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                if etat.grille[i, j] != self.caractere_vide:  # Ignorer la case vide
                    if etat.grille[i, j] != self.etat_final.grille[i, j]:
                        nb_mal_places += 1
        
        return nb_mal_places
    
    def calculer_distance_euclidienne(self, etat: Etat) -> float:
        """
        Calcule la distance euclidienne (en ligne droite) entre l'état donné et l'état final.
        
        Args:
            etat: État pour lequel calculer la distance
            
        Returns:
            float: Somme des distances euclidiennes pour chaque caractère
        """
        if self.etat_final is None:
            return 0
            
        distance = 0.0
        # Créer un dictionnaire pour accélérer la recherche
        positions_finales = {}
        
        # Mémoriser les positions de chaque caractère dans l'état final
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                caractere = self.etat_final.grille[i, j]
                positions_finales[caractere] = (i, j)
        
        # Calculer la distance euclidienne pour chaque caractère
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                caractere = etat.grille[i, j]
                if caractere != self.caractere_vide:  # Ignorer la case vide
                    if caractere in positions_finales:
                        pos_finale = positions_finales[caractere]
                        # Calculer la distance euclidienne (√((x2-x1)² + (y2-y1)²))
                        distance += ((i - pos_finale[0])**2 + (j - pos_finale[1])**2)**0.5
        
        return distance
    
    def calculer_heuristique_nilsson(self, etat: Etat) -> int:
        """
        Calcule l'heuristique de Nilsson qui combine la distance de Manhattan
        avec une pénalité pour les caractères qui ne suivent pas l'ordre séquentiel.
        
        Args:
            etat: État pour lequel calculer l'heuristique
            
        Returns:
            int: Valeur de l'heuristique de Nilsson
        """
        if self.etat_final is None:
            return 0
            
        # Calculer la distance de Manhattan de base
        manhattan = self.calculer_distance_manhattan(etat)
        
        # Ajouter une pénalité pour les séquences incorrectes
        penalite = 0
        
        # Créer un dictionnaire pour les positions finales
        positions_finales = {}
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                caractere = self.etat_final.grille[i, j]
                positions_finales[caractere] = (i, j)
        
        # Vérifier les séquences horizontales et verticales
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                caractere = etat.grille[i, j]
                if caractere != self.caractere_vide:
                    # Vérifier les voisins horizontaux et verticaux
                    # Horizontal: vérifier si le caractère à droite est le successeur dans l'état final
                    if j < self.taille_y - 1:
                        voisin_droit = etat.grille[i, j+1]
                        if voisin_droit != self.caractere_vide:
                            # On vérifie s'ils sont adjacents dans l'état final
                            pos_finale_courant = positions_finales.get(caractere, (-1, -1))
                            pos_finale_voisin = positions_finales.get(voisin_droit, (-1, -1))
                            
                            if (pos_finale_courant[0] == pos_finale_voisin[0] and 
                                abs(pos_finale_courant[1] - pos_finale_voisin[1]) == 1):
                                # Si adjacents dans l'état final mais pas dans le même ordre
                                if pos_finale_courant[1] + 1 != pos_finale_voisin[1]:
                                    penalite += 2
                    
                    # Vertical: vérifier si le caractère en dessous est le successeur dans l'état final
                    if i < self.taille_x - 1:
                        voisin_bas = etat.grille[i+1, j]
                        if voisin_bas != self.caractere_vide:
                            # On vérifie s'ils sont adjacents dans l'état final
                            pos_finale_courant = positions_finales.get(caractere, (-1, -1))
                            pos_finale_voisin = positions_finales.get(voisin_bas, (-1, -1))
                            
                            if (pos_finale_courant[1] == pos_finale_voisin[1] and 
                                abs(pos_finale_courant[0] - pos_finale_voisin[0]) == 1):
                                # Si adjacents dans l'état final mais pas dans le même ordre
                                if pos_finale_courant[0] + 1 != pos_finale_voisin[0]:
                                    penalite += 2
        
        return manhattan + 3 * penalite
    
    def calculer_heuristique_lineaire(self, etat: Etat) -> int:
        """
        Calcule une heuristique basée sur les conflits linéaires.
        Un conflit linéaire se produit quand deux caractères dans leur ligne/colonne finale
        sont dans le désordre, nécessitant des déplacements supplémentaires.
        
        Args:
            etat: État pour lequel calculer l'heuristique
            
        Returns:
            int: Valeur de l'heuristique avec conflits linéaires
        """
        if self.etat_final is None:
            return 0
            
        # Calculer la distance de Manhattan de base
        manhattan = self.calculer_distance_manhattan(etat)
        
        # Ajouter la pénalité pour les conflits linéaires
        conflits = 0
        
        # Créer des dictionnaires pour accélérer la recherche
        positions_finales = {}
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                caractere = self.etat_final.grille[i, j]
                positions_finales[caractere] = (i, j)
        
        # Vérifier les conflits sur les lignes
        for i in range(self.taille_x):
            # Collecter les caractères de cette ligne qui sont déjà dans leur ligne finale
            dans_ligne_finale = []
            for j in range(self.taille_y):
                caractere = etat.grille[i, j]
                if caractere != self.caractere_vide:
                    pos_finale = positions_finales.get(caractere, (-1, -1))
                    if pos_finale[0] == i:  # Si le caractère est dans sa ligne finale
                        dans_ligne_finale.append((j, caractere))
            
            # Vérifier les conflits parmi ces caractères
            for idx1, (j1, car1) in enumerate(dans_ligne_finale):
                for j2, car2 in dans_ligne_finale[idx1+1:]:
                    pos_finale1 = positions_finales[car1][1]
                    pos_finale2 = positions_finales[car2][1]
                    # Conflit si dans la même ligne et dans le désordre
                    if pos_finale1 > pos_finale2 and j1 < j2:
                        conflits += 2
                    elif pos_finale1 < pos_finale2 and j1 > j2:
                        conflits += 2
        
        # Vérifier les conflits sur les colonnes
        for j in range(self.taille_y):
            # Collecter les caractères de cette colonne qui sont déjà dans leur colonne finale
            dans_colonne_finale = []
            for i in range(self.taille_x):
                caractere = etat.grille[i, j]
                if caractere != self.caractere_vide:
                    pos_finale = positions_finales.get(caractere, (-1, -1))
                    if pos_finale[1] == j:  # Si le caractère est dans sa colonne finale
                        dans_colonne_finale.append((i, caractere))
            
            # Vérifier les conflits parmi ces caractères
            for idx1, (i1, car1) in enumerate(dans_colonne_finale):
                for i2, car2 in dans_colonne_finale[idx1+1:]:
                    pos_finale1 = positions_finales[car1][0]
                    pos_finale2 = positions_finales[car2][0]
                    # Conflit si dans la même colonne et dans le désordre
                    if pos_finale1 > pos_finale2 and i1 < i2:
                        conflits += 2
                    elif pos_finale1 < pos_finale2 and i1 > i2:
                        conflits += 2
        
        return manhattan + conflits
    
    def calculer_heuristique_combinee(self, etat: Etat) -> float:
        """
        Calcule l'heuristique combinée qui combine la distance de Manhattan
        avec une pénalité pour les caractères qui ne suivent pas l'ordre séquentiel.
        
        Args:
            etat: État pour lequel calculer l'heuristique
            
        Returns:
            float: Valeur de l'heuristique combinée
        """
        if self.etat_final is None:
            return 0
            
        manhattan = self.calculer_distance_manhattan(etat)
        mal_places = self.calculer_cases_mal_placees(etat)
        lineaire = self.calculer_heuristique_lineaire(etat)
        
        return (manhattan + 3 * mal_places + lineaire)
    
    def calculer_heuristique_pattern_database(self, etat: Etat) -> int:
        """
        Utilise une approche simplifiée de pattern database.
        Se concentre sur certaines parties spécifiques de la grille (comme les coins).
        
        Args:
            etat: État pour lequel calculer l'heuristique
            
        Returns:
            int: Valeur de l'heuristique pattern database
        """
        if self.etat_final is None:
            return 0
            
        # Utiliser la distance Manhattan comme base
        manhattan = self.calculer_distance_manhattan(etat)
        
        # Ajouter une pénalité spécifique pour les coins et les bords
        penalite_coins = 0
        
        # Positions des coins
        coins = [(0, 0), (0, self.taille_y-1), (self.taille_x-1, 0), (self.taille_x-1, self.taille_y-1)]
        
        # Récupérer les caractères attendus aux coins dans l'état final
        caracteres_coins = []
        for i, j in coins:
            if i < self.taille_x and j < self.taille_y:
                caracteres_coins.append(self.etat_final.grille[i, j])
        
        # Créer un dictionnaire des positions dans l'état courant
        positions_courantes = {}
        for i in range(self.taille_x):
            for j in range(self.taille_y):
                caractere = etat.grille[i, j]
                positions_courantes[caractere] = (i, j)
        
        # Pénalité pour les coins mal placés
        for idx, caractere in enumerate(caracteres_coins):
            if caractere != self.caractere_vide:
                if caractere in positions_courantes:
                    i, j = positions_courantes[caractere]
                    i_coin, j_coin = coins[idx]
                    if i != i_coin or j != j_coin:
                        # Pénalité plus forte si un caractère de coin n'est pas à sa place
                        penalite_coins += 3 * (abs(i - i_coin) + abs(j - j_coin))
        
        return manhattan + penalite_coins


# ============================================================================
# PARTIE 2: ALGORITHMES DE RECHERCHE
# ============================================================================

class NoeudRecherche:
    """
    Classe représentant un nœud dans l'arbre de recherche.
    """
    def __init__(self, etat: Etat, parent=None, action=None, profondeur=0):
        """
        Initialise un nœud de recherche.
        
        Args:
            etat: État du jeu
            parent: Nœud parent dans l'arbre de recherche
            action: Action qui a mené à cet état depuis le parent
            profondeur: Profondeur du nœud dans l'arbre de recherche
        """
        self.etat = etat
        self.parent = parent
        self.action = action
        self.profondeur = profondeur
        
    def __lt__(self, other):
        """
        Comparaison pour la file de priorité dans Best-First Search.
        """
        return False  # On définit une relation d'ordre par défaut
        
    def reconstruire_chemin(self) -> List[Tuple[str, Etat]]:
        """
        Reconstruit le chemin depuis la racine jusqu'à ce nœud.
        
        Returns:
            Liste de tuples (action, état) représentant le chemin
        """
        chemin = []
        noeud_courant = self
        
        while noeud_courant.parent is not None:
            chemin.append((noeud_courant.action, noeud_courant.etat))
            noeud_courant = noeud_courant.parent
            
        # Le chemin est dans l'ordre inverse (de la fin au début)
        chemin.reverse()
        return chemin


class NoeudPriorise(NoeudRecherche):
    """
    Nœud avec une priorité pour les algorithmes Best-First et A*.
    """
    def __init__(self, etat: Etat, parent=None, action=None, profondeur=0, priorite=0):
        super().__init__(etat, parent, action, profondeur)
        self.priorite = priorite
        
    def __lt__(self, other):
        """
        Comparaison pour la file de priorité.
        """
        if not isinstance(other, NoeudPriorise):
            return NotImplemented
        return self.priorite < other.priorite


def resolution_dfs(taquin: Taquin, limite_profondeur=100, limite_temps=30) -> Optional[List[Tuple[str, Etat]]]:
    """
    Résout le Taquin par parcours en profondeur (DFS).
    
    Args:
        taquin: Instance du jeu de Taquin
        limite_profondeur: Profondeur maximale de recherche
        limite_temps: Limite de temps en secondes
        
    Returns:
        Chemin de résolution ou None si pas de solution trouvée
    """
    if taquin.etat_initial is None or taquin.etat_final is None:
        return None
        
    # Vérifier que la configuration est résoluble
    if not taquin.est_resoluble():
        print("Cette configuration n'est pas résoluble.")
        return None
        
    # Initialisation
    debut_temps = time.time()
    pile = [NoeudRecherche(taquin.etat_initial)]
    etats_visites = set()
    nb_noeuds_explores = 0
    
    while pile and (time.time() - debut_temps) < limite_temps:
        noeud_courant = pile.pop()
        nb_noeuds_explores += 1
        
        # Vérifier si l'état est le but
        if np.array_equal(noeud_courant.etat.grille, taquin.etat_final.grille):
            print(f"Solution trouvée! Noeuds explorés: {nb_noeuds_explores}")
            return noeud_courant.reconstruire_chemin()
            
        # Éviter les cycles et limiter la profondeur
        etat_hash = hash(noeud_courant.etat)
        if etat_hash in etats_visites or noeud_courant.profondeur >= limite_profondeur:
            continue
            
        etats_visites.add(etat_hash)
        
        # Expanser le nœud
        if noeud_courant.profondeur < limite_profondeur:
            etats_voisins = taquin.obtenir_etats_voisins(noeud_courant.etat)
            
            # Les directions possibles
            directions = ['haut', 'bas', 'gauche', 'droite']
            
            # Pour chaque direction possible
            for i, voisin in enumerate(etats_voisins):
                action = directions[i] if i < len(directions) else "inconnu"
                pile.append(NoeudRecherche(
                    voisin, 
                    noeud_courant, 
                    action, 
                    noeud_courant.profondeur + 1
                ))
    
    # Si on sort de la boucle, c'est qu'on n'a pas trouvé de solution
    print(f"Pas de solution trouvée. Noeuds explorés: {nb_noeuds_explores}")
    return None


def resolution_bfs(taquin: Taquin, limite_noeuds=100000, limite_temps=30) -> Optional[List[Tuple[str, Etat]]]:
    """
    Résout le Taquin par parcours en largeur (BFS).
    
    Args:
        taquin: Instance du jeu de Taquin
        limite_noeuds: Nombre maximal de nœuds à explorer
        limite_temps: Limite de temps en secondes
        
    Returns:
        Chemin de résolution ou None si pas de solution trouvée
    """
    if taquin.etat_initial is None or taquin.etat_final is None:
        return None
        
    # Vérifier que la configuration est résoluble
    if not taquin.est_resoluble():
        print("Cette configuration n'est pas résoluble.")
        return None
        
    # Initialisation
    debut_temps = time.time()
    file = deque([NoeudRecherche(taquin.etat_initial)])
    etats_visites = set([hash(taquin.etat_initial)])
    nb_noeuds_explores = 0
    
    # Les directions possibles
    directions = ['haut', 'bas', 'gauche', 'droite']
    
    while file and nb_noeuds_explores < limite_noeuds and (time.time() - debut_temps) < limite_temps:
        noeud_courant = file.popleft()
        nb_noeuds_explores += 1
        
        # Vérifier si l'état est le but
        if np.array_equal(noeud_courant.etat.grille, taquin.etat_final.grille):
            print(f"Solution trouvée! Noeuds explorés: {nb_noeuds_explores}")
            return noeud_courant.reconstruire_chemin()
        
        # Expanser le nœud
        etats_voisins = taquin.obtenir_etats_voisins(noeud_courant.etat)
        
        # Pour chaque voisin
        for i, voisin in enumerate(etats_voisins):
            etat_hash = hash(voisin)
            if etat_hash not in etats_visites:
                etats_visites.add(etat_hash)
                action = directions[i] if i < len(directions) else "inconnu"
                file.append(NoeudRecherche(
                    voisin, 
                    noeud_courant, 
                    action, 
                    noeud_courant.profondeur + 1
                ))
    
    # Si on sort de la boucle, c'est qu'on n'a pas trouvé de solution
    print(f"Pas de solution trouvée. Noeuds explorés: {nb_noeuds_explores}")
    return None


def resolution_best_first(taquin: Taquin, limite_noeuds=100000, limite_temps=30, 
                          heuristique='combinee') -> Optional[List[Tuple[str, Etat]]]:
    """
    Résout le Taquin par parcours meilleur d'abord (Best-First Search).
    
    Args:
        taquin: Instance du jeu de Taquin
        limite_noeuds: Nombre maximal de nœuds à explorer
        limite_temps: Limite de temps en secondes
        heuristique: Heuristique à utiliser ('lineaire' ou 'combinee')
        
    Returns:
        Chemin de résolution ou None si pas de solution trouvée
    """
    if taquin.etat_initial is None or taquin.etat_final is None:
        return None
        
    # Vérifier que la configuration est résoluble
    if not taquin.est_resoluble():
        print("Cette configuration n'est pas résoluble.")
        return None
        
    # Sélectionner l'heuristique appropriée
    heuristique_func = None
    if heuristique == 'lineaire':
        heuristique_func = taquin.calculer_heuristique_lineaire
    elif heuristique == 'combinee':
        heuristique_func = taquin.calculer_heuristique_combinee
    else:
        print(f"Heuristique '{heuristique}' non reconnue. Utilisation de l'heuristique combinée par défaut.")
        heuristique_func = taquin.calculer_heuristique_combinee
        
    # Initialisation
    debut_temps = time.time()
    priorite_initiale = heuristique_func(taquin.etat_initial)
    
    # File de priorité : (priorité, compteur, nœud)
    # Le compteur sert à départager les nœuds de même priorité
    import heapq
    compteur = 0
    file_priorite = [(priorite_initiale, compteur, NoeudPriorise(taquin.etat_initial, priorite=priorite_initiale))]
    heapq.heapify(file_priorite)
    
    etats_visites = set([hash(taquin.etat_initial)])
    nb_noeuds_explores = 0
    
    # Les directions possibles
    directions = ['haut', 'bas', 'gauche', 'droite']
    
    while file_priorite and nb_noeuds_explores < limite_noeuds and (time.time() - debut_temps) < limite_temps:
        _, _, noeud_courant = heapq.heappop(file_priorite)
        nb_noeuds_explores += 1
        
        # Vérifier si l'état est le but
        if np.array_equal(noeud_courant.etat.grille, taquin.etat_final.grille):
            print(f"Solution trouvée! Noeuds explorés: {nb_noeuds_explores}")
            return noeud_courant.reconstruire_chemin()
        
        # Expanser le nœud
        etats_voisins = taquin.obtenir_etats_voisins(noeud_courant.etat)
        
        # Pour chaque voisin
        for i, voisin in enumerate(etats_voisins):
            etat_hash = hash(voisin)
            if etat_hash not in etats_visites:
                etats_visites.add(etat_hash)
                action = directions[i] if i < len(directions) else "inconnu"
                
                # Calculer la priorité en utilisant l'heuristique sélectionnée
                priorite = heuristique_func(voisin)
                compteur += 1
                
                nouveau_noeud = NoeudPriorise(
                    voisin, 
                    noeud_courant, 
                    action, 
                    noeud_courant.profondeur + 1,
                    priorite=priorite
                )
                
                heapq.heappush(file_priorite, (priorite, compteur, nouveau_noeud))
    
    # Si on sort de la boucle, c'est qu'on n'a pas trouvé de solution
    print(f"Pas de solution trouvée. Noeuds explorés: {nb_noeuds_explores}")
    return None


def resolution_a_star(taquin: Taquin, limite_noeuds=100000, limite_temps=30, 
                    heuristique='combinee') -> Optional[List[Tuple[str, Etat]]]:
    """
    Résout le Taquin par algorithme A* (A-Star).
    Diffère du Best-First en ajoutant le coût du chemin parcouru à l'heuristique.
    
    Args:
        taquin: Instance du jeu de Taquin
        limite_noeuds: Nombre maximal de nœuds à explorer
        limite_temps: Limite de temps en secondes
        heuristique: Heuristique à utiliser ('lineaire' ou 'combinee')
        
    Returns:
        Chemin de résolution ou None si pas de solution trouvée
    """
    if taquin.etat_initial is None or taquin.etat_final is None:
        return None
        
    # Vérifier que la configuration est résoluble
    if not taquin.est_resoluble():
        print("Cette configuration n'est pas résoluble.")
        return None
        
    # Sélectionner l'heuristique appropriée
    heuristique_func = None
    if heuristique == 'lineaire':
        heuristique_func = taquin.calculer_heuristique_lineaire
    elif heuristique == 'combinee':
        heuristique_func = taquin.calculer_heuristique_combinee
    else:
        print(f"Heuristique '{heuristique}' non reconnue. Utilisation de l'heuristique combinée par défaut.")
        heuristique_func = taquin.calculer_heuristique_combinee
        
    # Initialisation
    debut_temps = time.time()
    h_initial = heuristique_func(taquin.etat_initial)
    
    # Dans A*, la priorité est f(n) = g(n) + h(n) où:
    # - g(n) est le coût du chemin de l'état initial à l'état n (ici, la profondeur)
    # - h(n) est l'heuristique estimant le coût de n à l'état final
    cout_initial = 0  # g(n) pour l'état initial
    priorite_initiale = cout_initial + h_initial  # f(n) = g(n) + h(n)
    
    # File de priorité : (priorité, compteur, nœud)
    import heapq
    compteur = 0
    file_priorite = [(priorite_initiale, compteur, NoeudPriorise(taquin.etat_initial, priorite=priorite_initiale))]
    heapq.heapify(file_priorite)
    
    etats_visites = set([hash(taquin.etat_initial)])
    nb_noeuds_explores = 0
    
    # Les directions possibles
    directions = ['haut', 'bas', 'gauche', 'droite']
    
    while file_priorite and nb_noeuds_explores < limite_noeuds and (time.time() - debut_temps) < limite_temps:
        _, _, noeud_courant = heapq.heappop(file_priorite)
        nb_noeuds_explores += 1
        
        # Vérifier si l'état est le but
        if np.array_equal(noeud_courant.etat.grille, taquin.etat_final.grille):
            print(f"Solution trouvée! Noeuds explorés: {nb_noeuds_explores}")
            return noeud_courant.reconstruire_chemin()
        
        # Expanser le nœud
        etats_voisins = taquin.obtenir_etats_voisins(noeud_courant.etat)
        
        # Pour chaque voisin
        for i, voisin in enumerate(etats_voisins):
            etat_hash = hash(voisin)
            if etat_hash not in etats_visites:
                etats_visites.add(etat_hash)
                action = directions[i] if i < len(directions) else "inconnu"
                
                # Coût du chemin jusqu'ici (g(n))
                cout = noeud_courant.profondeur + 1
                
                # Valeur heuristique (h(n))
                h = heuristique_func(voisin)
                
                # Priorité totale f(n) = g(n) + h(n)
                priorite = cout + h
                compteur += 1
                
                nouveau_noeud = NoeudPriorise(
                    voisin, 
                    noeud_courant, 
                    action, 
                    cout,  # La profondeur correspond au coût du chemin
                    priorite=priorite
                )
                
                heapq.heappush(file_priorite, (priorite, compteur, nouveau_noeud))
    
    # Si on sort de la boucle, c'est qu'on n'a pas trouvé de solution
    print(f"Pas de solution trouvée. Noeuds explorés: {nb_noeuds_explores}")
    return None


def comparer_heuristiques(taquin: Taquin, limite_noeuds=10000, limite_temps=30) -> Dict:
    """
    Compare les performances des différentes heuristiques.
    
    Args:
        taquin: Instance du jeu de Taquin
        limite_noeuds: Nombre maximal de nœuds à explorer
        limite_temps: Limite de temps en secondes
        
    Returns:
        Dict: Dictionnaire contenant les résultats pour chaque heuristique
    """
    heuristiques = [
        'lineaire', 
        'combinee'
    ]
    
    resultats = {}
    
    for h in heuristiques:
        print(f"\nTest de l'heuristique: {h}")
        debut = time.time()
        chemin = resolution_a_star(taquin, limite_noeuds=limite_noeuds, 
                                      limite_temps=limite_temps, heuristique=h)
        temps_execution = time.time() - debut
        
        if chemin:
            resultats[h] = {
                'succes': True,
                'nb_etapes': len(chemin),
                'temps': temps_execution
            }
            print(f"Solution trouvée en {len(chemin)} étapes et {temps_execution:.4f} secondes.")
        else:
            resultats[h] = {
                'succes': False,
                'temps': temps_execution
            }
            print(f"Pas de solution trouvée en {temps_execution:.4f} secondes.")
    
    return resultats


# ============================================================================
# PARTIE 3: INTERFACE UTILISATEUR
# ============================================================================

def afficher_solution(taquin, chemin):
    """
    Affiche la solution étape par étape.
    
    Args:
        taquin: Instance du jeu de Taquin
        chemin: Liste de tuples (action, état) représentant la solution
    """
    print("\nSolution trouvée en", len(chemin), "étapes:")
    print("\nÉtat initial:")
    taquin.afficher_grille(taquin.etat_initial)
    
    for i, (action, etat) in enumerate(chemin):
        print(f"\nÉtape {i+1}: {action}")
        taquin.afficher_grille(etat)
    
    print("\nProblème résolu!")


# ============================================================================
# PARTIE 4: INSTANCES PRÉ-DÉFINIES
# ============================================================================

INSTANCES = {
    "taquin_2x4d": """2
isfn
l ue
elus
fin""",

    "taquin_3x3": """3
123
745
8  6
123
456
78""",

    "taquin_2x4c": """2
fnlu
ei s
elus
fin""",

    "taquin_5x5b": """5
wqpgo
utrla
bvdxc
 eskn
fhmij
abcde
fghij
klmno
pqrst
uvwx""",

    "taquin_3x3d": """3
123
456
87
123
456
78""",

    "taquin_4x4f": """4
ainh
 cdl
gbkf
ojme
abcd
efgh
ijkl
mno""",

    "taquin_3x3b": """3
8 6
123
745
123
456
78""",

    "taquin_3x4": """3
seul
kit 
farn
elus
kart
fin""",

    "taquin_4x4": """4
abcd
mno 
efgh
ijkl
abcd
efgh
ijkl
mno""",

    "taquin_2x4b": """2
lnuf
e is
elus
fin""",

    "taquin_3x4b": """3
kel 
itus 
farn
elus
kart
fin""",

    "taquin_4x4e": """4
abcd
mfng
e ho
ijkl
abcd
efgh
ijkl
mno""",

    "taquin_4x4d": """4
o lc
edgm
jnki
habf
abcd
efgh
ijkl
mno""",

    "taquin_4x4b": """4
abcd
efgh
ijkl
mno 
abcd
efgh
ijkl
mon""",

    "taquin_3x3c": """3
826
13 
745
123
456
78""",

    "taquin_3x4c": """3
kart
fin 
elus
elus
kart
fin""",

    "taquin_5x5e": """5
abcde
fghij
mn ot
lkqrs
puvwx
abcde
fghij
klmno
pqrst
uvwx""",

    "taquin_5x5d": """5
desno
cq uk
plwxv
amjbr
fghit
abcde
fghij
klmno
pqrst
uvwx""",

    "taquin_4x4c": """4
jhcd
afg 
lbki
eonm
abcd
efgh
ijkl
mno""",

    "taquin_5x5f": """5
fahce
kbmdj
pgrio
u wnt
qlvsx
abcde
fghij
klmno
pqrst
uvwx""",

    "taquin_3x4d": """3
kart
 fin
elus
elus
kart
fin""",

    "taquin_5x5": """5
abcde
fghij
klmno
pqrst
uvwx 
klmno
pqrst
uvwx 
abcde
fghij""",

    "taquin_4x4g": """4
acf 
ebgd
ijlh
mnko
abcd
efgh
ijkl
mno""",

    "taquin_5x5c": """5
kivnh
pqcst
mrlaw
jb du
fgoxe
abcde
fghij
klmno
pqrst
uvwx""",

    "taquin_2x4": """2
elus
fin 
fin 
elus"""
}


# ============================================================================
# PARTIE 5: FONCTION PRINCIPALE
# ============================================================================

def main():
    """
    Fonction principale du programme.
    """
    # Configurer le parseur d'arguments
    parser = argparse.ArgumentParser(description="Résolution du jeu de Taquin avec caractères")
    parser.add_argument("--fichier", "-f", help="Chemin vers le fichier contenant la grille")
    parser.add_argument("--instance", "-i", choices=INSTANCES.keys(), help="Utiliser une instance prédéfinie")
    parser.add_argument(
        "--algorithme", "-a",
        choices=["dfs", "bfs", "best-first", "a-star"],
        default="bfs",
        help="Algorithme à utiliser (par défaut: bfs)"
    )
    parser.add_argument(
        "--heuristique", "-u",
        choices=["lineaire", "combinee"],
        default="combinee",
        help="Heuristique à utiliser pour Best-First ou A* (par défaut: combinee)"
    )
    parser.add_argument(
        "--temps", "-t",
        type=int,
        default=30,
        help="Limite de temps en secondes (par défaut: 30)"
    )
    parser.add_argument(
        "--limite", "-l",
        type=int,
        default=100000,
        help="Limite de nœuds ou de profondeur (par défaut: 100000)"
    )
    parser.add_argument(
        "--comparer", "-c",
        action="store_true",
        help="Comparer les performances des différentes heuristiques"
    )
    
    args = parser.parse_args()
    
    # Créer une instance du jeu
    taquin = Taquin()
    
    # Charger la configuration
    if args.fichier:
        # Vérifier que le fichier existe
        if not os.path.isfile(args.fichier):
            print(f"Erreur: Le fichier '{args.fichier}' n'existe pas.")
            return 1
            
        if not taquin.charger_depuis_fichier(args.fichier):
            print("Erreur lors du chargement de la grille.")
            return 1
    elif args.instance:
        # Utiliser une instance prédéfinie
        if not taquin.charger_depuis_chaine(INSTANCES[args.instance]):
            print(f"Erreur lors du chargement de l'instance {args.instance}.")
            return 1
    else:
        print("Erreur: Vous devez spécifier un fichier (--fichier) ou une instance prédéfinie (--instance).")
        return 1
    
    # Afficher la grille chargée
    print("\nGrille chargée avec succès:")
    taquin.afficher_grille()
    
    print("\nÉtat final à atteindre:")
    taquin.afficher_grille(taquin.etat_final)
    
    # Vérifier si la grille est déjà résolue
    if taquin.est_resolu():
        print("La grille est déjà résolue!")
        return 0
    
    # Si l'option est de comparer les heuristiques
    if args.comparer:
        print("\nComparaison des performances des différentes heuristiques...")
        resultats = comparer_heuristiques(taquin, limite_noeuds=args.limite, limite_temps=args.temps)
        
        # Afficher un tableau de comparaison
        print("\n" + "=" * 80)
        print(f"{'Heuristique':20} | {'Succès':8} | {'Étapes':8} | {'Temps (s)':12}")
        print("-" * 80)
        
        for h, res in resultats.items():
            succes = "Oui" if res.get('succes', False) else "Non"
            etapes = str(res.get('nb_etapes', '-')) if res.get('succes', False) else "-"
            temps = f"{res.get('temps', 0):.4f}"
            print(f"{h:20} | {succes:8} | {etapes:8} | {temps:12}")
        
        print("=" * 80)
        return 0
    
    # Résoudre le problème avec l'algorithme choisi
    print(f"\nRésolution avec l'algorithme {args.algorithme}" + 
          (f" (heuristique: {args.heuristique})" if args.algorithme in ['best-first', 'a-star'] else "") + 
          "...")
    debut = time.time()
    
    if args.algorithme == "dfs":
        chemin = resolution_dfs(taquin, limite_profondeur=args.limite, limite_temps=args.temps)
    elif args.algorithme == "bfs":
        chemin = resolution_bfs(taquin, limite_noeuds=args.limite, limite_temps=args.temps)
    elif args.algorithme == "best-first":
        chemin = resolution_best_first(taquin, limite_noeuds=args.limite, limite_temps=args.temps, 
                                    heuristique=args.heuristique)
    else:  # a-star
        chemin = resolution_a_star(taquin, limite_noeuds=args.limite, limite_temps=args.temps, 
                                 heuristique=args.heuristique)
    
    temps_total = time.time() - debut
    
    if chemin:
        print(f"Solution trouvée en {temps_total:.2f} secondes.")
        afficher_solution(taquin, chemin)
    else:
        print(f"Pas de solution trouvée dans le temps imparti ({temps_total:.2f} secondes).")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 