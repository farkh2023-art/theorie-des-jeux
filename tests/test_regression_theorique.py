"""Résultats théoriques fixes pour contrôler les familles couvertes en v5/v8.

Les cas sont définis indépendamment du code du solveur. La comparaison aux
équilibres ci-dessous ne constitue pas une exécution ni une preuve exhaustive.
"""
import pytest

from nash_solver import find_mixed_nash


def has_support_equilibrium(A, B, rows, cols, row_probs, col_probs, tol=1e-8):
    equilibria = find_mixed_nash(A, B, tolerance=tol)
    for eq in equilibria:
        if eq.row_support != rows or eq.column_support != cols:
            continue
        if all(a == pytest.approx(b, abs=tol) for a, b in zip(eq.row_probabilities, row_probs)) and \
           all(a == pytest.approx(b, abs=tol) for a, b in zip(eq.column_probabilities, col_probs)):
            return True
    return False


@pytest.mark.parametrize("A,B,rows,cols,x,y,tol", [
    ([[3, 0], [5, 1]], [[3, 5], [0, 1]], (1,), (1,), (0, 1), (0, 1), 1e-8),
    ([[1, -1], [-1, 1]], [[-1, 1], [1, -1]], (0, 1), (0, 1), (.5, .5), (.5, .5), 1e-8),
    ([[2, 0], [0, 1]], [[1, 0], [0, 2]], (0,), (0,), (1, 0), (1, 0), 1e-8),
    ([[0, -1, 1], [1, 0, -1], [-1, 1, 0]],
     [[0, 1, -1], [-1, 0, 1], [1, -1, 0]],
     (0, 1, 2), (0, 1, 2), (1/3, 1/3, 1/3), (1/3, 1/3, 1/3), 1e-8),
    ([[3, 0, 0], [0, 2, 0], [0, 0, 1]],
     [[3, 0, 0], [0, 2, 0], [0, 0, 1]], (0,), (0,), (1, 0, 0), (1, 0, 0), 1e-8),
    ([[4, 1, 0, 0], [0, 3, 1, 0], [0, 0, 2, 1], [1, 0, 0, 4]],
     [[4, 1, 0, 0], [0, 3, 1, 0], [0, 0, 2, 1], [1, 0, 0, 4]],
     (0,), (0,), (1, 0, 0, 0), (1, 0, 0, 0), 1e-8),
    ([[2, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 2, 0], [0, 0, 0, 0, 2]],
     [[2, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 0, 2, 0, 0], [0, 0, 0, 2, 0], [0, 0, 0, 0, 2]],
     (0,), (0,), (1, 0, 0, 0, 0), (1, 0, 0, 0, 0), 1e-8),
    ([[3, 0, 1, 0, 1], [0, 3, 1, 0, 1], [0, 0, 2, 0, 1]],
     [[3, 0, 1, 0, 1], [0, 3, 1, 0, 1], [0, 0, 2, 0, 1]],
     (0,), (0,), (1, 0, 0), (1, 0, 0, 0, 0), 1e-8),
    ([[1, -1], [-1, 1 + 1e-7]], [[-1, 1], [1, -1 - 1e-7]],
     (0, 1), (0, 1),
     ((2 + 1e-7) / (4 + 1e-7), 2 / (4 + 1e-7)),
     ((2 + 1e-7) / (4 + 1e-7), 2 / (4 + 1e-7)), 1e-10),
    ([[1, 0], [0, 1e-6]], [[1, 0], [0, 1e-6]],
     (0,), (0,), (1, 0), (1, 0), 1e-10),
])
def test_theoretical_equilibrium_regressions(A, B, rows, cols, x, y, tol):
    assert sum(x) == pytest.approx(1.0)
    assert sum(y) == pytest.approx(1.0)
    assert has_support_equilibrium(A, B, rows, cols, x, y, tol)


def test_mixed_equilibrium_near_support_boundary_with_tight_tolerance():
    epsilon = 1e-10
    A = [[1, 0], [0, epsilon]]
    B = [[-value for value in row] for row in A]
    probability = epsilon / (1 + epsilon)
    expected = (probability, 1 - probability)
    assert has_support_equilibrium(
        A, B, (0, 1), (0, 1), expected, expected, tol=1e-12
    )


def test_loose_tolerance_outputs_epsilon_equilibria_by_best_response():
    epsilon = 1e-10
    tolerance = 1e-9
    A = [[1, 0], [0, epsilon]]
    B = [[-value for value in row] for row in A]
    equilibria = find_mixed_nash(A, B, tolerance=tolerance)
    assert equilibria

    for equilibrium in equilibria:
        x = equilibrium.row_probabilities
        y = equilibrium.column_probabilities
        played_row_payoff = sum(x[i] * A[i][j] * y[j]
                                for i in range(2) for j in range(2))
        played_column_payoff = sum(x[i] * B[i][j] * y[j]
                                   for i in range(2) for j in range(2))
        row_best_response = max(sum(A[i][j] * y[j] for j in range(2))
                                for i in range(2))
        column_best_response = max(sum(x[i] * B[i][j] for i in range(2))
                                   for j in range(2))
        assert 0 <= row_best_response - played_row_payoff < tolerance
        assert 0 <= column_best_response - played_column_payoff < tolerance
