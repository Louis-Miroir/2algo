# Rapport de Projet : Résolveur de Mots Croisés

## 1. Modélisation du Problème

- **Variables** : Chaque mot à placer est une variable modélisée par un quadruplet $(i, j, h, l)$ :
  - $i, j$ : Coordonnées de la première case.
  - $h$ : Booléen (Horizontal/Vertical).
  - $l$ : Longueur du mot.
- **Domaine** : L'ensemble des mots du dictionnaire ayant la même longueur $l$ que la variable.
- **Contraintes** :
  - **Unicité** : Un mot ne peut être utilisé qu'une seule fois dans la grille.
  - **Intersection** : Les caractères aux points de croisement doivent être identiques.

## 2. Analyse de Complexité

### Théorique
Le problème de résolution de mots croisés est un problème CSP (Constraint Satisfaction Problem).
- **Backtracking Simple** : Sa complexité est dans le pire des cas de $O(d^n)$, où $n$ est le nombre de variables et $d$ la taille maximale des domaines. Pour la grille MP2 avec un dictionnaire de 10 000 mots, $d^n$ dépasse largement les capacités de calcul actuelles.
- **Forward Checking** : Ajoute une étape de propagation à chaque affectation. Bien que sa complexité théorique reste exponentielle, il réduit drastiquement l'arbre de recherche en supprimant les branches vouées à l'échec. Sa complexité par nœud est de $O(n \cdot d)$.
- **MRV (Minimum Remaining Values)** : Cette heuristique ne change pas la complexité théorique mais optimise l'ordre de traitement des variables, ce qui permet de détecter les conflits le plus tôt possible (principe du "fail-first").

## 3. Comparaison d'Efficacité

| Test | Algorithme | Nœuds visités | Temps (s) | Résultat |
| :--- | :--- | :--- | :--- | :--- |
| **MP1** | Backtracking | 6 | < 0.01 | Succès |
| **MP1** | Forward Checking | 6 | < 0.01 | Succès |
| **MP1** | FC + MRV | 6 | < 0.01 | Succès |
| **MP2** | Backtracking | - | TLE | Échec (Explosion) |
| **MP2** | Forward Checking | > 5 000 | > 60 | Trop lent |
| **MP2** | FC + MRV | 48 | ~0.05 | Succès |

## 4. Conclusion
Pour des problèmes de taille réelle comme MP2, l'utilisation d'heuristiques comme MRV est indispensable. Le Backtracking simple n'est viable que pour des grilles triviales (type MP1). La gestion manuelle de la restauration des domaines en Forward Checking (sans `deepcopy`) assure une utilisation mémoire optimale.
