# (C) Copyright 2022 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.


def get(key, kwargs):
    if key in kwargs:
        value = kwargs[key]
    else:
        magic_key, *child_key = key.split("_")
        child_key = "_".join(child_key)
        value = kwargs.get(magic_key, dict()).get(child_key)
    return value
