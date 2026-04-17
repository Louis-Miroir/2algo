# Spécifications du Projet : Solveur de Mots Croisés CSP

## Structure des Variables
Une variable est un quadruplet : `(i, j, h, l)`
- `i`, `j` : coordonnées de départ (ligne, colonne).
- `h` : booléen (True si horizontal, False si vertical).
- `l` : longueur du mot.

## Contraintes du Projet
1. Interdiction d'utiliser des bibliothèques externes (sauf time, random).
2. Grille : Liste de listes (0 pour blanc '_', 1 pour noir '#').
3. Algorithmes à implémenter :
   - Backtracking (BT)
   - Forward Checking (FC) : avec restauration manuelle des domaines (pas de deepcopy).
   - FC + MRV (Minimum Remaining Values).
4. Intersections : Pré-calculer les contraintes entre variables partageant une case.
5. La génération de code par l'IA est interdite

## Architecture des Fichiers
- `loader.py` : Chargement fichiers TXT et extraction des variables.
- `utils.py` : Calcul des intersections et affichage.
- `solver.py` : Fonctions récursives de résolution (BT, FC, MRV).
- `main.py` : Orchestration et mesures de performance.