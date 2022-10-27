# (C) Copyright 2022 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

import warnings

import emohawk
import xarray as xr

from . import metadata, transformers

INPUT_ONLY_KWARGS = ["cyclic"]


def discard_input_only_kwargs(function):
    def wrapper(self, *args, **kwargs):
        result = function(self, *args, **kwargs)
        if result is not None:

            args, kwargs = result
            if kwargs.get("cyclic"):
                lengths = [len(kwargs[axis]) for axis in self.AXES]
                min_len = min(lengths)
                max_len = max(lengths)
                if min_len != max_len:
                    for axis in self.AXES:
                        if len(kwargs[axis]) == max_len - 2:
                            kwargs[axis] = transformers.cyclify(kwargs[axis])

            for kwarg in INPUT_ONLY_KWARGS:
                result[1].pop(kwarg, None)
        return result

    return wrapper


@discard_input_only_kwargs
def xarray(self, data, args, kwargs):
    try:
        dataset = xr.Dataset(emohawk.open(data).to_xarray()).squeeze()
    except (NotImplementedError, ValueError):
        return None

    if len(dataset.dims) != 1:
        raise ValueError(
            f"data must have exactly 1 dimension, but found "
            f"{len(dataset.dims)}; please reduce the data down to 1 dimension"
        )
    dim = list(dataset.dims)[0]

    data_vars = list(dataset.data_vars)

    axis_attrs = dict()
    assigned_attrs = [
        kwargs.get(axis).split(".")[-1] for axis in self.AXES if axis in kwargs
    ]
    for axis in self.AXES:
        hovertemplate = kwargs.get("hovertemplate")
        transformer = None
        attr = kwargs.get(axis)
        if isinstance(attr, str) and "." in attr:
            transformer = attr
            attr = attr.split(".")[-1]

        if attr is None:
            if dim not in list(axis_attrs.values()) + assigned_attrs:
                attr = dim
            else:
                attr = data_vars[0]
                if len(data_vars) > 1:
                    warnings.warn(
                        f"dataset contains more than one data variable; "
                        f"variable '{attr}' has been selected for plotting"
                    )
                if "{axis}" in hovertemplate:
                    kwargs["hovertemplate"] = hovertemplate.format(axis=axis)

        if f"%{{{axis}units}}" in kwargs.get("hovertemplate"):
            kwargs["hovertemplate"] = kwargs["hovertemplate"].replace(
                f"%{{{axis}units}}", metadata.get_units(dataset, attr) or ""
            )
        kwargs[axis] = dataset[attr].values
        axis_attrs[axis] = attr
        if transformer is not None:
            kwargs = self.transform(transformer, axis, kwargs)

        if getattr(self.layout, f"{axis}axis").title.text is None:
            title = metadata.get_axis_title(dataset, attr)
            self.update_layout(**{f"{axis}axis": {"title": title}})

    return args, kwargs


@discard_input_only_kwargs
def numpy(self, data, args, kwargs):
    try:
        ndarray = emohawk.open(data).to_numpy()
    except (NotImplementedError, ValueError):
        return None

    x = kwargs.get("x")
    y = kwargs.get("y")
    if isinstance(x, str):
        kwargs = self.transform(x, "x", kwargs)
        x = kwargs["x"]
    if isinstance(y, str):
        kwargs = self.transform(y, "y", kwargs)
        y = kwargs["y"]

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

    kwargs = {**kwargs, **{"x": x, "y": y}}

    return args, kwargs


@discard_input_only_kwargs
def plotly(self, data, args, kwargs):
    transformed_axes = []
    for axis in self.AXES:
        if isinstance(kwargs.get(axis), str):
            kwargs = self.transform(kwargs[axis], axis, kwargs)
            transformed_axes.append(axis)
    return args, kwargs
