# (C) Copyright 2022 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from . import figures
from .schema import schema

try:
    # NOTE: the `version.py` file must not be present in the git repository
    #   as it is generated by setuptools at install time
    from .version import __version__
except ImportError:  # pragma: no cover
    # Local copy or not installed with setuptools
    __version__ = "999"


@figures.Figure.new_if_none()
def line(*args, fig=None, **kwargs):
    return fig.add_line(*args, **kwargs)


@figures.Figure.new_if_none()
def scatter(*args, fig=None, **kwargs):
    return fig.add_scatter(*args, **kwargs)


@figures.Figure.new_if_none()
def bar(*args, fig=None, **kwargs):
    return fig.add_bar(*args, **kwargs)


@figures.Figure.new_if_none()
def envelope(*args, fig=None, **kwargs):
    return fig.add_envelope(*args, **kwargs)


@figures.Figure.new_if_none(schema=schema.figures.stripes)
def stripes(*args, fig=None, **kwargs):
    return fig.add_stripes(*args, **kwargs)
