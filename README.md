# Pack méthode V9 — théorie des jeux

Snapshot candidat canonique consolidé, basé sur v8. Il conserve le solveur
général par énumération des supports et l'optimisation ciblée 5×5.

## Installation locale et tests

Depuis ce dossier, exécuter ces trois commandes :

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt pytest
.venv/Scripts/python -m pytest -q
```

Sous Linux/macOS, utiliser `.venv/bin/python` aux deux dernières commandes.

La contrainte `numpy>=1.24,<3` est un choix de compatibilité prudent à valider
sur les environnements du projet.

## Exemples

```bash
python example_prisoners_dilemma.py
python example_nash_general.py
python example_nash_5x5.py
```

Le solveur énumère les équilibres isolés à supports de même cardinalité. Les
continua d'équilibres dégénérés ne sont pas représentés. Le coût combinatoire
augmente avec la taille des matrices.

### Tolérance du solveur

Le paramètre `tolerance` joue deux rôles : toute probabilité de support
inférieure ou égale à ce seuil est traitée comme nulle, et le gain maximal
d'une déviation unilatérale peut dépasser le gain joué d'au plus ce seuil.
Les résultats sont donc des `tolerance`-équilibres (epsilon-équilibres), pas
nécessairement des équilibres exacts. La même tolérance est utilisée par
`find_pure_nash` et `find_mixed_nash`.

## Performance

Les tests marqués `performance` utilisent des budgets muraux larges à 2×2, 4×4
et 5×5. Ils dépendent de l'environnement et n'ont pas été lancés ici. Le
benchmark v8 5×5 reste disponible dans `benchmarks/benchmark_5x5.py`.

La CI Linux et Windows exécute la suite pytest ; elle n'a pas été lancée ici.
