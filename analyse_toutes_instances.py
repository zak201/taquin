#!/usr/bin/env python3
"""
Script pour exécuter l'analyse sur toutes les instances de taquin disponibles.
"""
import subprocess
import time
import re
from tabulate import tabulate

# Récupérer la liste des instances depuis le module taquin_complet
from src.taquin_complet import INSTANCES

def analyser_instance(instance_name):
    """
    Analyse une instance avec l'algorithme A* et l'heuristique combinée.
    
    Args:
        instance_name: Nom de l'instance à analyser
        
    Returns:
        dict: Résultat de l'analyse
    """
    print(f"\nAnalyse de l'instance: {instance_name}")
    
    # Exécuter la commande avec un timeout
    start_time = time.time()
    command = ["python", "-m", "src.taquin_complet", "-i", instance_name, "-a", "a-star", "-u", "combinee", "-t", "30"]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        output = result.stdout
        
        # Extraire les informations pertinentes
        if "Solution trouvée!" in output:
            # Extraire le nombre de nœuds explorés
            nodes_match = re.search(r"Solution trouvée! Noeuds explorés: (\d+)", output)
            nodes = int(nodes_match.group(1)) if nodes_match else None
            
            # Extraire le nombre d'étapes
            steps_match = re.search(r"Solution trouvée en (\d+) étapes", output)
            steps = int(steps_match.group(1)) if steps_match else None
            
            # Extraire le temps d'exécution
            time_match = re.search(r"Solution trouvée en ([\d\.]+) secondes", output)
            exec_time = float(time_match.group(1)) if time_match else time.time() - start_time
            
            return {
                "instance": instance_name,
                "succes": True,
                "noeuds": nodes,
                "etapes": steps,
                "temps": exec_time
            }
        else:
            return {
                "instance": instance_name,
                "succes": False,
                "noeuds": None,
                "etapes": None,
                "temps": time.time() - start_time
            }
    except subprocess.TimeoutExpired:
        return {
            "instance": instance_name,
            "succes": False,
            "noeuds": None,
            "etapes": None,
            "temps": 60.0  # Timeout
        }

def main():
    """
    Fonction principale.
    """
    print("Analyse de toutes les instances disponibles...")
    print(f"Nombre total d'instances: {len(INSTANCES)}")
    
    # Analyser toutes les instances
    resultats = []
    
    for instance_name in INSTANCES.keys():
        res = analyser_instance(instance_name)
        resultats.append(res)
    
    # Classer les résultats par taille d'instance
    instances_par_taille = {
        "2x4": [],
        "3x3": [],
        "3x4": [],
        "4x4": [],
        "5x5": []
    }
    
    for res in resultats:
        for taille in instances_par_taille.keys():
            if taille in res["instance"]:
                instances_par_taille[taille].append(res)
                break
    
    # Afficher les résultats par taille
    for taille, res_list in instances_par_taille.items():
        if res_list:
            print(f"\n=== Instances {taille} ===")
            
            # Préparer les données pour le tableau
            table_data = []
            for res in res_list:
                table_data.append([
                    res["instance"],
                    "Oui" if res["succes"] else "Non",
                    res["etapes"] if res["succes"] else "-",
                    f"{res['noeuds']}" if res["succes"] and res["noeuds"] else "-",
                    f"{res['temps']:.4f}" if res["temps"] else "-"
                ])
            
            # Afficher le tableau
            headers = ["Instance", "Succès", "Étapes", "Nœuds", "Temps (s)"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Statistiques globales
    success_count = sum(1 for res in resultats if res["succes"])
    total_instances = len(resultats)
    
    print(f"\nRésumé global:")
    print(f"- Instances résolues: {success_count}/{total_instances} ({success_count/total_instances*100:.1f}%)")
    
    if success_count > 0:
        avg_steps = sum(res["etapes"] for res in resultats if res["succes"]) / success_count
        avg_time = sum(res["temps"] for res in resultats if res["succes"]) / success_count
        print(f"- Nombre moyen d'étapes: {avg_steps:.1f}")
        print(f"- Temps moyen d'exécution: {avg_time:.4f} secondes")

if __name__ == "__main__":
    main() 