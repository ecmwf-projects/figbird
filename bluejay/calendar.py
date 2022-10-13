from datetime import datetime, timedelta

from dateutil import relativedelta

from . import Figure, envelopes, plot
from .schema import schema


class CalendarFigure(Figure):
    TRACE_MODULE = "calendar"
    SCHEMA = schema.calendar


SEASON_TO_INT = {
    "DJF": 1,
    "MAM": 2,
    "JJA": 3,
    "SON": 4,
}


MONTH_CENTRES = [16, 14, 16, 15, 16, 15, 16, 16, 15, 16, 15, 16]
MONTH_HOURS = [0, 12, 0, 12, 0, 12, 0, 0, 12, 0, 12, 0]


def _get_calendar_axes(data):
    data = data.to_array().squeeze()
    frequencies = {
        "month": _month_axes,
        "dayofyear": _day_axes,
        "weekofyear": _week_axes,
        "season": _season_axes,
    }
    for dim in data.dims:
        frequency = dim.split("_")[0]
        if frequency in frequencies:
            x, y = frequencies[frequency](data, x_dim=dim)
            break
    else:
        pass
    return x, y


def _day_axes(data, x_dim="dayofyear"):
    days = data[x_dim].values[:-1]
    x = [datetime(2, 1, 1) + timedelta(days=int(day)) for day in days]
    x = [x[0] - timedelta(days=1)] + x + [x[-1] + timedelta(days=1)]
    y = list(data.values)[:-1]
    y = [y[-1]] + y + [y[0]]
    return x, y


def _week_axes(data, x_dim="weekofyear"):
    weeks = data[x_dim].values
    x = [datetime(2, 1, 1) + timedelta(days=int(week) * 7 - 3.5) for week in weeks]
    x = [x[0] - timedelta(days=7)] + x + [x[-1] + timedelta(days=7)]
    y = list(data.values)
    y = [y[-1]] + y + [y[0]]
    return x, y


def _month_axes(data, x_dim="month"):
    months = data[x_dim].values
    x = [
        datetime(2, int(month), MONTH_CENTRES[i], MONTH_HOURS[i])
        for i, month in enumerate(months)
    ]
    x = [x[0] - timedelta(days=31)] + x + [x[-1] + timedelta(days=31)]
    y = list(data.values)
    y = [y[-1]] + y + [y[0]]
    return x, y


def _season_axes(data, x_dim="season"):
    seasons = sorted(data[x_dim].values, key=lambda season: SEASON_TO_INT[season])
    x = [datetime(2, (SEASON_TO_INT[season] - 1) * 3 + 1, 16) for season in seasons]
    x = sorted(x)
    x = (
        [x[0] - relativedelta.relativedelta(months=3)]
        + x
        + [x[-1] + relativedelta.relativedelta(months=3)]
    )
    y = [value for _, value in sorted(zip(seasons, data.values))]
    y = [y[-1]] + y + [y[0]]
    return x, y


def _auto_hovertemplate(data):
    templates = {
        "month": lambda: {
            "hovertemplate": f"%{{y:{schema.settings.hoverprecision}}}<extra>%{{x|%B}}</extra>",
        },
        "dayofyear": lambda: {
            "hovertemplate": f"%{{y:{schema.settings.hoverprecision}}}<extra>%{{x|%-d %B}}</extra>",
        },
        "weekofyear": lambda: {
            "customdata": [
                date - timedelta(days=3.5) for date in _get_calendar_axes(data)[0]
            ],
            "hovertemplate": (
                f"%{{y:{schema.settings.hoverprecision}}}<extra>w/c %{{customdata|%-d %B}}</extra>"
            ),
        },
        "season": lambda: {
            "customdata": [
                "Autumn (SON)",
                "Winter (DJF)",
                "Spring (MAM)",
                "Summer (JJA)",
                "Autumn (SON)",
                "Winter (DJF)",
            ],
            "hovertemplate": f"%{{y:{schema.settings.hoverprecision}}}<extra>%{{customdata}}</extra>",
        },
    }
    for dim in data.dims:
        frequency = dim.split("_")[0]
        if frequency in templates:
            return templates[frequency]()


@CalendarFigure.create_if_none
def line(data, *args, fig=None, **kwargs):
    x, y = _get_calendar_axes(data)
    plot.line(*args, x=x, y=y, fig=fig, **kwargs)
    return fig


@CalendarFigure.create_if_none
def envelope(data, envelope_dim=None, *args, fig=None, **kwargs):
    if not isinstance(data, (list, tuple)):
        data = envelopes._split_envelope(data, envelope_dim)
    y_values = []
    for item in data:
        x, y = _get_calendar_axes(item)
        y_values.append(y)
    envelopes.envelope(y_values, *args, x=x, fig=fig, **kwargs)
    return fig
