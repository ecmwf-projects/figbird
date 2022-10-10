import random

import numpy as np
import plotly.graph_objects as go
from num2words import num2words

from . import colors, inputs
from .schema import schema


@schema.line.apply()
@inputs.polymorphic_input
def line(*args, **kwargs):
    return go.Scatter(*args, **kwargs)


@schema.envelope.apply()
def envelope(data, envelope_dim=None, grouped_hoverlabel=False, **kwargs):
    if not isinstance(data, (list, tuple)):
        data = _split_envelope(data, envelope_dim)

    hover_kwargs = dict()
    if grouped_hoverlabel:
        hover_kwargs = dict()
        if isinstance(grouped_hoverlabel, dict):
            hover_kwargs = grouped_hoverlabel
        hover_kwargs = _grouped_hoverlabel_kwargs(data, envelope_dim, **hover_kwargs)
        kwargs["hoverinfo"] = "skip"

    line_kwargs = kwargs.pop("line", dict())
    if "color" not in line_kwargs:
        line_kwargs["color"] = colors.next_color()

    traces = []
    # FIXME: WE NEED A BETTER WAY OF AUTO-LABELLING GROUPS
    legendgroup = kwargs.get("name", f"envelope_{random.random()}")
    showlegend = True
    for i, (bottom, top) in enumerate(_iter_envelopes(data)):
        if top is None and line_kwargs["width"] == 0:
            line_kwargs["width"] = schema.line.line.width
            if grouped_hoverlabel:
                kwargs.pop("hoverinfo", None)
                kwargs = {**hover_kwargs, **kwargs}

        trace_kwargs = {
            **{"showlegend": False, "legendgroup": legendgroup},
            **kwargs,
        }
        traces.append(line(bottom, line=line_kwargs, **trace_kwargs))
        if top is not None:
            if not len(data) % 2 and i + 1 == len(data) / 2:
                kwargs.pop("hoverinfo", None)
                kwargs = {**hover_kwargs, **kwargs}
            trace_kwargs = {
                **{
                    "showlegend": showlegend,
                    "legendgroup": legendgroup,
                    "fill": "tonexty",
                },
                **kwargs,
            }
            traces.append(line(top, line=line_kwargs, **trace_kwargs))
        showlegend = False
    return traces


def _split_envelope(data, envelope_dim=None):
    if envelope_dim is None:
        raise TypeError("'envelope_dim' arg required for non-list data")
    data = [data.isel(**{envelope_dim: i}) for i in range(len(data[envelope_dim]))]
    return data


def _grouped_hoverlabel_kwargs(data, envelope_dim, bound_names=None, units=None):
    kwargs = dict()
    kwargs["customdata"] = np.dstack(data)[0]

    bound_names = _get_bound_names(data, envelope_dim, bound_names)
    data_units = _get_data_units(data, units)
    labels = [
        f"{bound_names[i]}%{{customdata[{i}]:{schema.settings.hover_precision}}}{data_units[i]}"
        for i in range(len(data))
    ][::-1]
    kwargs["hovertemplate"] = "<br>".join(labels)
    kwargs["hoverinfo"] = "skip"
    return kwargs


def _get_bound_names(data, envelope_dim, bound_names):
    bound_names = bound_names or _auto_bound_names(data, envelope_dim)
    if isinstance(bound_names, (list, tuple)):
        bound_names = [f"{bound_name}: " for bound_name in bound_names]
    else:
        bound_names = [""] * len(data)
    return bound_names


def _auto_bound_names(data, envelope_dim):
    if envelope_dim is not None:
        try:
            return [
                f"{envelope_dim}={item[envelope_dim].values.item()}" for item in data
            ]
        except:  # noqa: E722
            pass

    n_bounds = len(data)
    tops = ["top"]
    bottoms = ["bottom"]
    for i in range((n_bounds - 2) // 2):
        ordinal = num2words(i + 2, ordinal=True)
        tops.append(f"{ordinal} top")
        bottoms.append(f"{ordinal} bottom")
    middle = ["middle"] if n_bounds % 2 else []
    return bottoms + middle + tops[::-1]


def _get_data_units(data, data_units):
    data_units = data_units or ""
    if not isinstance(data_units, (list, tuple)):
        data_units = [data_units] * len(data)
    return data_units


def _iter_envelopes(envelopes):
    for i in range(len(envelopes) // 2):
        yield envelopes[i], envelopes[-i - 1]
    if len(envelopes) % 2:
        yield envelopes[len(envelopes) // 2], None
