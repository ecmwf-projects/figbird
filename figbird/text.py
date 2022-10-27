"""Module for formatting and processing strings, text and labels."""

import re

#: Metadata units which should be directly mapped to specific strings
MAPPABLE_UNITS = {
    "celsius": "°C",
    "degrees_celsius": "°C",
    "degrees_c": "°C",
    "farenheit": "°F",
    "degrees_farenheit": "°F",
    "degrees_f": "°F",
}


def pretty_units(units):
    """
    Map CF metadata units to pretty, HTML formatted units for labels and titles.

    CF unit grammar assumptions:
    - Multiplicands are separated by spaces
    - Dividends are separated by slashes
    - Numeric characters *following* letters are exponents, not preceding

    Parameters
    ----------
    units : str
        CF-compliant metadta units.

    Returns
    -------
    str
        HTML-formatted units to properly display exponents, symbols etc. through
        Plotly.

    Example
    -------
    >>> pretty_units("m s-1")
    "m s<sup>-1</sup>"
    """
    multiplicands = []
    for multiplicand in units.split(" "):
        dividends = []
        for dividend in multiplicand.split("/"):
            exponentiations = []
            for exponentiation in re.findall(r"[^\W\d_]+|-?\d+", dividend):
                if not exponentiation.isalpha() and exponentiations:
                    exponentiation = f"<sup>{exponentiation}</sup>"
                exponentiations.append(exponentiation)
            dividends.append("".join(exponentiations))
        multiplicands.append("/".join(dividends))
    units = "".join(multiplicands)

    for unit in MAPPABLE_UNITS:
        if unit in units:
            units = units.replace(unit, MAPPABLE_UNITS[unit])

    return units
