# (C) Copyright 2022 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

LABEL_PREFERENCE = [
    "long_name",
    "name",
    "standard_name",
    "short_name",
    "var_name",
]


def get_axis_title(data, attr=None):
    title = get_label(data, attr) or str()
    units = get_units(data, attr)
    if units:
        title = f"{title} ({units})"
    return title


def get_label(data, attr=None):
    if attr is not None:
        data = data[attr]
    for item in LABEL_PREFERENCE:
        try:
            label = getattr(data, item)
            break
        except AttributeError:
            continue
    else:
        label = attr
    return label


def get_units(data, attr=None):
    units = ""
    if attr is not None:
        data = data[attr]
    try:
        units = data.units
    except AttributeError:
        pass
    return units


def split_dim(dataarray, dim):
    dataarray = [dataarray.isel(**{dim: i}) for i in range(len(dataarray[dim]))]
    return dataarray


def dim_labels(dataarray, dim):
    labels = [f"{dim}={value}" for value in dataarray[dim].values()]
    return labels
