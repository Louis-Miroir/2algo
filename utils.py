"""Utilitaires pour les intersections, domaines, affichage, et aides de debug."""

from loader import Grid, Variable, load_grid, load_words, extract_variables


def compute_intersections(variables):
    """Pre-calculer les intersections entre variables qui partagent une case."""
    intersections = []

    horizontales = [v for v in variables if v[2] is True]
    verticales = [v for v in variables if v[2] is False]

    for v_h in horizontales:
        i_h, j_h, _, l_h = v_h

        for v_v in verticales:
            i_v, j_v, _, l_v = v_v

            # Une horizontale (ligne i_h) croise une verticale (colonne j_v)
            # si la colonne de la verticale est dans le segment horizontal,
            # et la ligne de l'horizontale dans le segment vertical.
            if j_h <= j_v < j_h + l_h and i_v <= i_h < i_v + l_v:
                idx_h = j_v - j_h
                idx_v = i_h - i_v
                intersections.append((v_h, v_v, idx_h, idx_v))

    return intersections


def get_domains(variables, words):
    """Calculer le domaine initial pour chaque variable (mots de la bonne longueur)."""
    domains = {}
    
    # Pre-filtrage par longueur pour accelerer
    length_map = {}
    for w in words:
        l = len(w)
        if l not in length_map:
            length_map[l] = []
        length_map[l].append(w)
        
    for var in variables:
        _, _, _, l = var
        domains[var] = length_map.get(l, [])
        
    return domains


def build_empty_solution_grid(grid):
    """Construire une grille de sortie editable a partir de la grille 0/1."""
    solution = []

    for row in grid:
        solution_row = []
        for cell in row:
            if cell == 0:
                solution_row.append(" ")
            else:
                solution_row.append("#")
        solution.append(solution_row)

    return solution


def display_grid(grid):
    """Afficher la grille de facon lisible en console."""
    for row in grid:
        print("".join("." if cell == 0 else "#" for cell in row))


def display_assignment(grid, variables, assignment):
    """Afficher une solution partielle ou complete sur la grille."""
    visual_grid = build_empty_solution_grid(grid)

    for var, word in assignment.items():
        i, j, h, l = var

        if h:
            for k in range(min(l, len(word))):
                visual_grid[i][j + k] = word[k]
        else:
            for k in range(min(l, len(word))):
                visual_grid[i + k][j] = word[k]

    for row in visual_grid:
        print("".join(row))


