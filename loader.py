"""Chargement des donnees de grille et extraction des variables."""


Grid = list[list[int]]
Variable = tuple[int, int, bool, int]


def load_grid(path):
    """Lire un fichier TXT de grille et retourner une matrice (liste de listes) de 0/1."""
    grid = []
    # On ouvre le fichier en lecture avec encodage explicite.
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # Supprime espaces et retour a la ligne en bordure.
            clean_line = line.strip()

            # Ignore les lignes vides eventuelles.
            if not clean_line:
                continue

            # Convertit '_' en 0 (blanc) et tout le reste en 1 (noir).
            row = []
            for char in clean_line:
                if char == "_":
                    row.append(0)
                else:
                    row.append(1)

            grid.append(row)

    return grid


def load_words(path):
    """Lire un fichier TXT de dictionnaire et retourner une liste de mots."""
    pass


def extract_variables(grid):
    """Extraire les variables (i, j, h, l) horizontales et verticales de la grille."""
    pass
