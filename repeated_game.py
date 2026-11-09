"""Outils pour les jeux répétés et le seuil de coopération Grim."""


def discounted_payoff(stream, delta):
    """Somme actualisée d'un flux, pour un facteur delta dans [0, 1)."""
    if not 0 <= delta < 1:
        raise ValueError("delta doit appartenir à [0, 1).")
    return sum(delta**t * gain for t, gain in enumerate(stream))


def grim_threshold(R, T, P):
    """Seuil d'actualisation de Grim sous les gains T > R > P.

    L'ordre T > R > P est requis par le modèle de dilemme social considéré.
    Il garantit aussi un dénominateur non nul et un seuil dans (0, 1).
    """
    if T == P:
        raise ValueError("T et P doivent être différents pour calculer le seuil Grim.")
    if not T > R > P:
        raise ValueError("Les gains doivent respecter T > R > P.")
    return (T - R) / (T - P)


def threshold_delta(R, T, P):
    """Déprécié : utiliser :func:`grim_threshold` à la place."""
    return grim_threshold(R, T, P)
