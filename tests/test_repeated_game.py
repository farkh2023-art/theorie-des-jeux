import pytest

from repeated_game import discounted_payoff, grim_threshold, threshold_delta


def test_discounted_payoff_zero_discount():
    assert discounted_payoff([4, 99, 99], 0) == 4


def test_discounted_payoff_normal_values():
    assert discounted_payoff([3, 3, 3], 0.5) == pytest.approx(5.25)


@pytest.mark.parametrize("delta", [1, -0.01])
def test_discounted_payoff_rejects_out_of_range_delta(delta):
    with pytest.raises(ValueError):
        discounted_payoff([1, 2], delta)


def test_grim_threshold_known_value():
    assert grim_threshold(3, 5, 1) == pytest.approx(0.5)


def test_grim_threshold_rejects_equal_t_and_p_explicitly():
    with pytest.raises(ValueError, match="T et P"):
        grim_threshold(2, 2, 2)


@pytest.mark.parametrize("gains", [(3, 2, 1), (1, 3, 2), (3, 1, 2)])
def test_grim_threshold_requires_ordered_gains(gains):
    with pytest.raises(ValueError, match="T > R > P"):
        grim_threshold(*gains)


def test_deprecated_threshold_delta_alias():
    assert threshold_delta(3, 5, 1) == pytest.approx(grim_threshold(3, 5, 1))
