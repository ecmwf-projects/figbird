import numpy as np

from . import calendar  # noqa: F401


def cyclify(data):
    return np.concatenate(([data[-1]], data, [data[0]]))
