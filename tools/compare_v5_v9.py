"""Compare les sorties des solveurs v5 et v9 sur des jeux fixes.

À lancer depuis n'importe quel répertoire avec Python et NumPy installés.
Ce script ne modifie ni v5 ni les matrices utilisées.
"""
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import argparse
import random
import sys


V9_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = V9_DIR.parent


def load_solver(module_name, source_path):
    spec = spec_from_file_location(module_name, source_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Impossible de charger le module depuis {source_path}")
    module = module_from_spec(spec)
    # Enregistrement préalable requis notamment par dataclasses.
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


v5 = load_solver("nash_solver_v5", ROOT_DIR / "pack-methode-v5" / "nash_solver.py")
v9 = load_solver("nash_solver_v9", V9_DIR / "nash_solver.py")

CASES = [
    ("matching pennies 2x2",
     [[1, -1], [-1, 1]], [[-1, 1], [1, -1]]),
    ("battle of the sexes 2x2",
     [[2, 0], [0, 1]], [[1, 0], [0, 2]]),
    ("rock paper scissors 3x3",
     [[0, -1, 1], [1, 0, -1], [-1, 1, 0]],
     [[0, 1, -1], [-1, 0, 1], [1, -1, 0]]),
    ("coordination 4x4",
     [[4, 1, 0, 0], [0, 3, 1, 0], [0, 0, 2, 1], [1, 0, 0, 4]],
     [[4, 1, 0, 0], [0, 3, 1, 0], [0, 0, 2, 1], [1, 0, 0, 4]]),
    ("rectangular 3x5",
     [[3, 0, 1, 0, 1], [0, 3, 1, 0, 1], [0, 0, 2, 0, 1]],
     [[3, 0, 1, 0, 1], [0, 3, 1, 0, 1], [0, 0, 2, 0, 1]]),
    ("coordination 5x5",
     [[2 if i == j else 0 for j in range(5)] for i in range(5)],
     [[2 if i == j else 0 for j in range(5)] for i in range(5)]),
    ("near support boundary 2x2",
     [[1, 0], [0, 1e-10]], [[-1, 0], [0, -1e-10]]),
]
EPSILONS = (1e-6, 1e-9, 1e-11, 1e-13)
EPSILON_TOLERANCE = 1e-12
REGRESSION_SEED = 20261109
RANDOM_GAME_COUNT = 300
RANDOM_SIZES = ((2, 2), (3, 3), (4, 4), (3, 5))
EQUILIBRIUM_IDENTITY_TOLERANCE = 1e-8
VALIDITY_TOLERANCE = 1e-8


def signature(equilibrium):
    return (
        equilibrium.row_support,
        equilibrium.column_support,
        tuple(round(float(p), 10) for p in equilibrium.row_probabilities),
        tuple(round(float(p), 10) for p in equilibrium.column_probabilities),
    )


def deviation_gains(row_payoffs, column_payoffs, equilibrium):
    """Gains maximaux d'une déviation pure unilatérale pour un résultat."""
    x = equilibrium.row_probabilities
    y = equilibrium.column_probabilities
    row_count = len(row_payoffs)
    column_count = len(row_payoffs[0])
    row_played = sum(x[i] * row_payoffs[i][j] * y[j]
                     for i in range(row_count) for j in range(column_count))
    column_played = sum(x[i] * column_payoffs[i][j] * y[j]
                        for i in range(row_count) for j in range(column_count))
    row_best = max(sum(row_payoffs[i][j] * y[j] for j in range(column_count))
                   for i in range(row_count))
    column_best = max(sum(x[i] * column_payoffs[i][j] for i in range(row_count))
                      for j in range(column_count))
    return max(0.0, row_best - row_played), max(0.0, column_best - column_played)


def validity_flags(row_payoffs, column_payoffs, equilibria):
    gains = [deviation_gains(row_payoffs, column_payoffs, eq) for eq in equilibria]
    return [max(row_gain, column_gain) < VALIDITY_TOLERANCE
            for row_gain, column_gain in gains]


def same_equilibrium(left, right):
    """Supports identiques et chaque probabilité à 1e-8 absolu près."""
    if (left.row_support != right.row_support or
            left.column_support != right.column_support):
        return False
    return (
        len(left.row_probabilities) == len(right.row_probabilities)
        and len(left.column_probabilities) == len(right.column_probabilities)
        and all(abs(float(a) - float(b)) <= EQUILIBRIUM_IDENTITY_TOLERANCE
                for a, b in zip(left.row_probabilities, right.row_probabilities))
        and all(abs(float(a) - float(b)) <= EQUILIBRIUM_IDENTITY_TOLERANCE
                for a, b in zip(left.column_probabilities, right.column_probabilities))
    )


def equilibrium_sets_differ(left, right):
    """Compare deux collections sans dépendre de l'ordre des résultats."""
    if len(left) != len(right):
        return True
    candidates = [[j for j, other in enumerate(right) if same_equilibrium(eq, other)]
                  for eq in left]
    matched_left = [-1] * len(right)

    def augment(i, seen):
        for j in candidates[i]:
            if seen[j]:
                continue
            seen[j] = True
            if matched_left[j] == -1 or augment(matched_left[j], seen):
                matched_left[j] = i
                return True
        return False

    return not all(augment(i, [False] * len(right)) for i in range(len(left)))


def compare_fixed_cases(verbose=False):
    for name, row_payoffs, column_payoffs in CASES:
        results_v5 = v5.find_mixed_nash(row_payoffs, column_payoffs)
        results_v9 = v9.find_mixed_nash(row_payoffs, column_payoffs)
        signatures_v5 = {signature(eq) for eq in results_v5}
        signatures_v9 = {signature(eq) for eq in results_v9}
        print(f"\n{name}")
        print(f"  v5: {len(results_v5)} équilibres")
        print(f"  v9: {len(results_v9)} équilibres")
        print(f"  ensembles différents: "
              f"{equilibrium_sets_differ(results_v5, results_v9)}")
        if verbose:
            print(f"  seulement v5: {sorted(signatures_v5 - signatures_v9)}")
            print(f"  seulement v9: {sorted(signatures_v9 - signatures_v5)}")


def compare_epsilon_cases(verbose=False):
    print(f"\nCas epsilon (tolerance={EPSILON_TOLERANCE:g})")
    for epsilon in EPSILONS:
        row_payoffs = [[1, 0], [0, epsilon]]
        column_payoffs = [[-value for value in row] for row in row_payoffs]
        print(f"  epsilon={epsilon:g}")
        for label, solver in (("v5", v5), ("v9", v9)):
            equilibria = solver.find_mixed_nash(
                row_payoffs, column_payoffs, tolerance=EPSILON_TOLERANCE
            )
            flags = validity_flags(row_payoffs, column_payoffs, equilibria)
            print(f"    {label}: {len(equilibria)} équilibres; "
                  f"valides={sum(flags)}/{len(flags)}")
            if verbose:
                print(f"      détails: {list(zip([signature(eq) for eq in equilibria], flags))}")


def random_game_cases():
    rng = random.Random(REGRESSION_SEED)
    cases = []
    for index in range(RANDOM_GAME_COUNT):
        row_count, column_count = RANDOM_SIZES[index % len(RANDOM_SIZES)]
        is_degenerate = index % 50 in (0, 1)
        if index % 50 == 0:
            # Jeu constant : toutes les actions donnent les mêmes gains.
            row_payoffs = [[0 for _ in range(column_count)] for _ in range(row_count)]
            column_payoffs = [[0 for _ in range(column_count)] for _ in range(row_count)]
        else:
            row_payoffs = [[rng.randint(-5, 5) for _ in range(column_count)]
                           for _ in range(row_count)]
            column_payoffs = [[rng.randint(-5, 5) for _ in range(column_count)]
                              for _ in range(row_count)]
            if index % 50 == 1:
                # Deux lignes identiques dans les deux matrices, créant des
                # réponses indifférentes et des cas dégénérés reproductibles.
                row_payoffs[1] = row_payoffs[0][:]
                column_payoffs[1] = column_payoffs[0][:]
        cases.append((index + 1, row_payoffs, column_payoffs, is_degenerate))
    return cases


def compare_random_games(verbose=False):
    differing_cases = []
    invalid_v5 = 0
    invalid_v9 = 0
    total_equilibria_v5 = 0
    total_equilibria_v9 = 0

    print(f"\n{RANDOM_GAME_COUNT} jeux aléatoires, graine={REGRESSION_SEED}; "
          "gains entiers dans [-5, 5]")
    print("Identité: supports égaux et probabilités égales à 1e-8 absolu près.")
    for case_number, row_payoffs, column_payoffs, is_degenerate in random_game_cases():
        results_v5 = v5.find_mixed_nash(row_payoffs, column_payoffs)
        results_v9 = v9.find_mixed_nash(row_payoffs, column_payoffs)
        flags_v5 = validity_flags(row_payoffs, column_payoffs, results_v5)
        flags_v9 = validity_flags(row_payoffs, column_payoffs, results_v9)
        invalid_v5 += flags_v5.count(False)
        invalid_v9 += flags_v9.count(False)
        total_equilibria_v5 += len(results_v5)
        total_equilibria_v9 += len(results_v9)
        differs = equilibrium_sets_differ(results_v5, results_v9)
        size = f"{len(row_payoffs)}x{len(row_payoffs[0])}"
        marker = " dégénéré" if is_degenerate else ""
        if verbose:
            print(f"  jeu {case_number:03d} {size}{marker}: "
                  f"v5 n={len(results_v5)} valide={flags_v5}; "
                  f"v9 n={len(results_v9)} valide={flags_v9}; "
                  f"différent={differs}")
        if differs:
            differing_cases.append((case_number, size, row_payoffs, column_payoffs,
                                    results_v5, flags_v5, results_v9, flags_v9))

    print("\nRésumé des jeux aléatoires")
    print(f"  Jeux avec équilibres différents: {len(differing_cases)} / {RANDOM_GAME_COUNT}")
    print(f"  Jeux dégénérés: {sum(case[3] for case in random_game_cases())} / "
          f"{RANDOM_GAME_COUNT}")
    print(f"  Équilibres invalides v5: {invalid_v5} / {total_equilibria_v5}")
    print(f"  Équilibres invalides v9: {invalid_v9} / {total_equilibria_v9}")
    print("  Cinq premiers cas différents (matrices, équilibres, validité):")
    for case in differing_cases[:5]:
        number, size, row_payoffs, column_payoffs, eq5, valid5, eq9, valid9 = case
        print(f"    jeu {number:03d} {size}")
        print(f"      A={row_payoffs}")
        print(f"      B={column_payoffs}")
        print(f"      v5={list(zip(eq5, valid5))}")
        print(f"      v9={list(zip(eq9, valid9))}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verbose", action="store_true",
        help="affiche aussi les équilibres détaillés et chaque jeu aléatoire",
    )
    args = parser.parse_args()
    compare_fixed_cases(verbose=args.verbose)
    compare_epsilon_cases(verbose=args.verbose)
    compare_random_games(verbose=args.verbose)


if __name__ == "__main__":
    main()
