PRETTY_UNITS = {
    "celsius": "°C",
}


def pretty_units(units):
    """
    Map metadata units to pretty, HTML-formatted units for Plotly.

    Parameters
    ----------
    units : str
        Metadata units to map into HTML-formatted units for Plotly.

    Returns
    -------
    str
        HTML-formatted units for Plotly.

    Example
    -------
    >>> pretty_units("m s-1")
    "m s<sup>-1</sup>"
    """
    units_split = units.split(' ')
    units_join = []
    for unit in units_split:
        if len(unit)>0:
            if unit[0].isalpha() and unit[-1].isnumeric():
                # find split point
                for i in range(len(unit)):
                    if not unit[i].isalpha():
                        break
                units_join += [f'{unit[:i]}<sup>{unit[i:]}</sup>']
            else:
                units_join += [unit]
    units = ' '.join(units_join)
    return PRETTY_UNITS.get(units, units)
