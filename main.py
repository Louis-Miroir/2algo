"""Point d'entree: chargement, preparation, execution des solveurs, et mesures."""

from loader import extract_variables, load_grid, load_words
from solver import backtracking, forward_checking, forward_checking_mrv
from utils import compute_intersections, display_assignment


def run_backtracking(grid_path, words_path):
    """Charger les donnees puis executer la resolution Backtracking."""
    pass


def run_forward_checking(grid_path, words_path):
    """Charger les donnees puis executer la resolution Forward Checking."""
    pass


def run_forward_checking_mrv(grid_path, words_path):
    """Charger les donnees puis executer la resolution FC + MRV."""
    pass


def main():
    """Orchestrer les essais, afficher les resultats, et comparer les performances."""
    pass


if __name__ == "__main__":
    main()


# test de lecture de la grille et affichage de la matrice 2D !!!!!!!!!
from loader import load_grid


ma_grille = load_grid("gridMP1.txt")

# Affiche la première ligne pour voir
print("Première ligne de la matrice :", ma_grille[0])
# Affiche toute la grille
for ligne in ma_grille:
    print(ligne)

from loader import load_words

# Test du dictionnaire
mots = load_words("dictMP1.txt")  
print(f"Nombre de mots chargés : {len(mots)}")
print(f"Les 5 premiers mots : {mots[:5]}")

from loader import load_grid, extract_variables

# 1. On charge la grille
grid = load_grid("gridMP1.txt")

# 2. On extrait les variables (les quadruplets)
variables = extract_variables(grid)

# 3. On affiche le résultat proprement
print(f"--- Nombre de variables trouvées : {len(variables)} ---")
for v in variables:
    i, j, h, l = v
    direction = "Horizontal" if h else "Vertical"
    print(f"Position ({i}, {j}) | Direction: {direction} | Longueur: {l}")