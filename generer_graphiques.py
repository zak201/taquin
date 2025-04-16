#!/usr/bin/env python3
"""
Script pour générer des graphiques comparatifs des performances
des différents algorithmes et heuristiques pour la résolution du jeu de Taquin.
"""
import os
import time
import json
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
from typing import Dict, List, Tuple, Any, Optional

# Importer les instances de taquin
from src.taquin_complet import INSTANCES

def tester_algorithme(instance_name, algorithme, heuristique=None, limite_temps=30):
    """
    Teste un algorithme sur une instance donnée et retourne les résultats.
    
    Args:
        instance_name: Nom de l'instance à tester
        algorithme: Nom de l'algorithme ('dfs', 'bfs', 'best-first', 'a-star')
        heuristique: Nom de l'heuristique (pour best-first et a-star)
        limite_temps: Limite de temps en secondes
    
    Returns:
        dict: Résultats du test
    """
    print(f"  Test de {instance_name} avec {algorithme}" + 
          (f" ({heuristique})" if heuristique else ""))
    
    # Construire la commande
    cmd = ["python", "-m", "src.taquin_complet", 
          "-i", instance_name, 
          "-a", algorithme, 
          "-t", str(limite_temps)]
    
    # Ajouter l'heuristique si nécessaire
    if heuristique:
        cmd.extend(["-u", heuristique])
    
    # Exécuter la commande
    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout
    
    # Analyser la sortie
    succes = "Solution trouvée!" in output
    
    if succes:
        # Extraire les informations
        import re
        noeuds_match = re.search(r"Solution trouvée! Noeuds explorés: (\d+)", output)
        noeuds = int(noeuds_match.group(1)) if noeuds_match else None
        
        etapes_match = re.search(r"Solution trouvée en (\d+) étapes", output)
        etapes = int(etapes_match.group(1)) if etapes_match else None
        
        temps_match = re.search(r"Solution trouvée en ([\d\.]+) secondes", output)
        temps = float(temps_match.group(1)) if temps_match else time.time() - start_time
    else:
        noeuds = None
        etapes = None
        temps = time.time() - start_time
    
    return {
        "instance": instance_name,
        "algorithme": algorithme,
        "heuristique": heuristique,
        "succes": succes,
        "noeuds": noeuds,
        "etapes": etapes,
        "temps": temps
    }

def executer_tests():
    """
    Exécute des tests comparatifs et retourne les résultats.
    
    Returns:
        dict: Résultats des tests par instance
    """
    # Sélectionner quelques instances représentatives
    instances_test = ["taquin_2x4b", "taquin_3x3b", "taquin_4x4", "taquin_5x5f"]
    
    # Algorithmes à tester
    algorithmes = ["dfs", "bfs", "best-first", "a-star"]
    
    # Heuristiques à tester
    heuristiques = ["lineaire", "combinee"]
    
    resultats = {}
    
    for instance in instances_test:
        print(f"\nAnalyse de l'instance: {instance}")
        resultats[instance] = []
        
        # Tester DFS et BFS (sans heuristique)
        for algo in ["dfs", "bfs"]:
            res = tester_algorithme(instance, algo)
            resultats[instance].append(res)
        
        # Tester Best-First et A* avec les différentes heuristiques
        for algo in ["best-first", "a-star"]:
            for h in heuristiques:
                res = tester_algorithme(instance, algo, h)
                resultats[instance].append(res)
    
    return resultats

def generer_graphiques(resultats):
    """
    Génère des graphiques à partir des résultats.
    
    Args:
        resultats: Dictionnaire des résultats par instance
    """
    # Créer le répertoire pour les graphiques
    os.makedirs("graphiques", exist_ok=True)
    
    # Pour chaque instance
    for instance, results_list in resultats.items():
        # Filtrer les résultats avec succès
        succes_results = [r for r in results_list if r["succes"]]
        
        if not succes_results:
            print(f"Aucun résultat avec succès pour {instance}")
            continue
        
        # Préparer les catégories et les données
        categories = []
        temps_exec = []
        nb_noeuds = []
        nb_etapes = []
        
        for res in succes_results:
            if res["heuristique"]:
                cat = f"{res['algorithme']}\n({res['heuristique']})"
            else:
                cat = res["algorithme"]
            categories.append(cat)
            temps_exec.append(res["temps"])
            nb_noeuds.append(res["noeuds"])
            nb_etapes.append(res["etapes"])
        
        # 1. Graphique des temps d'exécution
        plt.figure(figsize=(12, 6))
        bars = plt.barh(categories, temps_exec, color='skyblue')
        plt.xlabel('Temps d\'exécution (s)')
        plt.title(f'Temps d\'exécution par algorithme - {instance}')
        
        # Ajouter les valeurs sur les barres
        for bar, value in zip(bars, temps_exec):
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                    f'{value:.2f}s', va='center')
        
        plt.tight_layout()
        plt.savefig(f"graphiques/{instance}_temps.png")
        plt.close()
        
        # 2. Graphique du nombre de nœuds explorés
        plt.figure(figsize=(12, 6))
        bars = plt.barh(categories, nb_noeuds, color='lightgreen')
        plt.xlabel('Nombre de nœuds explorés')
        plt.title(f'Nœuds explorés par algorithme - {instance}')
        
        # Ajouter les valeurs sur les barres
        for bar, value in zip(bars, nb_noeuds):
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                    f'{value}', va='center')
        
        plt.tight_layout()
        plt.savefig(f"graphiques/{instance}_noeuds.png")
        plt.close()
        
        # 3. Graphique du nombre d'étapes
        plt.figure(figsize=(12, 6))
        bars = plt.barh(categories, nb_etapes, color='coral')
        plt.xlabel('Nombre d\'étapes')
        plt.title(f'Longueur de la solution par algorithme - {instance}')
        
        # Ajouter les valeurs sur les barres
        for bar, value in zip(bars, nb_etapes):
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                    f'{value}', va='center')
        
        plt.tight_layout()
        plt.savefig(f"graphiques/{instance}_etapes.png")
        plt.close()
        
        # 4. Graphique d'efficacité (noeuds / étape)
        efficacite = [n/e for n, e in zip(nb_noeuds, nb_etapes)]
        
        plt.figure(figsize=(12, 6))
        bars = plt.barh(categories, efficacite, color='purple')
        plt.xlabel('Nœuds explorés par étape')
        plt.title(f'Efficacité par algorithme - {instance}')
        
        # Ajouter les valeurs sur les barres
        for bar, value in zip(bars, efficacite):
            plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                    f'{value:.1f}', va='center')
        
        plt.tight_layout()
        plt.savefig(f"graphiques/{instance}_efficacite.png")
        plt.close()

def afficher_tableau_comparatif(resultats):
    """
    Affiche un tableau comparatif des résultats.
    
    Args:
        resultats: Dictionnaire des résultats par instance
    """
    for instance, results_list in resultats.items():
        # Préparer les données pour le tableau
        tableau_data = []
        
        for res in results_list:
            algo = res["algorithme"]
            if res["heuristique"]:
                algo += f" ({res['heuristique']})"
                
            row = [
                algo,
                "Oui" if res["succes"] else "Non",
                res["etapes"] if res["succes"] else "-",
                f"{res['noeuds']}" if res["succes"] and res["noeuds"] else "-",
                f"{res['temps']:.4f}"
            ]
            tableau_data.append(row)
        
        # Afficher le tableau
        print(f"\nInstance: {instance}")
        headers = ["Algorithme", "Succès", "Étapes", "Nœuds", "Temps (s)"]
        print(tabulate(tableau_data, headers=headers, tablefmt="grid"))

def main():
    """
    Fonction principale.
    """
    print("Exécution des tests comparatifs...")
    resultats = executer_tests()
    
    print("\nGénération des graphiques...")
    generer_graphiques(resultats)
    
    print("\nAffichage des tableaux comparatifs:")
    afficher_tableau_comparatif(resultats)
    
    print("\nAnalyse terminée. Les graphiques ont été enregistrés dans le dossier 'graphiques/'")

if __name__ == "__main__":
    main() 