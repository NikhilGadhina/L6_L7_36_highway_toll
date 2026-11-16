"""Tests aimed at demonstrating complete line coverage with missed branches.

Every executable statement in highway_toll.py is reached, while peak and
FASTag false outcomes are deliberately left for the branch-coverage suite.
"""

import pytest

from highway_toll import pass_advice, toll_charge, toll_for


def test_invalid_axle_count_raises():
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, True, True)


def test_peak_fastag_rates_cover_base_and_fallback_paths():
    assert toll_for(2, True, True) == 112.5
    assert toll_for(3, True, True) == 178.12
    assert toll_for(5, True, True) == 475.0


def test_exempt_and_non_exempt_vehicle_paths():
    assert toll_charge("ambulance", 2, True, True) == 0
    assert toll_charge("car", 2, True, True) == 112.5


@pytest.mark.parametrize(
    ("pass_price", "expected"),
    [
        (112.0, "buy_pass"),
        (112.5, "either"),
        (113.0, "pay_per_trip"),
    ],
)
def test_pass_advice_outcomes(pass_price, expected):
    assert pass_advice([(True, True)], 2, pass_price) == expected
