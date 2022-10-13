import warnings

import teal
import xarray as xr

from .schema import schema


class TealIncompatibility(Exception):
    pass


def polymorphic(function):
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
    except (ValueError, NotImplementedError):  # noqa: E722
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
        dataset = xr.Dataset(data.to_xarray()).squeeze()
    except (ValueError, NotImplementedError):  # noqa: E722
        raise TealIncompatibility()

    dims = list(dataset.dims)
    data_vars = list(dataset.data_vars)

    if len(dims) != 1:
        raise ValueError(
            f"data must have exactly 1 dimension, but found {len(dims)}; "
            f"please reduce the data down to 1 dimension"
        )

    done_axis = []
    assigned_axes = [kwargs.get(ax) for ax in ("x", "y")]
    var_kwargs = dict()
    var_keys = dict()
    for axis_name in ["x", "y"]:
        axis = kwargs.get(axis_name)
        if axis is None:
            if dims[0] not in done_axis + assigned_axes:
                var_kwargs[axis_name] = dataset[dims[0]].values
                var_keys[axis_name] = dims[0]
                done_axis += [dims[0]]
            else:
                data_var = data_vars[0]
                if len(data_vars) > 1:
                    warnings.warn(
                        f"dataset contains more than one data variable; "
                        f"variable '{data_var}' has been selected for plotting"
                    )
                var_keys[axis_name] = data_var
                var_kwargs[axis_name] = dataset[data_var].values
        else:
            var_kwargs[axis_name] = dataset[axis].values
            var_keys[axis_name] = axis

    if schema.settings.auto_label_axes:
        kwargs = _auto_label_axes(var_keys, kwargs)

    return args, {**kwargs, **var_kwargs}


def _auto_label_axes(var_keys, kwargs):
    kwargs.setdefault("_update_layout", dict())
    for axis in var_keys:
        axis_kwargs = kwargs.get("_update_layout", dict()).get(f"{axis}axis", dict())
        axis_kwargs.setdefault("title", var_keys[axis])
        kwargs["_update_layout"].setdefault(f"{axis}axis", axis_kwargs)
    return kwargs
