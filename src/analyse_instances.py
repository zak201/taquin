#!/usr/bin/env python3
"""
Script d'analyse des différentes instances de taquin
"""
import os
import sys
import time
import json
from collections import defaultdict

# Ajouter le répertoire parent au chemin de recherche des modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Remplacer les importations des anciens fichiers séparés par le fichier unique
from src.taquin_complet import Taquin, resolution_dfs, resolution_bfs, INSTANCES


def creer_fichier_temporaire(nom_instance, contenu):
    """
    Crée un fichier temporaire pour l'instance de taquin.
    
    Args:
        nom_instance: Nom de l'instance
        contenu: Contenu du fichier
        
    Returns:
        str: Chemin vers le fichier temporaire
    """
    chemin = f"temp_{nom_instance}.txt"
    with open(chemin, 'w') as f:
        f.write(contenu)
    return chemin


def supprimer_fichier_temporaire(chemin):
    """
    Supprime un fichier temporaire.
    
    Args:
        chemin: Chemin vers le fichier à supprimer
    """
    if os.path.exists(chemin):
        os.remove(chemin)


def analyser_instance(nom_instance, contenu_instance, algorithmes=None, limite_temps=60):
    """
    Analyse une instance de taquin avec différents algorithmes.
    
    Args:
        nom_instance: Nom de l'instance
        contenu_instance: Contenu de l'instance
        algorithmes: Liste des algorithmes à utiliser (par défaut: DFS et BFS)
        limite_temps: Limite de temps en secondes
        
    Returns:
        dict: Résultats de l'analyse
    """
    if algorithmes is None:
        algorithmes = ["dfs", "bfs"]
    
    resultats = {}
    
    # Créer le fichier temporaire
    chemin_fichier = creer_fichier_temporaire(nom_instance, contenu_instance)
    
    try:
        # Créer l'instance de taquin en utilisant la nouvelle classe unifiée
        taquin = Taquin()
        if not taquin.charger_depuis_fichier(chemin_fichier):
            print(f"Erreur lors du chargement de l'instance {nom_instance}")
            return {"erreur": "Échec du chargement"}
        
        # Analyser avec chaque algorithme
        for algo in algorithmes:
            print(f"Analyse de {nom_instance} avec {algo}...")
            debut = time.time()
            
            if algo == "dfs":
                # Pour DFS, limiter la profondeur pour éviter une exploration trop longue
                limite_profondeur = 100 if "4x4" in nom_instance or "5x5" in nom_instance else 50
                chemin = resolution_dfs(taquin, limite_profondeur=limite_profondeur, limite_temps=limite_temps)
            else:  # bfs
                # Pour BFS, limiter le nombre de nœuds
                limite_noeuds = 1000000 if "4x4" in nom_instance or "5x5" in nom_instance else 100000
                chemin = resolution_bfs(taquin, limite_noeuds=limite_noeuds, limite_temps=limite_temps)
            
            temps_total = time.time() - debut
            
            # Enregistrer les résultats
            resultats[algo] = {
                "succes": chemin is not None,
                "temps": temps_total,
                "longueur_solution": len(chemin) if chemin else None
            }
    
    except Exception as e:
        print(f"Erreur lors de l'analyse de {nom_instance}: {e}")
        resultats["erreur"] = str(e)
    
    finally:
        # Supprimer le fichier temporaire
        supprimer_fichier_temporaire(chemin_fichier)
    
    return resultats


def analyser_toutes_instances(limite_instances=None, limite_temps=60):
    """
    Analyse toutes les instances disponibles.
    
    Args:
        limite_instances: Nombre maximal d'instances à analyser (None = toutes)
        limite_temps: Limite de temps par instance en secondes
        
    Returns:
        dict: Résultats complets de l'analyse
    """
    resultats = {}
    
    # Obtenir la liste des instances depuis le nouveau fichier taquin_complet
    instances = list(INSTANCES.items())
    if limite_instances:
        instances = instances[:limite_instances]
    
    # Analyser chaque instance
    for nom, contenu in instances:
        print(f"\nAnalyse de l'instance {nom}...")
        resultats[nom] = analyser_instance(nom, contenu, limite_temps=limite_temps)
    
    return resultats


def enregistrer_resultats(resultats, chemin_fichier="resultats_analyse_alpha.json"):
    """
    Enregistre les résultats d'analyse dans un fichier JSON.
    
    Args:
        resultats: Résultats à enregistrer
        chemin_fichier: Chemin du fichier de sortie
    """
    with open(chemin_fichier, 'w') as f:
        json.dump(resultats, f, indent=2)
    print(f"Résultats enregistrés dans {chemin_fichier}")


def analyser_resultats(resultats):
    """
    Fournit une analyse des résultats.
    
    Args:
        resultats: Résultats d'analyse
        
    Returns:
        dict: Analyse des résultats
    """
    analyse = {
        "statistiques_globales": {
            "instances_total": len(resultats),
            "succes_par_algo": defaultdict(int),
            "temps_moyen_par_algo": defaultdict(float),
            "longueur_moyenne_par_algo": defaultdict(float),
        },
        "instances_par_taille": defaultdict(list)
    }
    
    # Regrouper les instances par taille
    for nom in resultats:
        if "erreur" in resultats[nom]:
            continue
            
        if "2x4" in nom:
            analyse["instances_par_taille"]["2x4"].append(nom)
        elif "3x3" in nom:
            analyse["instances_par_taille"]["3x3"].append(nom)
        elif "3x4" in nom:
            analyse["instances_par_taille"]["3x4"].append(nom)
        elif "4x4" in nom:
            analyse["instances_par_taille"]["4x4"].append(nom)
        elif "5x5" in nom:
            analyse["instances_par_taille"]["5x5"].append(nom)
    
    # Calculer les statistiques globales
    for nom, res_instance in resultats.items():
        if "erreur" in res_instance:
            continue
            
        for algo, res_algo in res_instance.items():
            if res_algo["succes"]:
                analyse["statistiques_globales"]["succes_par_algo"][algo] += 1
                analyse["statistiques_globales"]["temps_moyen_par_algo"][algo] += res_algo["temps"]
                if res_algo["longueur_solution"]:
                    analyse["statistiques_globales"]["longueur_moyenne_par_algo"][algo] += res_algo["longueur_solution"]
    
    # Calculer les moyennes
    for algo in analyse["statistiques_globales"]["temps_moyen_par_algo"]:
        nb_succes = analyse["statistiques_globales"]["succes_par_algo"][algo]
        if nb_succes > 0:
            analyse["statistiques_globales"]["temps_moyen_par_algo"][algo] /= nb_succes
            analyse["statistiques_globales"]["longueur_moyenne_par_algo"][algo] /= nb_succes
    
    return analyse


def main():
    """
    Fonction principale.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyse des instances de taquin")
    parser.add_argument("--limite", "-l", type=int, help="Nombre maximal d'instances à analyser")
    parser.add_argument("--temps", "-t", type=int, default=60, help="Limite de temps par instance en secondes")
    parser.add_argument("--instance", "-i", help="Nom d'une instance spécifique à analyser")
    
    args = parser.parse_args()
    
    if args.instance:
        if args.instance in INSTANCES:
            resultats = {args.instance: analyser_instance(args.instance, INSTANCES[args.instance], limite_temps=args.temps)}
        else:
            print(f"Erreur: L'instance {args.instance} n'existe pas.")
            print(f"Instances disponibles: {', '.join(INSTANCES.keys())}")
            return 1
    else:
        resultats = analyser_toutes_instances(limite_instances=args.limite, limite_temps=args.temps)
    
    # Enregistrer les résultats
    enregistrer_resultats(resultats)
    
    # Analyser les résultats
    analyse = analyser_resultats(resultats)
    
    # Afficher un résumé
    print("\nRésumé de l'analyse:")
    print(f"Nombre total d'instances analysées: {analyse['statistiques_globales']['instances_total']}")
    
    print("\nTaux de réussite par algorithme:")
    for algo, nb_succes in analyse["statistiques_globales"]["succes_par_algo"].items():
        print(f"  - {algo}: {nb_succes}/{analyse['statistiques_globales']['instances_total']} instances")
    
    print("\nTemps moyen d'exécution pour les résolutions réussies:")
    for algo, temps_moyen in analyse["statistiques_globales"]["temps_moyen_par_algo"].items():
        print(f"  - {algo}: {temps_moyen:.4f} secondes")
    
    print("\nLongueur moyenne des solutions trouvées:")
    for algo, longueur_moyenne in analyse["statistiques_globales"]["longueur_moyenne_par_algo"].items():
        print(f"  - {algo}: {longueur_moyenne:.1f} étapes")
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 