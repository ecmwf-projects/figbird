PRETTY_UNITS = {
    "celsius": "°C",
    "m s-1": "m s<sup>-1</sup>",
    "m2 s-1": "m<sup>2</sup> s<sup>-1</sup>",
    "m2 m-2": "m<sup>2</sup> m<sup>-2</sup>",
    "m3 m-3": "m<sup>3</sup> m<sup>-3</sup>",
    "w m-2": "W m<sup>-2</sup>",
    "kg m-2": "kg m<sup>-2</sup>",
    "kg m-3": "kg m<sup>-3</sup>",
    "j m-2": "J m<sup>-2</sup>",
    "kg m-2 s-1": "kg m<sup>-2</sup> s<sup>-1</sup>",
    "n m-2": "N m<sup>-2</sup>",
    "n m-2 s": "N m<sup>-2</sup> s",
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
    return PRETTY_UNITS.get(units, units)
