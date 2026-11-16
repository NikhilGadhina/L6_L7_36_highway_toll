"""Validated input helpers for the Lab 7 highway toll exercise."""

import re


_PLATE_PATTERN = re.compile(r"([A-Za-z]{2})-([0-9]{1,2})-([A-Za-z]{1,3})-([0-9]{1,4})")
_TRIP_PATTERN = re.compile(r"([0-9]+)\s*[xX]\s*([0-9]+)")


def parse_plate(plate):
    """Return (uppercase state, district number, registration number).

    Accepted plates have the form ``KA-05-AB-1234``. Invalid types, malformed
    fields, and district codes outside 01-99 raise ValueError rather than
    leaking implementation exceptions or silently accepting bad data.
    """
    if not isinstance(plate, str):
        raise ValueError("plate must be text in the form SS-DD-SERIES-NUMBER")

    match = _PLATE_PATTERN.fullmatch(plate.strip())
    if match is None:
        raise ValueError("plate must match SS-DD-SERIES-NUMBER (for example KA-05-AB-1234)")

    state, district_text, _series, number_text = match.groups()
    district = int(district_text)
    if not 1 <= district <= 99:
        raise ValueError("district code must be between 01 and 99")

    return state.upper(), district, int(number_text)


def trip_cost(text):
    """Calculate trips × rate from a non-negative integer expression."""
    if not isinstance(text, str):
        raise ValueError("trip cost must be text in the form trips x rate")

    match = _TRIP_PATTERN.fullmatch(text.strip())
    if match is None:
        raise ValueError("trip cost must match trips x rate using non-negative whole numbers")

    count, rate = (int(value) for value in match.groups())
    return count * rate


def axle_class(axles):
    """Classify a whole-number axle count; at least two axles are required."""
    if isinstance(axles, bool):
        raise ValueError("axle count must be a whole number of at least 2")

    if isinstance(axles, int):
        number = axles
    elif isinstance(axles, str) and re.fullmatch(r"\s*[0-9]+\s*", axles):
        number = int(axles.strip())
    else:
        raise ValueError("axle count must be a whole number of at least 2")

    if number < 2:
        raise ValueError("axle count must be at least 2")
    if number == 2:
        return "car"
    if number <= 4:
        return "truck"
    return "heavy"


def _read_result(prompt, function, label):
    """Read one value and report controlled validation errors to the user."""
    value = input(prompt)
    try:
        result = function(value)
    except ValueError as exc:
        print(f"Invalid {label}: {exc}")
        return
    print(f"{label}:", result)


def main():
    print("==== Running parse_plate ====")
    _read_result("Enter a plate (e.g. KA-05-AB-1234): ", parse_plate, "State, District and Number")

    print("\n==== Running trip_cost ====")
    _read_result("Enter trips x rate (e.g. 3x150): ", trip_cost, "Trip Cost")

    print("\n==== Running axle_class ====")
    _read_result("Enter an axle count (e.g. 3): ", axle_class, "Vehicle Class")


if __name__ == "__main__":
    main()
