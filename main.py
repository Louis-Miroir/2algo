"""Point d'entree: chargement, preparation, execution des solveurs, et mesures."""

import time
from loader import extract_variables, load_grid, load_words
from solver import backtracking, forward_checking, forward_checking_mrv
from utils import compute_intersections, display_assignment, get_domains


def run_experiment(grid_path, dict_path, label):
    """Executer les 3 algorithmes sur un couple (grille, dictionnaire)."""
    print(f"\n{'='*20} EXPERIENCES : {label} {'='*20}")
    
    try:
        grid = load_grid(grid_path)
        words = load_words(dict_path)
    except FileNotFoundError:
        print(f"Erreur : Fichier non trouve ({grid_path} ou {dict_path})")
        return

    variables = extract_variables(grid)
    intersections = compute_intersections(variables)
    domains = get_domains(variables, words)
    
    print(f"Grille: {len(grid)}x{len(grid[0])}")
    print(f"Variables: {len(variables)}")
    print(f"Intersections: {len(intersections)}")
    print(f"Mots dans le dictionnaire: {len(words)}")

    algorithms = [
        ("Backtracking", backtracking),
        ("Forward Checking", forward_checking),
        ("FC + MRV", forward_checking_mrv)
    ]

    for name, func in algorithms:
        if label == "MP2" and name == "Backtracking":
            print(f"\n--- Algorithme : {name} ---")
            print("(!) Backtracking ignore pour MP2 car trop inefficace (complexité exponentielle).")
            continue

        print(f"\n--- Algorithme : {name} ---")
        assignment = {}
        solution, stats = func(variables, domains, intersections, assignment)
        
        if solution:
            print(f"Solution trouvée !")
            print(f"Temps d'exécution : {stats.get_duration():.4f} secondes")
            print(f"Nombre de nœuds visités : {stats.nodes_visited}")
            # Affichage de la grille pour MP1 (plus lisible)
            if label == "MP1":
                display_assignment(grid, variables, solution)
        else:
            if stats.nodes_visited >= 500000 and name == "Backtracking":
                print(f"ECHEC : Limite de {stats.nodes_visited} noeuds atteinte (Trop lent).")
            else:
                print(f"Aucune solution trouvée en {stats.nodes_visited} noeuds.")
            print(f"Temps d'exécution : {stats.get_duration():.4f} secondes")


def main():
    """Lancer les tests pour MP1 et MP2."""
    run_experiment("gridMP1.txt", "dictMP1.txt", "MP1")
    run_experiment("gridMP2.txt", "dictMP2.txt", "MP2")


if __name__ == "__main__":
    main()