"""Algorithmes CSP: Backtracking, Forward Checking, et MRV."""

from loader import Variable
import time

class CSPStats:
    def __init__(self):
        self.nodes_visited = 0
        self.start_time = 0
        self.end_time = 0

    def start_timer(self):
        self.start_time = time.time()
        self.nodes_visited = 0

    def stop_timer(self):
        self.end_time = time.time()

    def get_duration(self):
        return self.end_time - self.start_time


def get_intersections_by_var(variables, intersections):
    """Organiser les intersections par variable pour un acces plus rapide."""
    adj = {v: [] for v in variables}
    for v1, v2, idx1, idx2 in intersections:
        adj[v1].append((v2, idx1, idx2))
        adj[v2].append((v1, idx2, idx1))
    return adj


def is_consistent_optimized(var, word, assignment, adj):
    """Verifier si l'affectation var=word respecte les contraintes d'intersection."""
    for neighbor, my_idx, neighbor_idx in adj[var]:
        if neighbor in assignment:
            if word[my_idx] != assignment[neighbor][neighbor_idx]:
                return False
    return True


# --- BACKTRACKING SIMPLE ---

def solve_backtracking(assignment, variables, domains_lists, adj, stats):
    stats.nodes_visited += 1
    
    # Limitation pour eviter de bloquer sur MP2 (BT est tres inefficace sur de gros index)
    if stats.nodes_visited > 500000:
        return None

    if len(assignment) == len(variables):
        return assignment

    var = None
    for v in variables:
        if v not in assignment:
            var = v
            break
            
    used_words = set(assignment.values())
    
    for word in domains_lists[var]:
        if word not in used_words and is_consistent_optimized(var, word, assignment, adj):
            assignment[var] = word
            result = solve_backtracking(assignment, variables, domains_lists, adj, stats)
            if result is not None:
                return result
            del assignment[var]
            
    return None


def backtracking(variables, domains, intersections, assignment):
    stats = CSPStats()
    stats.start_timer()
    adj = get_intersections_by_var(variables, intersections)
    # BT utilise les listes de domaines filtrées par longueur
    res = solve_backtracking(assignment, variables, domains, adj, stats)
    stats.stop_timer()
    return res, stats


# --- FORWARD CHECKING ---

def solve_forward_checking(assignment, variables, domains_sets, adj, stats, use_mrv=False):
    stats.nodes_visited += 1
    
    if len(assignment) == len(variables):
        return assignment

    if use_mrv:
        var = select_unassigned_variable_mrv(variables, domains_sets, assignment)
    else:
        var = None
        for v in variables:
            if v not in assignment:
                var = v
                break

    used_words = set(assignment.values())
    
    # On itere sur une copie du domaine car on va le modifier (via forward checking)
    # On trie ou on prend l'ordre par défaut.
    words_to_try = list(domains_sets[var])
    
    for word in words_to_try:
        if word in used_words:
            continue
            
        if is_consistent_optimized(var, word, assignment, adj):
            assignment[var] = word
            removals = []
            
            # Propagation: chaque mot est unique
            for other_var in variables:
                if other_var not in assignment:
                    if word in domains_sets[other_var]:
                        domains_sets[other_var].remove(word)
                        removals.append((other_var, word))
            
            # Propagation: intersections
            valid_propagation = True
            for neighbor, my_idx, neighbor_idx in adj[var]:
                if neighbor not in assignment:
                    # Trouver les mots incompatibles
                    to_remove = [w for w in domains_sets[neighbor] if word[my_idx] != w[neighbor_idx]]
                    
                    if to_remove:
                        for w in to_remove:
                            domains_sets[neighbor].remove(w)
                            removals.append((neighbor, w))
                    
                    if not domains_sets[neighbor]:
                        valid_propagation = False
                        break
            
            if valid_propagation:
                result = solve_forward_checking(assignment, variables, domains_sets, adj, stats, use_mrv)
                if result is not None:
                    return result
            
            # Restauration (Backtrack)
            for r_var, r_word in reversed(removals):
                domains_sets[r_var].add(r_word)
            del assignment[var]
            
    return None


def forward_checking(variables, domains, intersections, assignment):
    stats = CSPStats()
    stats.start_timer()
    adj = get_intersections_by_var(variables, intersections)
    # On convertit en sets pour des suppressions en O(1)
    domains_sets = {v: set(d) for v, d in domains.items()}
    res = solve_forward_checking(assignment, variables, domains_sets, adj, stats, use_mrv=False)
    stats.stop_timer()
    return res, stats


# --- MRV ---

def select_unassigned_variable_mrv(variables, domains_sets, assignment):
    best_var = None
    min_size = float('inf')
    
    for v in variables:
        if v not in assignment:
            size = len(domains_sets[v])
            if size < min_size:
                min_size = size
                best_var = v
    return best_var


def forward_checking_mrv(variables, domains, intersections, assignment):
    stats = CSPStats()
    stats.start_timer()
    adj = get_intersections_by_var(variables, intersections)
    domains_sets = {v: set(d) for v, d in domains.items()}
    res = solve_forward_checking(assignment, variables, domains_sets, adj, stats, use_mrv=True)
    stats.stop_timer()
    return res, stats
