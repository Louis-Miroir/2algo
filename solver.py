"""Algorithmes CSP: Backtracking, Forward Checking, et MRV."""

from loader import Variable


def is_consistent(var, word, assignment, intersections):
    """Verifier si l'affectation var=word respecte les contraintes d'intersection."""
    if len(word) != var[3]:
        return False

    for v1, v2, idx1, idx2 in intersections:
        if v1 == var and v2 in assignment:
            other_word = assignment[v2]
            if idx1 >= len(word) or idx2 >= len(other_word):
                return False
            if word[idx1] != other_word[idx2]:
                return False

        elif v2 == var and v1 in assignment:
            other_word = assignment[v1]
            if idx2 >= len(word) or idx1 >= len(other_word):
                return False
            if word[idx2] != other_word[idx1]:
                return False

    return True


def solve(assignment, variables, words, intersections):
    """Resoudre le CSP par backtracking recursif et retourner une affectation ou None."""
    if len(assignment) == len(variables):
        return assignment

    current_var = None
    for var in variables:
        if var not in assignment:
            current_var = var
            break

    if current_var is None:
        return assignment

    used_words = set(assignment.values())

    for candidate_word in words:
        if candidate_word in used_words:
            continue

        if is_consistent(current_var, candidate_word, assignment, intersections):
            assignment[current_var] = candidate_word

            result = solve(assignment, variables, words, intersections)
            if result is not None:
                return result

            # Retour en arriere: on annule l'affectation pour essayer un autre mot.
            del assignment[current_var]

    return None


def backtracking(variables, domains, intersections, assignment):
    """Resoudre le CSP par Backtracking simple (BT)."""
    # Compatibilite avec l'API du projet: si domains est un dict var->liste,
    # on utilise l'union des mots comme dictionnaire global de candidats.
    if isinstance(domains, dict):
        words = []
        seen = set()
        for values in domains.values():
            for w in values:
                if w not in seen:
                    seen.add(w)
                    words.append(w)
    else:
        words = list(domains)

    return solve(assignment, variables, words, intersections)


def forward_checking(variables, domains, intersections, assignment):
    """Resoudre le CSP par Forward Checking (FC) avec restauration manuelle des domaines."""
    # PSEUDO-CODE:
    # 1. Si toutes les variables sont assignees, retourner assignment.
    # 2. Choisir une variable non assignee.
    # 3. Pour chaque mot du domaine de cette variable:
    # 4. Si coherent avec assignment, affecter var=mot.
    # 5. Propager: pour chaque voisin non assigne, filtrer son domaine
    #    en supprimant les mots incompatibles avec var=mot.
    # 6. Memoriser exactement les suppressions effectuees pour pouvoir restaurer.
    # 7. Si un domaine voisin devient vide, echec local -> restaurer puis essayer mot suivant.
    # 8. Sinon, appel recursif forward_checking(...).
    # 9. Si succes recursif, propager la solution.
    # 10. Sinon, restaurer toutes les suppressions et desaffecter var.
    # 11. Si aucun mot ne marche, retourner echec (None).
    pass


def select_unassigned_variable_mrv(variables, domains, assignment):
    """Choisir la variable non assignee avec le plus petit domaine (heuristique MRV)."""
    # PSEUDO-CODE:
    # 1. Construire la liste des variables non assignees.
    # 2. Calculer la taille de domaine de chacune.
    # 3. Retourner celle de taille minimale.
    # 4. En cas d'egalite, appliquer une regle deterministe (ex: ordre d'origine).
    pass


def forward_checking_mrv(variables, domains, intersections, assignment):
    """Resoudre le CSP par FC en utilisant MRV pour le choix de variable."""
    # PSEUDO-CODE:
    # 1. Meme schema que forward_checking.
    # 2. Difference principale: selectionner la prochaine variable via MRV.
    # 3. Faire la meme propagation, detection d'echec, restauration, et retour arriere.
    # 4. Retourner la solution complete ou None.
    pass
