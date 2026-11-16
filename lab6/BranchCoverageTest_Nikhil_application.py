"""Comprehensive tests for every decision branch in highway_toll.py."""

import pytest

from highway_toll import pass_advice, toll_charge, toll_for


def test_invalid_axle_count_branch():
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, False, False)


def test_each_base_rate_and_unknown_axle_fallback():
    assert toll_for(2, False, False) == 100.0
    assert toll_for(3, False, False) == 150.0
    assert toll_for(4, False, False) == 250.0
    assert toll_for(6, False, False) == 400.0


def test_peak_and_fastag_branches_for_two_and_other_axles():
    assert toll_for(2, True, False) == 125.0
    assert toll_for(2, False, True) == 90.0
    assert toll_for(3, True, True) == 178.12
    assert toll_for(4, False, True) == 237.5
    assert toll_for(5, True, True) == 475.0


def test_exempt_and_non_exempt_vehicles():
    assert toll_charge("ambulance", 2, False, False) == 0
    assert toll_charge("fire_engine", 4, True, True) == 0
    assert toll_charge("car", 2, False, False) == 100.0


def test_pass_advice_buy_either_and_pay_per_trip():
    trips = [(False, False)]
    assert pass_advice(trips, 2, 99.0) == "buy_pass"
    assert pass_advice(trips, 2, 100.0) == "either"
    assert pass_advice(trips, 2, 101.0) == "pay_per_trip"


def test_pass_advice_with_no_trips():
    assert pass_advice([], 2, 1.0) == "pay_per_trip"
