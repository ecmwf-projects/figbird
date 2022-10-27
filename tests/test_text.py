# (C) Copyright 2022 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from figbird import text


def test_pretty_units_map():
    assert text.pretty_units("celsius") == "°C"
    assert text.pretty_units("10celsius m2") == "10°Cm<sup>2</sup>"
    assert text.pretty_units("bananas") == "bananas"


def test_pretty_units_exponents():
    assert text.pretty_units("m s-1") == "ms<sup>-1</sup>"
    assert text.pretty_units("m2") == "m<sup>2</sup>"
    assert text.pretty_units("10m3s-1") == "10m<sup>3</sup>s<sup>-1</sup>"


def test_pretty_units_unknown():
    assert text.pretty_units("bananas") == "bananas"
    assert text.pretty_units("bananas2") == "bananas<sup>2</sup>"
