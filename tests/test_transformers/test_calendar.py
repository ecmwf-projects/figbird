# (C) Copyright 2022 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from datetime import datetime

import numpy as np
import pytest

from figbird.transformers import calendar


def test_season_to_datetime():
    year = calendar.DUMMY_YEAR
    assert calendar.season_to_datetime("DJF") == datetime(year, 1, 16, 12)
    assert calendar.season_to_datetime("DJ") == datetime(year, 1, 1, 0)
    assert calendar.season_to_datetime("FMAM") == datetime(year, 4, 1, 0)
    assert calendar.season_to_datetime("JFM") == datetime(year, 2, 14, 0)
    assert calendar.season_to_datetime("JFM", 2022) == datetime(2022, 2, 14, 0)


def test_month_12_months():
    year = calendar.DUMMY_YEAR
    assert np.array_equal(
        list(calendar.month([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])),
        [
            datetime(year, 1, 16, 12),
            datetime(year, 2, 14, 0),
            datetime(year, 3, 16, 12),
            datetime(year, 4, 16, 0),
            datetime(year, 5, 16, 12),
            datetime(year, 6, 16, 0),
            datetime(year, 7, 16, 0),
            datetime(year, 8, 16, 12),
            datetime(year, 9, 16, 0),
            datetime(year, 10, 16, 12),
            datetime(year, 11, 16, 0),
            datetime(year, 12, 16, 12),
        ],
    )


def test_month_missing_months():
    year = calendar.DUMMY_YEAR
    assert np.array_equal(
        list(calendar.month([4, 6, 9, 10])),
        [
            datetime(year, 4, 16, 0),
            datetime(year, 6, 16, 0),
            datetime(year, 9, 16, 0),
            datetime(year, 10, 16, 12),
        ],
    )


def test_month_cyclic_12_months():
    year = calendar.DUMMY_YEAR
    assert np.array_equal(
        list(calendar.month([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], cyclic=True)),
        [
            datetime(year - 1, 12, 16, 12),
            datetime(year, 1, 16, 12),
            datetime(year, 2, 14, 0),
            datetime(year, 3, 16, 12),
            datetime(year, 4, 16, 0),
            datetime(year, 5, 16, 12),
            datetime(year, 6, 16, 0),
            datetime(year, 7, 16, 0),
            datetime(year, 8, 16, 12),
            datetime(year, 9, 16, 0),
            datetime(year, 10, 16, 12),
            datetime(year, 11, 16, 0),
            datetime(year, 12, 16, 12),
            datetime(year + 1, 1, 16, 12),
        ],
    )


def test_month_cyclic_missing_months():
    year = calendar.DUMMY_YEAR
    with pytest.warns(UserWarning):
        assert np.array_equal(
            list(calendar.month([4, 6, 9, 10], cyclic=True)),
            [
                datetime(year, 4, 16, 0),
                datetime(year, 6, 16, 0),
                datetime(year, 9, 16, 0),
                datetime(year, 10, 16, 12),
            ],
        )
        assert np.array_equal(
            list(calendar.month([1, 4, 6, 9, 10, 12], cyclic=True)),
            [
                datetime(year, 1, 16, 12),
                datetime(year, 4, 16, 0),
                datetime(year, 6, 16, 0),
                datetime(year, 9, 16, 0),
                datetime(year, 10, 16, 12),
                datetime(year, 12, 16, 12),
            ],
        )
