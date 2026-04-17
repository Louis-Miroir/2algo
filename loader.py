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
    words = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if not word:
                continue
            words.append(word.upper())

    return words


def extract_variables(grid):
    """Extraire les variables (i, j, h, l) horizontales et verticales de la grille."""
    variables = []

    if not grid:
        return variables

    n_rows = len(grid)
    n_cols = len(grid[0])

    for i, row in enumerate(grid):
        start_j = None
        length = 0

        for j, cell in enumerate(row):
            if cell == 0:
                if start_j is None:
                    start_j = j
                length += 1
            else:
                if length >= 2:
                    variables.append((i, start_j, True, length))
                start_j = None
                length = 0

        if length >= 2:
            variables.append((i, start_j, True, length))

    for j in range(n_cols):
        start_i = None
        length = 0

        for i in range(n_rows):
            cell = grid[i][j]
            if cell == 0:
                if start_i is None:
                    start_i = i
                length += 1
            else:
                if length >= 2:
                    variables.append((start_i, j, False, length))
                start_i = None
                length = 0

        if length >= 2:
            variables.append((start_i, j, False, length))

    return variables
