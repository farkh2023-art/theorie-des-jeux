"""Équilibre mixte de pierre-papier-ciseaux, jeu 3×3 à somme nulle."""
from nash_solver import find_mixed_nash


A = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
B = [[-value for value in row] for row in A]
for equilibrium in find_mixed_nash(A, B):
    print(equilibrium)

# Équilibre théorique attendu : probabilités uniformes et gains (0, 0).
