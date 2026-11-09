"""Dilemme du prisonnier répété avec stratégie Grim."""
from repeated_game import discounted_payoff, grim_threshold
from strategies import grim_trigger


R, T, P = 3, 5, 1
delta = 0.6
history = [("C", "C"), ("C", "C")]
print("Seuil Grim:", grim_threshold(R, T, P))
print("Coopération soutenable:", delta > grim_threshold(R, T, P))
print("Action après l'historique:", grim_trigger(history))
print("Valeur actualisée de la coopération:", discounted_payoff([R] * 5, delta))
