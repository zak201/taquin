#!/usr/bin/env python3
"""
Script pour exécuter l'analyse sur toutes les instances de taquin disponibles.

Ce script permet d'analyser les performances de l'algorithme A* 
avec l'heuristique combinée sur toutes les instances de taquin définies.
Il génère un rapport détaillé des résultats.
"""
import subprocess  # Pour exécuter des commandes externes
import time        # Pour mesurer le temps d'exécution
import re          # Pour les expressions régulières (extraction d'informations)
from tabulate import tabulate  # Pour formater les tableaux de résultats

# Récupérer la liste des instances depuis le module taquin_complet
from src.taquin_complet import INSTANCES

def analyser_instance(instance_name):
    """
    Analyse une instance spécifique avec l'algorithme A* et l'heuristique combinée.
    
    Cette fonction exécute le module taquin_complet.py en mode résolution sur
    l'instance spécifiée, puis analyse la sortie pour extraire les informations
    importantes comme le temps d'exécution, le nombre de nœuds explorés, etc.
    
    Args:
        instance_name: Nom de l'instance à analyser (doit être définie dans INSTANCES)
        
    Returns:
        dict: Dictionnaire contenant les résultats de l'analyse
            {
                "instance": nom de l'instance,
                "succes": True/False selon si une solution a été trouvée,
                "noeuds": nombre de nœuds explorés (si succès),
                "etapes": nombre d'étapes de la solution (si succès),
                "temps": temps d'exécution en secondes
            }
    """
    print(f"\nAnalyse de l'instance: {instance_name}")
    
    # Préparer la commande à exécuter
    # L'algorithme A* avec l'heuristique combinée est utilisé
    # avec une limite de temps de 30 secondes
    start_time = time.time()
    command = ["python", "-m", "src.taquin_complet", 
               "-i", instance_name,   # Instance à résoudre
               "-a", "a-star",        # Algorithme A*
               "-u", "combinee",      # Heuristique combinée
               "-t", "30"]            # Timeout de 30 secondes
    
    try:
        # Exécuter la commande et capturer la sortie
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        output = result.stdout
        
        # Analyser la sortie pour extraire les informations
        if "Solution trouvée!" in output:
            # La solution a été trouvée - extraire les détails

            # Nombre de nœuds explorés
            nodes_match = re.search(r"Solution trouvée! Noeuds explorés: (\d+)", output)
            nodes = int(nodes_match.group(1)) if nodes_match else None
            
            # Nombre d'étapes dans la solution
            steps_match = re.search(r"Solution trouvée en (\d+) étapes", output)
            steps = int(steps_match.group(1)) if steps_match else None
            
            # Temps d'exécution
            time_match = re.search(r"Solution trouvée en ([\d\.]+) secondes", output)
            exec_time = float(time_match.group(1)) if time_match else time.time() - start_time
            
            # Retourner les résultats avec succès
            return {
                "instance": instance_name,
                "succes": True,
                "noeuds": nodes,
                "etapes": steps,
                "temps": exec_time
            }
        else:
            # Aucune solution trouvée dans le temps imparti
            return {
                "instance": instance_name,
                "succes": False,
                "noeuds": None,
                "etapes": None,
                "temps": time.time() - start_time
            }
    except subprocess.TimeoutExpired:
        # La commande a dépassé le timeout (60 secondes)
        return {
            "instance": instance_name,
            "succes": False,
            "noeuds": None,
            "etapes": None,
            "temps": 60.0  # Timeout
        }

def main():
    """
    Fonction principale qui analyse toutes les instances et affiche les résultats.
    
    Le processus est le suivant:
    1. Analyser chaque instance définie dans INSTANCES
    2. Classer les résultats par taille d'instance (2x4, 3x3, etc.)
    3. Afficher des tableaux formatés par catégorie
    4. Calculer et afficher des statistiques globales
    """
    print("Analyse de toutes les instances disponibles avec A* et l'heuristique combinée...")
    print(f"Nombre total d'instances: {len(INSTANCES)}")
    
    # Étape 1: Analyser toutes les instances
    resultats = []
    
    for instance_name in INSTANCES.keys():
        res = analyser_instance(instance_name)
        resultats.append(res)
    
    # Étape 2: Classer les résultats par taille d'instance
    instances_par_taille = {
        "2x4": [],  # Instances de taille 2x4
        "3x3": [],  # Instances de taille 3x3
        "3x4": [],  # Instances de taille 3x4
        "4x4": [],  # Instances de taille 4x4
        "5x5": []   # Instances de taille 5x5
    }
    
    # Parcourir les résultats et les classer par taille
    for res in resultats:
        for taille in instances_par_taille.keys():
            if taille in res["instance"]:
                instances_par_taille[taille].append(res)
                break
    
    # Étape 3: Afficher les résultats par taille
    for taille, res_list in instances_par_taille.items():
        if res_list:  # Si la liste n'est pas vide
            print(f"\n=== Instances {taille} ===")
            
            # Préparer les données pour le tableau
            table_data = []
            for res in res_list:
                table_data.append([
                    res["instance"],  # Nom de l'instance
                    "Oui" if res["succes"] else "Non",  # Succès (Oui/Non)
                    res["etapes"] if res["succes"] else "-",  # Nombre d'étapes
                    f"{res['noeuds']}" if res["succes"] and res["noeuds"] else "-",  # Nœuds explorés
                    f"{res['temps']:.4f}" if res["temps"] else "-"  # Temps d'exécution
                ])
            
            # Afficher le tableau formaté
            headers = ["Instance", "Succès", "Étapes", "Nœuds", "Temps (s)"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Étape 4: Calculer et afficher des statistiques globales
    success_count = sum(1 for res in resultats if res["succes"])  # Nombre d'instances résolues
    total_instances = len(resultats)  # Nombre total d'instances
    
    print(f"\nRésumé global:")
    print(f"- Instances résolues: {success_count}/{total_instances} ({success_count/total_instances*100:.1f}%)")
    
    if success_count > 0:
        # Calculer la moyenne des étapes et du temps pour les instances résolues
        avg_steps = sum(res["etapes"] for res in resultats if res["succes"]) / success_count
        avg_time = sum(res["temps"] for res in resultats if res["succes"]) / success_count
        print(f"- Nombre moyen d'étapes: {avg_steps:.1f}")
        print(f"- Temps moyen d'exécution: {avg_time:.4f} secondes")

# Point d'entrée du script
if __name__ == "__main__":
    main() 