# reversi_heuristic_vs_MonteCarlo

J’ai implémenté deux IA pour jouer le jeu Reversi.

La première IA utilise l’algorithme MTDF avec une fonction heuristique pour trouver le meilleur coup à jouer.

Description de l'heuristique de la première IA :
Cette fonction dépend de trois éléments :
- Mobilité : plus on a des coups à jouer mieux c’est.
- Stabilité : on donne des bonus aux pièces stables.
- Possession des coins.
- Parité des pièces.

La deuxième IA utilise l’algorithme Monte Carlo Tree Search.

### résultats sur 50 parties entre ces deux IA:

![](https://raw.githubusercontent.com/MohamedAminMallek/reversi_heuristic_vs_MonteCarlo/master/results.png)
