"""Property-based input-validation tests for the Lab 7 toll functions.

The fuzz properties allow a documented ValueError for invalid input, but reject
unexpected crashes and values returned for malformed or semantically invalid data.
"""

import re

import pytest
from hypothesis import given, settings, strategies as st

from highway_toll import axle_class, parse_plate, trip_cost


ANY_INPUT = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.booleans(),
    st.floats(allow_nan=True, allow_infinity=True),
)

PLATE_PATTERN = re.compile(
    r"^([A-Za-z]{2})-([0-9]{1,2})-([A-Za-z]{1,3})-([0-9]{1,4})$"
)
TRIP_PATTERN = re.compile(r"^\s*([0-9]+)\s*[xX]\s*([0-9]+)\s*$")


def _assert_value_or_validation_error(function, value, is_valid_result):
    """Reject unexpected exceptions and reject silent acceptance of bad data."""
    try:
        result = function(value)
    except ValueError:
        return
    except Exception as exc:  # pragma: no cover - exercised by Hypothesis on bugs
        pytest.fail(
            f"{function.__name__} raised unexpected "
            f"{type(exc).__name__} for {value!r}: {exc}"
        )
    assert is_valid_result(value, result), (
        f"{function.__name__} silently accepted invalid input {value!r} "
        f"and returned {result!r}"
    )


def _valid_plate_result(value, result):
    if not isinstance(value, str):
        return False
    match = PLATE_PATTERN.fullmatch(value.strip())
    if not match:
        return False
    state, district, _series, number = match.groups()
    return (
        1 <= int(district) <= 99
        and result == (state.upper(), int(district), int(number))
    )


def _valid_trip_result(value, result):
    if not isinstance(value, str):
        return False
    match = TRIP_PATTERN.fullmatch(value)
    return bool(match and result == int(match.group(1)) * int(match.group(2)))


def _valid_axle_result(value, result):
    if isinstance(value, bool):
        return False
    if isinstance(value, int):
        number = value
    elif isinstance(value, str) and re.fullmatch(r"\s*[0-9]+\s*", value):
        number = int(value)
    else:
        return False
    if number < 2:
        return False
    expected = "car" if number == 2 else "truck" if number <= 4 else "heavy"
    return result == expected


@settings(max_examples=300, deadline=None)
@given(ANY_INPUT)
def test_parse_plate_fuzzes_unexpected_inputs(value):
    _assert_value_or_validation_error(parse_plate, value, _valid_plate_result)


@settings(max_examples=300, deadline=None)
@given(ANY_INPUT)
def test_trip_cost_fuzzes_unexpected_inputs(value):
    _assert_value_or_validation_error(trip_cost, value, _valid_trip_result)


@settings(max_examples=300, deadline=None)
@given(ANY_INPUT)
def test_axle_class_fuzzes_unexpected_inputs(value):
    _assert_value_or_validation_error(axle_class, value, _valid_axle_result)


@settings(max_examples=100, deadline=None)
@given(
    state=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=2, max_size=2),
    district=st.integers(min_value=1, max_value=99),
    series=st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1, max_size=3),
    number=st.integers(min_value=0, max_value=9999),
)
def test_parse_plate_valid_generated_plates(state, district, series, number):
    plate = f"{state}-{district:02d}-{series}-{number:04d}"
    assert parse_plate(plate) == (state, district, number)


@settings(max_examples=100, deadline=None)
@given(count=st.integers(min_value=0, max_value=10**6), rate=st.integers(min_value=0, max_value=10**6))
def test_trip_cost_valid_generated_inputs(count, rate):
    assert trip_cost(f"{count}X{rate}") == count * rate


@settings(max_examples=100, deadline=None)
@given(number=st.integers(min_value=2, max_value=10**6))
def test_axle_class_valid_generated_counts(number):
    expected = "car" if number == 2 else "truck" if number <= 4 else "heavy"
    assert axle_class(str(number)) == expected


@pytest.mark.parametrize("plate", [None, "", "KA-05-AB-1234-extra", "K-05-AB-1234", "KA-00-AB-1"])
def test_parse_plate_rejects_invalid_examples(plate):
    with pytest.raises(ValueError):
        parse_plate(plate)


@pytest.mark.parametrize("text", [None, "", "3x-1", "-1x10", "2x3x4", "three x 150"])
def test_trip_cost_rejects_invalid_examples(text):
    with pytest.raises(ValueError):
        trip_cost(text)


@pytest.mark.parametrize("axles", [None, True, 1, -5, 2.5, "2.5", ""])
def test_axle_class_rejects_invalid_examples(axles):
    with pytest.raises(ValueError):
        axle_class(axles)
