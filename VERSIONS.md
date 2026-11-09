# Statut des snapshots

| Snapshot | Statut | Note |
|---|---|---|
| `pack-methode/` | Historique v1 | API historique `threshold_delta`; périmètre initial incomplet. |
| `pack-methode-v2/` | Historique v2 | Renomme le seuil Grim et ajoute un premier test. |
| `pack-methode-v3/` | Historique v3 | Première version avec solveur de Nash. |
| `pack-methode-v4/` | Historique v4 | Solveur mixte général et validations des matrices. |
| `pack-methode-v5/` | Référence de couverture | Tests et budgets 2×2/4×4 restaurés dans v9. |
| `pack-methode-v6/` | Snapshot d'optimisation | Introduit les optimisations ciblées 5×5. |
| `pack-methode-v7/` | Snapshot CI Linux | Ajoute la CI Linux multi-version Python. |
| `pack-methode-v8/` | Base de consolidation | Dernier snapshot avant consolidation ; tests non exécutés ici. |
| `pack-methode-v9/` | Candidat canonique | Consolidation basée sur v8 ; attend validation locale. |

Commande de test depuis `pack-methode-v9/` : `python -m pytest -q`.

Version de référence. Validée le 9 novembre 2026 sur Windows, Python 3.12,
NumPy 2.5.4, pytest 9.2.0, en environnement virtuel vierge.
- 51 tests réussis.
- Comparaison avec pack-methode-v5 (tools/compare_v5_v9.py) : mêmes équilibres
  sur 7 matrices de référence, sur les cas epsilon 1e-6 à 1e-13 (tolérance
  1e-12) et sur 300 jeux aléatoires reproductibles (graine 20261109, tailles
  2x2 à 4x4 et 3x5, dont 12 jeux dégénérés) ; 0 équilibre invalide sur 618
  par version (contrôle par meilleure réponse).
- Non couvert : Python 3.10, 3.11, 3.13 et Linux (CI non exécutée), tailles
  supérieures à 5x5, jeux dégénérés à continuum d'équilibres, exhaustivité
  des équilibres au-delà des supports de même taille.
