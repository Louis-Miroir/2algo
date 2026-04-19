import time

# --- MODÉLISATION ---
# Une grille : liste de listes de 0 (blanc) et 1 (noir)
# Un dictionnaire : liste de mots
# Une variable : quadruplet (i, j, h, l)
#   i, j : coordonnées de départ
#   h : True si horizontal, False si vertical
#   l : longueur du mot
# Un domaine : liste de mots du dictionnaire de longueur l
# Solution : dictionnaire {variable: mot}

def charger_grille(nom_fichier):
    """Charge la grille depuis un fichier texte."""
    grille = []
    with open(nom_fichier, 'r') as f:
        for ligne in f:
            ligne = ligne.strip()
            if ligne:
                # '_' -> 0, '#' -> 1
                ligne_num = [0 if c == '_' else 1 for c in ligne]
                grille.append(ligne_num)
    return grille

def charger_dictionnaire(nom_fichier):
    """Charge les mots du dictionnaire."""
    mots = []
    with open(nom_fichier, 'r') as f:
        for ligne in f:
            mot = ligne.strip().upper()
            if mot:
                mots.append(mot)
    return mots

def trouver_variables(grille):
    """Extrait les variables (i, j, h, l) de la grille."""
    vars = []
    n_lignes = len(grille)
    n_cols = len(grille[0])

    # Variables horizontales
    for i in range(n_lignes):
        j = 0
        while j < n_cols:
            if grille[i][j] == 0:
                debut = j
                longueur = 0
                while j < n_cols and grille[i][j] == 0:
                    longueur += 1
                    j += 1
                if longueur >= 2:
                    vars.append((i, debut, True, longueur))
            else:
                j += 1

    # Variables verticales
    for j in range(n_cols):
        i = 0
        while i < n_lignes:
            if grille[i][j] == 0:
                debut = i
                longueur = 0
                while i < n_lignes and grille[i][j] == 0:
                    longueur += 1
                    i += 1
                if longueur >= 2:
                    vars.append((debut, j, False, longueur))
            else:
                i += 1
    return vars

def calculer_domaines(variables, dictionnaire):
    """Associe à chaque variable ses mots possibles (bonne longueur)."""
    # Pré-filtrage par longueur pour éviter de scanner tout le dico à chaque fois
    dico_par_longueur = {}
    for mot in dictionnaire:
        l = len(mot)
        if l not in dico_par_longueur:
            dico_par_longueur[l] = []
        dico_par_longueur[l].append(mot)
        
    domaines = {}
    for v in variables:
        l = v[3]
        # On utilise des listes comme demandé, mais on filtre intelligemment
        domaines[v] = list(dico_par_longueur.get(l, []))
    return domaines

def calculer_intersections(variables):
    """Pré-calcul des points de croisement entre variables."""
    inter = {v: [] for v in variables}
    for k, v1 in enumerate(variables):
        for v2 in variables[k+1:]:
            i1, j1, h1, l1 = v1
            i2, j2, h2, l2 = v2
            
            if h1 == h2: continue
            
            v_h, v_v = (v1, v2) if h1 else (v2, v1)
            ih, jh, _, lh = v_h
            iv, jv, _, lv = v_v
            
            if jh <= jv < jh + lh and iv <= ih < iv + lv:
                idx_h = jv - jh
                idx_v = ih - iv
                inter[v1].append((v2, idx_h if h1 else idx_v, idx_v if h1 else idx_h))
                inter[v2].append((v1, idx_v if h1 else idx_h, idx_h if h1 else idx_v))
    return inter

# --- ALGORITHMES DE RÉSOLUTION ---

class Solveur:
    def __init__(self, variables, domaines, intersections):
        self.variables = variables
        self.domaines = domaines
        self.intersections = intersections
        self.noeuds = 0

    def est_cohérent(self, var, mot, assignment):
        """Vérifie si un mot peut être placé sans conflit avec l'existant."""
        for voisin, idx_ma, idx_voisin in self.intersections[var]:
            if voisin in assignment:
                if mot[idx_ma] != assignment[voisin][idx_voisin]:
                    return False
        return True

    # 1. Backtracking Simple
    def backtracking(self, assignment):
        self.noeuds += 1
        if self.noeuds > 100000: return None # Limite pour éviter de bloquer
        
        if len(assignment) == len(self.variables):
            return assignment

        var = next(v for v in self.variables if v not in assignment)
        mots_utilises = set(assignment.values())

        for mot in self.domaines[var]:
            if mot not in mots_utilises and self.est_cohérent(var, mot, assignment):
                assignment[var] = mot
                resultat = self.backtracking(assignment)
                if resultat: return resultat
                del assignment[var]
        return None

    # 2. Forward Checking
    def forward_checking(self, assignment, domaines_actuels):
        self.noeuds += 1
        if len(assignment) == len(self.variables):
            return assignment

        var = next(v for v in self.variables if v not in assignment)
        mots_utilises = set(assignment.values())

        # On fait une copie du domaine pour l'itérer car on va le modifier
        for mot in list(domaines_actuels[var]):
            if mot in mots_utilises: continue
            
            if self.est_cohérent(var, mot, assignment):
                assignment[var] = mot
                supprimes = []
                
                # Propagation : mot unique
                for v in self.variables:
                    if v not in assignment and v[3] == len(mot):
                        if mot in domaines_actuels[v]:
                            domaines_actuels[v].remove(mot)
                            supprimes.append((v, mot))
                
                # Propagation : intersections
                possible = True
                for voisin, idx_ma, idx_voisin in self.intersections[var]:
                    if voisin not in assignment:
                        # Filtrage efficace
                        nouveau_dom = []
                        for mw in domaines_actuels[voisin]:
                            if mot[idx_ma] == mw[idx_voisin]:
                                nouveau_dom.append(mw)
                            else:
                                supprimes.append((voisin, mw))
                        
                        domaines_actuels[voisin] = nouveau_dom
                        if not domaines_actuels[voisin]:
                            possible = False
                            break
                
                if possible:
                    resultat = self.forward_checking(assignment, domaines_actuels)
                    if resultat: return resultat
                
                # Backtrack : on restaure
                for v_suppr, m_suppr in reversed(supprimes):
                    domaines_actuels[v_suppr].append(m_suppr)
                
                del assignment[var]
        return None

    # 3. FC + MRV
    def fc_mrv(self, assignment, domaines_actuels):
        self.noeuds += 1
        if len(assignment) == len(self.variables):
            return assignment

        # MRV
        var = None
        min_dom = float('inf')
        for v in self.variables:
            if v not in assignment:
                if len(domaines_actuels[v]) < min_dom:
                    min_dom = len(domaines_actuels[v])
                    var = v
        
        mots_utilises = set(assignment.values())

        for mot in list(domaines_actuels[var]):
            if mot in mots_utilises: continue
            
            if self.est_cohérent(var, mot, assignment):
                assignment[var] = mot
                supprimes = []
                
                for v in self.variables:
                    if v not in assignment and v[3] == len(mot):
                        if mot in domaines_actuels[v]:
                            domaines_actuels[v].remove(mot)
                            supprimes.append((v, mot))
                
                possible = True
                for voisin, idx_ma, idx_voisin in self.intersections[var]:
                    if voisin not in assignment:
                        nouveau_dom = []
                        for mw in domaines_actuels[voisin]:
                            if mot[idx_ma] == mw[idx_voisin]:
                                nouveau_dom.append(mw)
                            else:
                                supprimes.append((voisin, mw))
                        domaines_actuels[voisin] = nouveau_dom
                        if not domaines_actuels[voisin]:
                            possible = False
                            break
                
                if possible:
                    resultat = self.fc_mrv(assignment, domaines_actuels)
                    if resultat: return resultat
                
                for v_suppr, m_suppr in reversed(supprimes):
                    domaines_actuels[v_suppr].append(m_suppr)
                del assignment[var]
        return None

# --- AFFICHAGE ET TESTS ---

def imprimer_solution(grille, variables, solution):
    if not solution:
        print("Pas de solution.")
        return
    
    n_lig, n_col = len(grille), len(grille[0])
    rendu = [['#' if grille[i][j] == 1 else ' ' for j in range(n_col)] for i in range(n_lig)]
    
    for (i, j, h, l), mot in solution.items():
        for k in range(l):
            if h: rendu[i][j+k] = mot[k]
            else: rendu[i+k][j] = mot[k]
            
    for ligne in rendu:
        print("".join(ligne))

def evaluer(fichier_grille, fichier_dict):
    print(f"\n========================================")
    print(f"TEST : {fichier_grille}")
    print(f"========================================")
    
    grille = charger_grille(fichier_grille)
    dico = charger_dictionnaire(fichier_dict)
    vars = trouver_variables(grille)
    doms = calculer_domaines(vars, dico)
    inter = calculer_intersections(vars)

    methodes = [
        ("Backtracking", lambda s: s.backtracking({})),
        ("Forward Checking", lambda s: s.forward_checking({}, {v: list(d) for v, d in doms.items()})),
        ("FC + MRV", lambda s: s.fc_mrv({}, {v: list(d) for v, d in doms.items()}))
    ]

    for nom, methode in methodes:
        if "MP2" in fichier_grille and nom == "Backtracking":
            print(f"\n[{nom}] : Ignoré (trop complexe pour BT simple)")
            continue

        s = Solveur(vars, doms, inter)
        start = time.time()
        res = methode(s)
        end = time.time()
        
        print(f"\nAlgorithme: {nom}")
        print(f"Noeuds visités: {s.noeuds}")
        print(f"Temps: {end-start:.4f}s")
        if res and nom == "FC + MRV":
            print("Grille complétée :")
            imprimer_solution(grille, vars, res)

if __name__ == "__main__":
    evaluer("gridMP1.txt", "dictMP1.txt")
    evaluer("gridMP2.txt", "dictMP2.txt")
