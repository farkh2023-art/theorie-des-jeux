import pytest

from strategies import grim_trigger, tit_for_tat


@pytest.mark.parametrize(
    "history, expected",
    [([], "C"), ([('C', 'C')], "C"), ([('C', 'C'), ('D', 'D')], "T"),
     ([('C', 'C'), ('C', 'D')], "T")],
)
def test_grim_trigger_on_usual_histories(history, expected):
    assert grim_trigger(history) == expected


@pytest.mark.parametrize(
    "history, expected",
    [([], "C"), ([('C', 'D')], "D"), ([('D', 'C'), ('C', 'D')], "D")],
)
def test_tit_for_tat_on_usual_histories(history, expected):
    assert tit_for_tat(history) == expected
