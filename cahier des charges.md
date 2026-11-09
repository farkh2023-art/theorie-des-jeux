# Cahier des charges general

## Exigence de performance 5x5
Le solveur doit traiter les jeux bimatriciels 5x5 par enumeration des supports avec cache des combinaisons, detection vectorisee des cas purs et allocations limitees. Les tests doivent verifier l'exactitude d'un equilibre 5x5 uniforme, la reutilisation du cache et un budget large de non-regression. Un benchmark reproductible doit mesurer plusieurs jeux aleatoires 5x5 et produire un rapport JSON.

## Limite
L'enumeration des supports garde une complexite combinatoire. L'optimisation cible les couts constants des jeux 5x5, sans promettre une mise a l'echelle arbitraire.

## Integration continue
- Declenchement sur push vers main, pull request et lancement manuel.
- Matrice Python 3.10, 3.11, 3.12 et 3.13.
- Cache pip, installation des dependances et execution de tous les tests.
- Job distinct pour le benchmark 5x5 et publication du rapport JSON.
- Permissions minimales en lecture et annulation des executions obsoletes.

## Compatibilite Windows
- Ajouter un job GitHub Actions distinct sur `windows-latest`.
- Tester Python 3.10, 3.11, 3.12 et 3.13.
- Installer les dependances et executer les tests avec PowerShell.
- Executer l'exemple 5x5 comme verification de bout en bout.
