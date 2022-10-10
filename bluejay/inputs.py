import teal
from six import string_types


class TealIncompatibility(Exception):
    pass


def polymorphic_input(function):
    def wrapper(data=None, *args, **kwargs):
        if data is not None:
            teal_data = teal.open(data)
            for method in (xarray_input, numpy_input):
                try:
                    args, kwargs = method(teal_data, *args, **kwargs)
                except TealIncompatibility:
                    continue
                else:
                    break
            else:
                raise TypeError("unable to read input data")

        return function(*args, **kwargs)

    return wrapper


def numpy_input(data, *args, **kwargs):
    try:
        ndarray = data.to_numpy()
    except:  # noqa: E722
        raise TealIncompatibility()

    x = kwargs.get("x")
    y = kwargs.get("y")

    if x is None and y is None:
        if ndarray.ndim == 1:
            y = ndarray
            x = list(range(len(y)))
        elif ndarray.ndim == 2:
            y, x = ndarray
        else:
            raise ValueError(
                f"data must have at most 2 dimensions, but found {ndarray.ndim}"
            )
    elif x is None:
        x = ndarray
    elif y is None:
        y = ndarray

    return args, {**kwargs, **{"x": x, "y": y}}


def xarray_input(data, *args, **kwargs):
    try:
        dataset = data.to_xarray().squeeze()
    except:  # noqa: E722
        raise TealIncompatibility()

    x = kwargs.get("x")
    y = kwargs.get("y")

    if x is None or y is None:
        n_dims = len(dataset.dims)
        n_vars = len(dataset.data_vars)
        if n_dims != 1:
            raise ValueError(
                f"data must have exactly 1 dimension, but found {n_dims}; "
                f"either slice the data down to 1 dimension or pass the 'x' "
                f"and 'y' arguments to select named dimensions/coordinates"
            )
        if n_vars != 1:
            raise ValueError(
                f"data must have exactly 1 data variable, but found {n_vars}; "
                f"either slice the data down to 1 variable or pass the 'x' "
                f"and 'y' arguments to select a variable"
            )

        if x is None and y is None:
            x = dataset[list(dataset.dims)[0]].values
            y = dataset[list(dataset.data_vars)[0]].values
        elif x is None:
            if isinstance(y, string_types) and y in dataset.dims:
                x = dataset[list(dataset.data_vars)[0]].values
                y = dataset[list(dataset.dims)[0]].values
            else:
                x = dataset[list(dataset.data_vars)[0]].values
        elif y is None:
            if isinstance(x, string_types) and x in dataset.dims:
                y = dataset[list(dataset.data_vars)[0]].values
                x = dataset[list(dataset.dims)[0]].values
            else:
                y = dataset[list(dataset.data_vars)[0]].values

    else:
        x = search_for_facet(dataset, x, "x")
        y = search_for_facet(dataset, y, "y")

    var_kwargs = {"x": x, "y": y}

    return args, {**kwargs, **var_kwargs}


def search_for_facet(dataset, facet, facet_name):
    if facet in dataset.dims:
        result = dataset[facet].values
    elif facet in dataset.data_vars:
        result = dataset[facet].values
    else:
        facet_name = facet_name or facet
        raise ValueError(f"unable to match {facet_name} value '{facet}' against data")
    return result
